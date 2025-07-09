#!/usr/bin/env python3
"""
Script de diagnostic pour l'endpoint taged_multiple
Identifie les problèmes avec l'endpoint et les paramètres
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000/api"
MEMBRES_URL = f"{BASE_URL}/membres"
TAGS_URL = f"{BASE_URL}/tags"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Token d'authentification
AUTH_TOKEN = None

def login():
    """Authentification pour obtenir un token"""
    global AUTH_TOKEN
    
    login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        print(f"Status login: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            AUTH_TOKEN = data["data"]["token"]
            HEADERS["Authorization"] = f"Token {AUTH_TOKEN}"
            print("✅ Authentification réussie")
            return True
        else:
            print(f"❌ Échec de l'authentification: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return False

def check_endpoint_exists():
    """Vérifie si l'endpoint existe"""
    print("\n🔍 Vérification de l'existence de l'endpoint")
    
    try:
        # Test avec une requête GET pour voir si l'endpoint répond
        response = requests.get(f"{MEMBRES_URL}/taged_multiple/", headers=HEADERS)
        print(f"   GET /api/membres/taged_multiple/ - Status: {response.status_code}")
        
        # Test avec une requête POST vide
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json={}, headers=HEADERS)
        print(f"   POST /api/membres/taged_multiple/ (vide) - Status: {response.status_code}")
        
        if response.status_code == 400:
            print("   ✅ Endpoint existe et répond (erreur 400 attendue pour payload vide)")
            return True
        elif response.status_code == 405:
            print("   ❌ Endpoint n'existe pas (Méthode non autorisée)")
            return False
        else:
            print(f"   ⚠️ Endpoint répond avec un status inattendu: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification: {e}")
        return False

def get_existing_data():
    """Récupère des données existantes pour les tests"""
    print("\n📊 Récupération des données existantes")
    
    try:
        # Récupérer des membres
        response_membres = requests.get(f"{MEMBRES_URL}/", headers=HEADERS)
        print(f"   Status membres: {response_membres.status_code}")
        
        if response_membres.status_code == 200:
            membres_data = response_membres.json()
            membres = membres_data.get('results', [])
            print(f"   Membres trouvés: {len(membres)}")
            if membres:
                membre_ids = [m['id'] for m in membres[:3]]
                print(f"   IDs membres: {membre_ids}")
            else:
                membre_ids = []
                print("   ⚠️ Aucun membre trouvé")
        else:
            membre_ids = []
            print(f"   ❌ Erreur récupération membres: {response_membres.text}")
        
        # Récupérer des tags
        response_tags = requests.get(f"{TAGS_URL}/", headers=HEADERS)
        print(f"   Status tags: {response_tags.status_code}")
        
        if response_tags.status_code == 200:
            tags_data = response_tags.json()
            tags = tags_data.get('results', [])
            print(f"   Tags trouvés: {len(tags)}")
            if tags:
                tag_ids = [t['id'] for t in tags[:2]]
                print(f"   IDs tags: {tag_ids}")
            else:
                tag_ids = []
                print("   ⚠️ Aucun tag trouvé")
        else:
            tag_ids = []
            print(f"   ❌ Erreur récupération tags: {response_tags.text}")
        
        return membre_ids, tag_ids
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la récupération des données: {e}")
        return [], []

def test_payload_validation():
    """Teste différents payloads pour identifier le problème"""
    print("\n🧪 Tests de validation des payloads")
    
    membre_ids, tag_ids = get_existing_data()
    
    if not membre_ids:
        print("   ⚠️ Impossible de tester sans membres existants")
        return
    
    if not tag_ids:
        print("   ⚠️ Impossible de tester sans tags existants")
        return
    
    # Test 1: Payload vide
    print("\n   Test 1: Payload vide")
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json={}, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   Erreur: {data.get('error', 'N/A')}")
        else:
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: Payload avec tags_ids manquant
    print("\n   Test 2: Payload avec tags_ids manquant")
    try:
        payload = {"membre_ids": membre_ids}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   Erreur: {data.get('error', 'N/A')}")
        else:
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Payload avec membre_ids manquant
    print("\n   Test 3: Payload avec membre_ids manquant")
    try:
        payload = {"tags_ids": tag_ids}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   Erreur: {data.get('error', 'N/A')}")
        else:
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: Payload avec listes vides
    print("\n   Test 4: Payload avec listes vides")
    try:
        payload = {"tags_ids": [], "membre_ids": []}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   Erreur: {data.get('error', 'N/A')}")
        else:
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 5: Payload valide avec nouveau format
    print("\n   Test 5: Payload valide avec nouveau format")
    try:
        payload = {"tags_ids": tag_ids, "membre_ids": membre_ids}
        print(f"   Payload envoyé: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Succès: {data.get('message', 'N/A')}")
            print(f"   Format utilisé: {data.get('payload_recu', {}).get('format_utilise', 'N/A')}")
        elif response.status_code == 400:
            data = response.json()
            print(f"   ❌ Erreur 400: {data.get('error', 'N/A')}")
        else:
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 6: Payload valide avec ancien format
    print("\n   Test 6: Payload valide avec ancien format")
    try:
        payload = {"tag_ids": tag_ids, "membre_ids": membre_ids}
        print(f"   Payload envoyé: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Succès: {data.get('message', 'N/A')}")
            print(f"   Format utilisé: {data.get('payload_recu', {}).get('format_utilise', 'N/A')}")
        elif response.status_code == 400:
            data = response.json()
            print(f"   ❌ Erreur 400: {data.get('error', 'N/A')}")
        else:
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def test_headers():
    """Teste les headers de la requête"""
    print("\n📋 Test des headers")
    
    membre_ids, tag_ids = get_existing_data()
    
    if not membre_ids or not tag_ids:
        print("   ⚠️ Impossible de tester sans données")
        return
    
    # Test sans Content-Type
    print("\n   Test 1: Sans Content-Type")
    try:
        headers_without_content_type = HEADERS.copy()
        del headers_without_content_type['Content-Type']
        
        payload = {"tags_ids": tag_ids, "membre_ids": membre_ids}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=headers_without_content_type)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test avec Content-Type incorrect
    print("\n   Test 2: Content-Type incorrect")
    try:
        headers_wrong_content_type = HEADERS.copy()
        headers_wrong_content_type['Content-Type'] = 'text/plain'
        
        payload = {"tags_ids": tag_ids, "membre_ids": membre_ids}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               data=json.dumps(payload), headers=headers_wrong_content_type)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def test_authentication():
    """Teste l'authentification"""
    print("\n🔐 Test de l'authentification")
    
    membre_ids, tag_ids = get_existing_data()
    
    if not membre_ids or not tag_ids:
        print("   ⚠️ Impossible de tester sans données")
        return
    
    # Test sans token
    print("\n   Test 1: Sans token d'authentification")
    try:
        headers_without_auth = HEADERS.copy()
        if 'Authorization' in headers_without_auth:
            del headers_without_auth['Authorization']
        
        payload = {"tags_ids": tag_ids, "membre_ids": membre_ids}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=headers_without_auth)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test avec token invalide
    print("\n   Test 2: Token invalide")
    try:
        headers_invalid_auth = HEADERS.copy()
        headers_invalid_auth['Authorization'] = 'Token invalid_token_123'
        
        payload = {"tags_ids": tag_ids, "membre_ids": membre_ids}
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=headers_invalid_auth)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def run_diagnostic():
    """Exécute le diagnostic complet"""
    print("🔍 Diagnostic de l'endpoint taged_multiple")
    print("=" * 60)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Vérifications
    check_endpoint_exists()
    test_payload_validation()
    test_headers()
    test_authentication()
    
    print("\n" + "=" * 60)
    print("✅ Diagnostic terminé !")

if __name__ == "__main__":
    run_diagnostic() 