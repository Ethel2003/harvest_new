#!/usr/bin/env python3
"""
Script simple pour corriger le format de date 0000-00-00 dans les fichiers JSON
"""

import json
import sys

def fix_date_format(input_file, output_file=None):
    """
    Corrige les dates au format 0000-00-00 dans un fichier JSON
    """
    if output_file is None:
        output_file = input_file.replace('.json', '_fixed.json')
    
    try:
        # Lire le fichier JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Fichier lu: {input_file}")
        print(f"📋 Nombre d'enregistrements: {len(data)}")
        
        # Compter les corrections
        corrections = 0
        
        # Traiter chaque enregistrement
        for i, record in enumerate(data):
            # Vérifier le champ date_naissance
            if 'date_naissance' in record:
                if record['date_naissance'] == "0000-00-00" or record['date_naissance'] == "":
                    record['date_naissance'] = None
                    corrections += 1
                    print(f"✅ Enregistrement {i+1}: Date corrigée")
            
            # Vérifier d'autres champs de date potentiels
            date_fields = ['date_naissance', 'date_creation', 'date_modification', 'created_at', 'updated_at']
            for field in date_fields:
                if field in record and record[field] == "0000-00-00":
                    record[field] = None
                    corrections += 1
                    print(f"✅ Enregistrement {i+1}: Champ {field} corrigé")
        
        # Sauvegarder le fichier corrigé
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 RAPPORT DE CORRECTION")
        print("=" * 40)
        print(f"Total d'enregistrements: {len(data)}")
        print(f"Corrections effectuées: {corrections}")
        print(f"Fichier corrigé: {output_file}")
        
        return data
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {input_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de format JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return None

def create_test_script(data, output_file):
    """
    Crée un script de test pour l'enregistrement multiple
    """
    script_content = f'''#!/usr/bin/env python3
"""
Script de test pour l'enregistrement multiple avec données corrigées
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
    """Test d'enregistrement multiple"""
    print("\\n👥 Test d'enregistrement multiple...")
    
    # Données corrigées
    membres_data = {json.dumps(data, ensure_ascii=False, indent=8)}
    
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
    if len(sys.argv) < 2:
        print("🔧 Correcteur de format de date JSON")
        print("=" * 40)
        print("Usage: python fix_date_format.py <fichier_json>")
        print("Exemple: python fix_date_format.py membres_202506271515.json")
        return
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.json', '_fixed.json')
    
    print("🔧 Correction du format de date...")
    print("=" * 40)
    
    # Corriger le fichier
    data = fix_date_format(input_file, output_file)
    
    if data:
        # Créer un script de test
        test_script = input_file.replace('.json', '_test.py')
        create_test_script(data, test_script)
        
        print(f"\n✅ Prêt pour les tests !")
        print(f"   - Fichier corrigé: {output_file}")
        print(f"   - Script de test: {test_script}")
        print(f"\n💡 Pour tester: python {test_script}")

if __name__ == "__main__":
    main() 