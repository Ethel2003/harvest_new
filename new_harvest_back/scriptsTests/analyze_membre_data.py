#!/usr/bin/env python3
"""
Script d'analyse et de correction des données JSON des membres
Pour préparer l'enregistrement multiple via l'API
"""

import json
import re
from datetime import datetime, date
from typing import List, Dict, Any

def validate_date_format(date_str: str) -> str:
    """
    Valide et corrige le format de date
    Retourne une date valide ou None si impossible à corriger
    """
    if not date_str or date_str == "0000-00-00" or date_str == "":
        return None
    
    # Formats de date acceptés
    date_formats = [
        "%Y-%m-%d",      # 1990-05-15
        "%d/%m/%Y",      # 15/05/1990
        "%d-%m-%Y",      # 15-05-1990
        "%Y/%m/%d",      # 1990/05/15
        "%d.%m.%Y",      # 15.05.1990
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    # Si aucun format ne fonctionne, essayer de nettoyer la chaîne
    cleaned_date = re.sub(r'[^\d\-/]', '', date_str)
    if cleaned_date:
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(cleaned_date, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
    
    return None

def validate_phone(phone: str) -> str:
    """
    Valide et corrige le format de téléphone
    """
    if not phone:
        return None
    
    # Nettoyer le numéro de téléphone
    cleaned_phone = re.sub(r'[^\d\+]', '', phone)
    
    # Ajouter le préfixe +33 si nécessaire
    if cleaned_phone.startswith('0') and len(cleaned_phone) == 10:
        cleaned_phone = '+33' + cleaned_phone[1:]
    elif not cleaned_phone.startswith('+'):
        cleaned_phone = '+' + cleaned_phone
    
    return cleaned_phone

def validate_email(email: str) -> str:
    """
    Valide le format d'email
    """
    if not email:
        return None
    
    # Regex simple pour valider l'email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    
    return None

def validate_choices(value: str, choices: List[str], field_name: str) -> str:
    """
    Valide les choix prédéfinis
    """
    if not value:
        return None
    
    # Normaliser la valeur
    normalized_value = value.lower().strip()
    
    # Mapper les variations courantes
    choice_mapping = {
        'genre': {
            'm': 'masculin',
            'f': 'feminin',
            'homme': 'masculin',
            'femme': 'feminin',
            'male': 'masculin',
            'female': 'feminin'
        },
        'situation_matrimoniale': {
            'célibataire': 'celibataire',
            'marié': 'marie',
            'mariée': 'marie',
            'divorcé': 'celibataire',
            'divorcée': 'celibataire',
            'veuf': 'celibataire',
            'veuve': 'celibataire'
        },
        'statut': {
            'inscription': 'inscrit',
            'membre actif': 'membre',
            'actif': 'membre'
        }
    }
    
    # Vérifier dans le mapping
    if field_name in choice_mapping:
        if normalized_value in choice_mapping[field_name]:
            return choice_mapping[field_name][normalized_value]
    
    # Vérifier dans les choix valides
    if normalized_value in [choice.lower() for choice in choices]:
        return normalized_value
    
    return None

def clean_membre_data(membre: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nettoie et valide les données d'un membre
    """
    cleaned_membre = {}
    
    # Champs texte simples
    text_fields = ['nom', 'prenom', 'adresse', 'ville', 'profession', 'nationalite']
    for field in text_fields:
        value = membre.get(field, '').strip() if membre.get(field) else None
        cleaned_membre[field] = value if value else None
    
    # Téléphone
    cleaned_membre['telephone'] = validate_phone(membre.get('telephone', ''))
    
    # Email
    cleaned_membre['email'] = validate_email(membre.get('email', ''))
    
    # Date de naissance
    date_naissance = membre.get('date_naissance', '')
    cleaned_membre['date_naissance'] = validate_date_format(date_naissance)
    
    # Genre
    cleaned_membre['genre'] = validate_choices(
        membre.get('genre', ''), 
        ['masculin', 'feminin'], 
        'genre'
    )
    
    # Situation matrimoniale
    cleaned_membre['situation_matrimoniale'] = validate_choices(
        membre.get('situation_matrimoniale', ''), 
        ['celibataire', 'marie'], 
        'situation_matrimoniale'
    )
    
    # Statut
    cleaned_membre['statut'] = validate_choices(
        membre.get('statut', ''), 
        ['inscrit', 'membre'], 
        'statut'
    ) or 'inscrit'  # Valeur par défaut
    
    # Couleur (valeur par défaut si manquante)
    cleaned_membre['color'] = membre.get('color', '1')
    
    # UUID (générer si manquant)
    if not membre.get('uuid'):
        import uuid
        cleaned_membre['uuid'] = str(uuid.uuid4())
    else:
        cleaned_membre['uuid'] = membre.get('uuid')
    
    return cleaned_membre

def analyze_json_file(file_path: str) -> Dict[str, Any]:
    """
    Analyse un fichier JSON de membres et retourne un rapport
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de format JSON: {e}")
        return None
    
    print(f"📊 Analyse du fichier: {file_path}")
    print(f"📋 Nombre total d'enregistrements: {len(data)}")
    
    # Statistiques
    stats = {
        'total': len(data),
        'errors': [],
        'warnings': [],
        'cleaned_data': []
    }
    
    # Analyser chaque membre
    for i, membre in enumerate(data):
        print(f"\n🔍 Analyse du membre {i+1}:")
        
        # Vérifier les champs requis
        if not membre.get('nom') and not membre.get('prenom'):
            error = f"Membre {i+1}: Nom et prénom manquants"
            stats['errors'].append(error)
            print(f"❌ {error}")
            continue
        
        # Nettoyer les données
        cleaned_membre = clean_membre_data(membre)
        
        # Vérifier les problèmes potentiels
        warnings = []
        if not cleaned_membre['date_naissance']:
            warnings.append("Date de naissance invalide ou manquante")
        if not cleaned_membre['telephone']:
            warnings.append("Téléphone invalide ou manquant")
        if not cleaned_membre['email']:
            warnings.append("Email invalide ou manquant")
        if not cleaned_membre['genre']:
            warnings.append("Genre invalide ou manquant")
        
        if warnings:
            stats['warnings'].extend([f"Membre {i+1}: {w}" for w in warnings])
            for warning in warnings:
                print(f"⚠️ {warning}")
        
        stats['cleaned_data'].append(cleaned_membre)
        print(f"✅ Membre nettoyé: {cleaned_membre.get('prenom', '')} {cleaned_membre.get('nom', '')}")
    
    return stats

def save_cleaned_data(cleaned_data: List[Dict], output_file: str):
    """
    Sauvegarde les données nettoyées dans un nouveau fichier
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Données nettoyées sauvegardées dans: {output_file}")

def create_test_script(cleaned_data: List[Dict], output_file: str):
    """
    Crée un script de test avec les données nettoyées
    """
    script_content = f'''#!/usr/bin/env python3
"""
Script de test généré automatiquement pour l'enregistrement multiple
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {{"Content-Type": "application/json", "Accept": "application/json"}}

def login():
    """Authentification"""
    login_data = {{"email": "utilisateur1@example.com", "password": "motdepasse"}}
    
    try:
        response = requests.post(f"{{BASE_URL}}/login", json=login_data, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            token = data["data"]["token"]
            HEADERS["Authorization"] = f"Token {{token}}"
            print("✅ Authentification réussie")
            return True
        else:
            print(f"❌ Échec de l'authentification: {{response.status_code}}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {{e}}")
        return False

def test_create_multiple_membres():
    """Test d'enregistrement multiple avec les données nettoyées"""
    print("\\n👥 Test d'enregistrement multiple...")
    
    # Données nettoyées
    membres_data = {json.dumps(cleaned_data, ensure_ascii=False, indent=8)}
    
    try:
        response = requests.post(
            f"{{BASE_URL}}/membres/store_multiple/", 
            json=membres_data, 
            headers=HEADERS
        )
        print(f"Status: {{response.status_code}}")
        print(f"Response: {{response.json()}}")
        
        if response.status_code == 201:
            print("✅ Membres créés avec succès")
        else:
            print(f"❌ Erreur: {{response.text}}")
    except Exception as e:
        print(f"❌ Exception: {{e}}")

if __name__ == "__main__":
    if login():
        test_create_multiple_membres()
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📝 Script de test créé: {output_file}")

def main():
    """Fonction principale"""
    print("🔧 Analyseur de données JSON pour l'enregistrement multiple")
    print("=" * 60)
    
    # Demander le chemin du fichier
    file_path = input("📁 Chemin vers le fichier JSON: ").strip()
    
    if not file_path:
        print("❌ Chemin de fichier requis")
        return
    
    # Analyser le fichier
    stats = analyze_json_file(file_path)
    
    if not stats:
        return
    
    # Afficher le rapport
    print(f"\n📊 RAPPORT D'ANALYSE")
    print("=" * 60)
    print(f"Total d'enregistrements: {stats['total']}")
    print(f"Données nettoyées: {len(stats['cleaned_data'])}")
    print(f"Erreurs: {len(stats['errors'])}")
    print(f"Avertissements: {len(stats['warnings'])}")
    
    if stats['errors']:
        print(f"\n❌ ERREURS:")
        for error in stats['errors']:
            print(f"  - {error}")
    
    if stats['warnings']:
        print(f"\n⚠️ AVERTISSEMENTS:")
        for warning in stats['warnings'][:10]:  # Limiter l'affichage
            print(f"  - {warning}")
        if len(stats['warnings']) > 10:
            print(f"  ... et {len(stats['warnings']) - 10} autres")
    
    # Sauvegarder les données nettoyées
    if stats['cleaned_data']:
        output_file = file_path.replace('.json', '_cleaned.json')
        save_cleaned_data(stats['cleaned_data'], output_file)
        
        # Créer un script de test
        test_script = file_path.replace('.json', '_test.py')
        create_test_script(stats['cleaned_data'], test_script)
        
        print(f"\n✅ Prêt pour les tests !")
        print(f"   - Données nettoyées: {output_file}")
        print(f"   - Script de test: {test_script}")

if __name__ == "__main__":
    main() 