#!/usr/bin/env python3
"""
Script de test simple pour l'enregistrement multiple
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

def login():
    """Authentification"""
    login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            token = data["data"]["token"]
            HEADERS["Authorization"] = f"Token {token}"
            print("✅ Authentification réussie")
            return True
        else:
            print(f"❌ Échec de l'authentification: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return False

def test_create_multiple_membres():
    """Test d'enregistrement multiple"""
    print("\n👥 Test d'enregistrement multiple...")
    
    # Charger les données corrigées
    with open('membres_202506271515_fixed.json', 'r', encoding='utf-8') as f:
        membres_data = json.load(f)
    
    print(f"📊 Nombre de membres à traiter: {len(membres_data)}")
    
    # Traiter par lots de 20
    batch_size = 20
    success_count = 0
    
    for i in range(0, len(membres_data), batch_size):
        batch = membres_data[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        print(f"\n🔄 Lot {batch_num} ({len(batch)} membres)")
        
        try:
            response = requests.post(
                f"{BASE_URL}/membres/store_multiple/", 
                json=batch, 
                headers=HEADERS,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                success_count += len(batch)
                print(f"✅ Lot {batch_num} réussi")
            else:
                print(f"❌ Erreur lot {batch_num}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception lot {batch_num}: {e}")
    
    print(f"\n📊 Résultat: {success_count}/{len(membres_data)} membres créés")

if __name__ == "__main__":
    if login():
        test_create_multiple_membres()
    else:
        print("❌ Impossible de continuer sans authentification.")
