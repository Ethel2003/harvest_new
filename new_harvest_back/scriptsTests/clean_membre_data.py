#!/usr/bin/env python3
"""
Script pour nettoyer et préparer les données des membres pour l'API
Utilise le fichier JSON corrigé et le prépare pour l'enregistrement multiple
"""

import json
import re
import uuid

def clean_phone_number(phone):
    """
    Nettoie et standardise les numéros de téléphone béninois
    """
    if not phone or phone == "null":
        return None
    
    # Nettoyer le numéro
    cleaned = re.sub(r'[^\d\+\(\)]', '', phone)
    
    # Gérer les cas spéciaux
    if cleaned.startswith('-'):
        cleaned = cleaned[1:]
    
    # Si le numéro commence par 229, c'est déjà au bon format
    if cleaned.startswith('229'):
        return '+' + cleaned
    
    # Si le numéro commence par 22, ajouter le +
    if cleaned.startswith('22'):
        return '+' + cleaned
    
    # Si c'est un numéro local (8-9 chiffres), ajouter +229
    if len(cleaned) in [8, 9] and cleaned.isdigit():
        return '+229' + cleaned
    
    # Si c'est un numéro avec préfixe 229 (10-11 chiffres)
    if len(cleaned) in [10, 11] and cleaned.startswith('229'):
        return '+' + cleaned
    
    # Si c'est un numéro avec préfixe 22 (10-11 chiffres)
    if len(cleaned) in [10, 11] and cleaned.startswith('22'):
        return '+' + cleaned
    
    return None

def clean_email(email):
    """
    Nettoie les adresses email
    """
    if not email or email == "null":
        return None
    
    # Nettoyer l'email
    cleaned = email.strip().lower()
    
    # Vérifier si l'email contient des espaces ou caractères invalides
    if ' ' in cleaned or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', cleaned):
        return None
    
    return cleaned

def clean_membre_data(membre):
    """
    Nettoie et corrige les données d'un membre
    """
    cleaned = {}
    
    # Champs texte simples
    text_fields = ['nom', 'prenom', 'adresse', 'ville', 'profession', 'nationalite']
    for field in text_fields:
        value = membre.get(field)
        if value and value != "null":
            cleaned[field] = value.strip()
        else:
            cleaned[field] = None
    
    # Téléphone
    cleaned['telephone'] = clean_phone_number(membre.get('telephone'))
    
    # Email
    cleaned['email'] = clean_email(membre.get('email'))
    
    # Date de naissance (déjà corrigée à null)
    cleaned['date_naissance'] = None if membre.get('date_naissance') == "null" else membre.get('date_naissance')
    
    # Genre (déjà correct)
    cleaned['genre'] = membre.get('genre', 'feminin')
    
    # Situation matrimoniale (déjà correct)
    cleaned['situation_matrimoniale'] = membre.get('situation_matrimoniale', 'celibataire')
    
    # Statut (déjà correct)
    cleaned['statut'] = membre.get('statut', 'inscrit')
    
    # Couleur
    cleaned['color'] = membre.get('color', '1')
    
    # UUID (générer si manquant)
    if not membre.get('uuid'):
        cleaned['uuid'] = str(uuid.uuid4())
    else:
        cleaned['uuid'] = membre.get('uuid')
    
    return cleaned

def process_membres_data(input_file, output_file=None):
    """
    Traite les données des membres
    """
    if output_file is None:
        output_file = input_file.replace('_fixed.json', '_cleaned.json')
    
    try:
        # Charger les données corrigées
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Traitement du fichier: {input_file}")
        print(f"📋 Nombre d'enregistrements: {len(data)}")
        
        # Statistiques
        stats = {
            'total': len(data),
            'cleaned_data': [],
            'phone_fixes': 0,
            'email_fixes': 0,
            'warnings': []
        }
        
        # Traiter chaque membre
        for i, membre in enumerate(data):
            if i % 50 == 0:  # Afficher le progrès tous les 50 membres
                print(f"🔄 Traitement: {i+1}/{len(data)}")
            
            # Vérifier les champs requis
            if not membre.get('nom') and not membre.get('prenom'):
                stats['warnings'].append(f"Membre {i+1}: Nom et prénom manquants")
                continue
            
            # Nettoyer les données
            cleaned_membre = clean_membre_data(membre)
            
            # Compter les corrections
            if cleaned_membre['telephone'] != membre.get('telephone'):
                stats['phone_fixes'] += 1
            
            if cleaned_membre['email'] != membre.get('email'):
                stats['email_fixes'] += 1
            
            # Vérifier les problèmes potentiels
            if not cleaned_membre['telephone']:
                stats['warnings'].append(f"Membre {i+1}: Téléphone invalide")
            if not cleaned_membre['email']:
                stats['warnings'].append(f"Membre {i+1}: Email invalide")
            
            stats['cleaned_data'].append(cleaned_membre)
        
        # Sauvegarder les données nettoyées
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats['cleaned_data'], f, ensure_ascii=False, indent=2)
        
        print(f"✅ Données nettoyées sauvegardées: {output_file}")
        
        return stats, output_file
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement: {e}")
        return None, None

def create_final_test_script(cleaned_data, output_file):
    """
    Crée le script de test final
    """
    script_content = f'''#!/usr/bin/env python3
"""
Script de test final pour l'enregistrement multiple des membres
Données nettoyées et optimisées pour l'API
"""

import requests
import json
import time

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
            print(f"Réponse: {{response.text}}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {{e}}")
        return False

def test_single_membre():
    """Test avec un seul membre"""
    print("\\n🧪 Test avec un seul membre...")
    
    # Charger les données nettoyées
    with open('membres_202506271515_cleaned.json', 'r', encoding='utf-8') as f:
        membres_data = json.load(f)
    
    if membres_data:
        test_membre = membres_data[0]
        
        try:
            response = requests.post(
                f"{{BASE_URL}}/membres/", 
                json=test_membre, 
                headers=HEADERS
            )
            
            print(f"Status: {{response.status_code}}")
            
            if response.status_code == 201:
                print("✅ Test avec un membre réussi")
                return True
            else:
                print(f"❌ Erreur: {{response.text}}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {{e}}")
            return False
    
    return False

def test_create_multiple_membres():
    """Test d'enregistrement multiple par lots"""
    print("\\n👥 Test d'enregistrement multiple...")
    
    # Charger les données nettoyées
    with open('membres_202506271515_cleaned.json', 'r', encoding='utf-8') as f:
        membres_data = json.load(f)
    
    print(f"📊 Total de membres à traiter: {{len(membres_data)}}")
    
    # Diviser en lots de 30 pour éviter les timeouts
    batch_size = 30
    total_membres = len(membres_data)
    success_count = 0
    error_count = 0
    
    for i in range(0, total_membres, batch_size):
        batch = membres_data[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_membres + batch_size - 1) // batch_size
        
        print(f"\\n🔄 Lot {{batch_num}}/{{total_batches}} ({{len(batch)}} membres)")
        
        try:
            response = requests.post(
                f"{{BASE_URL}}/membres/store_multiple/", 
                json=batch, 
                headers=HEADERS,
                timeout=60
            )
            
            print(f"Status: {{response.status_code}}")
            
            if response.status_code == 201:
                success_count += len(batch)
                print(f"✅ Lot {{batch_num}} réussi")
            else:
                error_count += len(batch)
                print(f"❌ Erreur lot {{batch_num}}: {{response.text}}")
            
            # Pause entre les lots
            if i + batch_size < total_membres:
                print("⏳ Pause de 3 secondes...")
                time.sleep(3)
                
        except Exception as e:
            error_count += len(batch)
            print(f"❌ Exception lot {{batch_num}}: {{e}}")
    
    print(f"\\n📊 RAPPORT FINAL")
    print("=" * 40)
    print(f"Total de membres: {{total_membres}}")
    print(f"Succès: {{success_count}}")
    print(f"Erreurs: {{error_count}}")
    print(f"Taux de succès: {{(success_count/total_membres)*100:.1f}}%")

if __name__ == "__main__":
    print("🚀 Test d'enregistrement des membres")
    print("=" * 50)
    
    if login():
        # Test avec un seul membre d'abord
        if test_single_membre():
            # Si le test simple réussit, faire l'enregistrement multiple
            test_create_multiple_membres()
        else:
            print("\\n❌ Le test simple a échoué. Vérifiez le format des données.")
    else:
        print("\\n❌ Impossible de continuer sans authentification.")
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📝 Script de test final créé: {output_file}")

def main():
    """Fonction principale"""
    input_file = "membres_202506271515_fixed.json"
    output_file = "membres_202506271515_cleaned.json"
    test_script = "test_import_final.py"
    
    print("🔧 Nettoyage des données membres")
    print("=" * 50)
    
    # Traiter les données
    stats, cleaned_file = process_membres_data(input_file, output_file)
    
    if stats:
        # Afficher le rapport
        print(f"\n📊 RAPPORT DE NETTOYAGE")
        print("=" * 50)
        print(f"Total d'enregistrements: {stats['total']}")
        print(f"Données nettoyées: {len(stats['cleaned_data'])}")
        print(f"Corrections téléphone: {stats['phone_fixes']}")
        print(f"Corrections email: {stats['email_fixes']}")
        print(f"Avertissements: {len(stats['warnings'])}")
        
        if stats['warnings']:
            print(f"\n⚠️ AVERTISSEMENTS (premiers 10):")
            for warning in stats['warnings'][:10]:
                print(f"  - {warning}")
            if len(stats['warnings']) > 10:
                print(f"  ... et {len(stats['warnings']) - 10} autres")
        
        # Créer le script de test final
        create_final_test_script(stats['cleaned_data'], test_script)
        
        print(f"\n✅ Prêt pour les tests !")
        print(f"   - Données nettoyées: {cleaned_file}")
        print(f"   - Script de test: {test_script}")
        print(f"\n💡 Pour tester: python {test_script}")
        
        # Afficher un exemple
        if stats['cleaned_data']:
            print(f"\n📋 Exemple de données finales:")
            example = stats['cleaned_data'][0]
            print(json.dumps(example, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 