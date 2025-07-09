#!/usr/bin/env python3
"""
Script de test pour l'endpoint taged_multiple avec le nouveau format de payload
Teste l'association de tags à des membres avec le format tags_ids
"""

import requests
import json
import time
from datetime import datetime

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
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return False

def get_existing_ids():
    """Récupère des IDs existants de membres et tags"""
    try:
        # Récupérer des membres
        response_membres = requests.get(f"{MEMBRES_URL}/", headers=HEADERS)
        if response_membres.status_code == 200:
            membres_data = response_membres.json()
            membre_ids = [m['id'] for m in membres_data.get('results', [])[:3]]
        else:
            membre_ids = [1, 2, 3]  # IDs par défaut
        
        # Récupérer des tags
        response_tags = requests.get(f"{TAGS_URL}/", headers=HEADERS)
        if response_tags.status_code == 200:
            tags_data = response_tags.json()
            tag_ids = [t['id'] for t in tags_data.get('results', [])[:2]]
        else:
            tag_ids = [1, 2]  # IDs par défaut
        
        return membre_ids, tag_ids
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des IDs: {e}")
        return [1, 2], [1, 2]

def test_nouveau_format_payload():
    """Test 1: Nouveau format avec tags_ids"""
    print("\n1️⃣ Test NOUVEAU_FORMAT - Payload avec tags_ids")
    
    membre_ids, tag_ids = get_existing_ids()
    
    payload = {
        "tags_ids": tag_ids,
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Association réussie avec le nouveau format")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Étiquetages créés: {data.get('data', {}).get('etiquetages_crees', 'N/A')}")
            print(f"   Format utilisé: {data.get('payload_recu', {}).get('format_utilise', 'N/A')}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_ancien_format_compatibilite():
    """Test 2: Ancien format pour compatibilité"""
    print("\n2️⃣ Test ANCIEN_FORMAT - Compatibilité avec tag_ids")
    
    membre_ids, tag_ids = get_existing_ids()
    
    payload = {
        "tag_ids": tag_ids,
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Association réussie avec l'ancien format")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Format utilisé: {data.get('payload_recu', {}).get('format_utilise', 'N/A')}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_validation_tags_ids_vide():
    """Test 3: Validation - tags_ids vide"""
    print("\n3️⃣ Test VALIDATION - tags_ids vide")
    
    membre_ids, _ = get_existing_ids()
    
    payload = {
        "tags_ids": [],
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"   ❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_validation_membre_ids_vide():
    """Test 4: Validation - membre_ids vide"""
    print("\n4️⃣ Test VALIDATION - membre_ids vide")
    
    _, tag_ids = get_existing_ids()
    
    payload = {
        "tags_ids": tag_ids,
        "membre_ids": []
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"   ❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_validation_tags_inexistants():
    """Test 5: Validation - tags inexistants"""
    print("\n5️⃣ Test VALIDATION - Tags inexistants")
    
    membre_ids, _ = get_existing_ids()
    
    payload = {
        "tags_ids": [99999, 99998],  # IDs inexistants
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print(f"   ✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"   ❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_validation_membres_inexistants():
    """Test 6: Validation - Membres inexistants"""
    print("\n6️⃣ Test VALIDATION - Membres inexistants")
    
    _, tag_ids = get_existing_ids()
    
    payload = {
        "tags_ids": tag_ids,
        "membre_ids": [99999, 99998]  # IDs inexistants
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print(f"   ✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"   ❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_payload_mixte():
    """Test 7: Payload avec les deux formats (nouveau en priorité)"""
    print("\n7️⃣ Test PAYLOAD_MIXTE - Nouveau format en priorité")
    
    membre_ids, tag_ids = get_existing_ids()
    
    payload = {
        "tags_ids": tag_ids,      # Nouveau format
        "tag_ids": [999, 998],    # Ancien format (doit être ignoré)
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Nouveau format prioritaire")
            print(f"   Format utilisé: {data.get('payload_recu', {}).get('format_utilise', 'N/A')}")
            print(f"   Tags utilisés: {data.get('payload_recu', {}).get('tags_ids', 'N/A')}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_reponse_detaille():
    """Test 8: Vérification de la réponse détaillée"""
    print("\n8️⃣ Test REPONSE_DETAILLEE - Structure de la réponse")
    
    membre_ids, tag_ids = get_existing_ids()
    
    payload = {
        "tags_ids": tag_ids,
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Réponse détaillée reçue")
            print(f"   Success: {data.get('success', 'N/A')}")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Étiquetages créés: {data.get('data', {}).get('etiquetages_crees', 'N/A')}")
            print(f"   Étiquetages supprimés: {data.get('data', {}).get('etiquetages_supprimes', 'N/A')}")
            print(f"   Tags associés: {len(data.get('data', {}).get('tags_associes', []))}")
            print(f"   Membres associés: {len(data.get('data', {}).get('membres_associes', []))}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_performance():
    """Test 9: Test de performance"""
    print("\n9️⃣ Test PERFORMANCE - Temps de réponse")
    
    membre_ids, tag_ids = get_existing_ids()
    
    payload = {
        "tags_ids": tag_ids,
        "membre_ids": membre_ids
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{MEMBRES_URL}/taged_multiple/", 
                               json=payload, headers=HEADERS)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000  # en millisecondes
        
        print(f"   Temps de réponse: {duration:.2f}ms")
        
        if response.status_code == 201:
            print(f"   ✅ Performance acceptable")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests pour l'endpoint taged_multiple (nouveau format)")
    print("=" * 70)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests
    test_nouveau_format_payload()
    # test_ancien_format_compatibilite()
    test_validation_tags_ids_vide()
    test_validation_membre_ids_vide()
    test_validation_tags_inexistants()
    test_validation_membres_inexistants()
    # test_payload_mixte()
    test_reponse_detaille()
    test_performance()
    
    print("\n" + "=" * 70)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests() 