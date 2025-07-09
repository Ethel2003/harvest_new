#!/usr/bin/env python3
"""
Script pour corriger le format JSON du fichier membres_202506271515.json
Remplace None par null et corrige les autres problèmes de format
"""

import re
import json

def fix_json_format(input_file, output_file=None):
    """
    Corrige le format JSON en remplaçant None par null
    """
    if output_file is None:
        output_file = input_file.replace('.json', '_fixed.json')
    
    try:
        # Lire le fichier comme texte
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📊 Lecture du fichier: {input_file}")
        print(f"📏 Taille: {len(content)} caractères")
        
        # Remplacer None par null
        content = re.sub(r'\bNone\b', 'null', content)
        
        # Remplacer les dates 0000-00-00 par null
        content = re.sub(r'"0000-00-00"', 'null', content)
        
        # Nettoyer les espaces en trop
        content = re.sub(r',\s*}', '}', content)
        content = re.sub(r',\s*]', ']', content)
        
        # Sauvegarder le fichier corrigé
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fichier corrigé sauvegardé: {output_file}")
        
        # Tester si le JSON est valide
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ JSON valide - {len(data)} enregistrements")
            return data
        except json.JSONDecodeError as e:
            print(f"❌ JSON toujours invalide: {e}")
            return None
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement: {e}")
        return None

def create_simple_test_script(data, output_file):
    """
    Crée un script de test simple
    """
    script_content = f'''#!/usr/bin/env python3
"""
Script de test simple pour l'enregistrement multiple
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
    
    # Charger les données corrigées
    with open('membres_202506271515_fixed.json', 'r', encoding='utf-8') as f:
        membres_data = json.load(f)
    
    print(f"📊 Nombre de membres à traiter: {{len(membres_data)}}")
    
    # Traiter par lots de 20
    batch_size = 20
    success_count = 0
    
    for i in range(0, len(membres_data), batch_size):
        batch = membres_data[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        print(f"\\n🔄 Lot {{batch_num}} ({{len(batch)}} membres)")
        
        try:
            response = requests.post(
                f"{{BASE_URL}}/membres/store_multiple/", 
                json=batch, 
                headers=HEADERS,
                timeout=30
            )
            
            print(f"Status: {{response.status_code}}")
            
            if response.status_code == 201:
                success_count += len(batch)
                print(f"✅ Lot {{batch_num}} réussi")
            else:
                print(f"❌ Erreur lot {{batch_num}}: {{response.text}}")
                
        except Exception as e:
            print(f"❌ Exception lot {{batch_num}}: {{e}}")
    
    print(f"\\n📊 Résultat: {{success_count}}/{{len(membres_data)}} membres créés")

if __name__ == "__main__":
    if login():
        test_create_multiple_membres()
    else:
        print("❌ Impossible de continuer sans authentification.")
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📝 Script de test créé: {output_file}")

def main():
    """Fonction principale"""
    input_file = "membres_202506271515.json"
    output_file = "membres_202506271515_fixed.json"
    test_script = "test_import_simple.py"
    
    print("🔧 Correcteur de format JSON")
    print("=" * 40)
    
    # Corriger le format JSON
    data = fix_json_format(input_file, output_file)
    
    if data:
        # Créer un script de test simple
        create_simple_test_script(data, test_script)
        
        print(f"\n✅ Prêt pour les tests !")
        print(f"   - Fichier corrigé: {output_file}")
        print(f"   - Script de test: {test_script}")
        print(f"\n💡 Pour tester: python {test_script}")
        
        # Afficher un exemple
        if data:
            print(f"\n📋 Exemple de données corrigées:")
            example = data[0]
            print(json.dumps(example, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 