#!/usr/bin/env python3
"""
Script rapide pour vérifier l'état de l'endpoint taged_multiple
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
MEMBRES_URL = f"{BASE_URL}/membres"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

def quick_check():
    """Vérification rapide de l'endpoint"""
    print("🔍 Vérification rapide de l'endpoint taged_multiple")
    print("=" * 50)
    
    # Test 1: Vérifier si l'endpoint répond
    print("\n1️⃣ Test de réponse de l'endpoint")
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json={}, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            print("   ✅ Endpoint répond (erreur 400 attendue pour payload vide)")
            try:
                data = response.json()
                print(f"   Message d'erreur: {data.get('error', 'N/A')}")
            except:
                print("   Réponse non-JSON")
        elif response.status_code == 405:
            print("   ❌ Endpoint n'existe pas (Méthode non autorisée)")
        else:
            print(f"   ⚠️ Status inattendu: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    # Test 2: Vérifier l'authentification
    print("\n2️⃣ Test d'authentification")
    try:
        login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            token = data["data"]["token"]
            print("   ✅ Authentification réussie")
            
            # Test avec token
            headers_with_auth = HEADERS.copy()
            headers_with_auth["Authorization"] = f"Token {token}"
            
            response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                                   json={}, headers=headers_with_auth)
            print(f"   Status avec auth: {response.status_code}")
            
            if response.status_code == 400:
                try:
                    data = response.json()
                    print(f"   Message d'erreur: {data.get('error', 'N/A')}")
                except:
                    print("   Réponse non-JSON")
        else:
            print(f"   ❌ Échec de l'authentification: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Vérifier les routes disponibles
    print("\n3️⃣ Vérification des routes")
    try:
        response = requests.get(f"{MEMBRES_URL}/", headers=HEADERS)
        print(f"   Status liste membres: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Endpoint membres accessible")
        else:
            print(f"   ❌ Endpoint membres inaccessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Vérification terminée")

if __name__ == "__main__":
    quick_check() 