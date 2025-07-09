#!/usr/bin/env python3
"""
Script de test final pour l'enregistrement multiple des membres
Données nettoyées et optimisées pour l'API
"""

import requests
import json
import time

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
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return False

def test_single_membre():
    """Test avec un seul membre"""
    print("\n🧪 Test avec un seul membre...")
    
    # Charger les données nettoyées
    with open('membres_202506271515_cleaned.json', 'r', encoding='utf-8') as f:
        membres_data = json.load(f)
    
    if membres_data:
        test_membre = membres_data[0]
        
        try:
            response = requests.post(
                f"{BASE_URL}/membres/", 
                json=test_membre, 
                headers=HEADERS
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                print("✅ Test avec un membre réussi")
                return True
            else:
                print(f"❌ Erreur: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    return False

def test_create_multiple_membres():
    """Test d'enregistrement multiple par lots"""
    print("\n👥 Test d'enregistrement multiple...")
    
    # Charger les données nettoyées
    with open('membres_202506271515_cleaned.json', 'r', encoding='utf-8') as f:
        membres_data = json.load(f)
    
    print(f"📊 Total de membres à traiter: {len(membres_data)}")
    
    # Diviser en lots de 30 pour éviter les timeouts
    batch_size = 30
    total_membres = len(membres_data)
    success_count = 0
    error_count = 0
    
    for i in range(0, total_membres, batch_size):
        batch = membres_data[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_membres + batch_size - 1) // batch_size
        
        print(f"\n🔄 Lot {batch_num}/{total_batches} ({len(batch)} membres)")
        
        try:
            response = requests.post(
                f"{BASE_URL}/membres/store_multiple/", 
                json=batch, 
                headers=HEADERS,
                timeout=60
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                success_count += len(batch)
                print(f"✅ Lot {batch_num} réussi")
            else:
                error_count += len(batch)
                print(f"❌ Erreur lot {batch_num}: {response.text}")
            
            # Pause entre les lots
            if i + batch_size < total_membres:
                print("⏳ Pause de 3 secondes...")
                time.sleep(3)
                
        except Exception as e:
            error_count += len(batch)
            print(f"❌ Exception lot {batch_num}: {e}")
    
    print(f"\n📊 RAPPORT FINAL")
    print("=" * 40)
    print(f"Total de membres: {total_membres}")
    print(f"Succès: {success_count}")
    print(f"Erreurs: {error_count}")
    print(f"Taux de succès: {(success_count/total_membres)*100:.1f}%")

if __name__ == "__main__":
    print("🚀 Test d'enregistrement des membres")
    print("=" * 50)
    
    if login():
        # Test avec un seul membre d'abord
        if test_single_membre():
            # Si le test simple réussit, faire l'enregistrement multiple
            test_create_multiple_membres()
        else:
            print("\n❌ Le test simple a échoué. Vérifiez le format des données.")
    else:
        print("\n❌ Impossible de continuer sans authentification.")
