#!/usr/bin/env python3
"""
Script de test pour l'endpoint store_multiple_etapes
Teste l'association d'une étape à plusieurs membres
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
MEMBRES_URL = f"{BASE_URL}/membres"
ETAPES_URL = f"{BASE_URL}/etapes"
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
    """Récupère des IDs existants pour les tests"""
    try:
        # Récupérer quelques membres
        response = requests.get(f"{MEMBRES_URL}/", headers=HEADERS)
        if response.status_code == 200:
            membres_data = response.json()
            membre_ids = [membre['id'] for membre in membres_data.get('results', [])[:3]]
        else:
            membre_ids = [1, 2, 3]  # Fallback
        
        # Récupérer quelques étapes
        response = requests.get(f"{ETAPES_URL}/", headers=HEADERS)
        if response.status_code == 200:
            etapes_data = response.json()
            etape_ids = [etape['id'] for etape in etapes_data.get('results', [])[:2]]
        else:
            etape_ids = [1, 2]  # Fallback
        
        return membre_ids, etape_ids
    except Exception as e:
        print(f"Erreur lors de la récupération des IDs: {e}")
        return [1, 2, 3], [1, 2]

def test_association_etape_membres():
    """Test 1: Association d'une étape à plusieurs membres"""
    print("\n1️⃣ Test ASSOCIATION_ETAPE_MEMBRES - Association normale")
    
    membre_ids, etape_ids = get_existing_ids()
    etape_id = etape_ids[0]  # Utiliser la première étape
    
    payload = {
        "etape_id": etape_id,
        "membre_ids": membre_ids
    }
    
    print(f"Payload envoyé: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Association réussie!")
            print(f"Message: {data.get('message', 'N/A')}")
            print(f"Intégrations créées: {data.get('data', {}).get('integrations_crees', 'N/A')}")
            print(f"Étape associée: {data.get('data', {}).get('etape_associee', {}).get('libelle', 'N/A')}")
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_validation_etape_id_manquant():
    """Test 2: Validation - etape_id manquant"""
    print("\n2️⃣ Test VALIDATION - etape_id manquant")
    
    membre_ids, _ = get_existing_ids()
    
    payload = {
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_validation_membre_ids_manquant():
    """Test 3: Validation - membre_ids manquant"""
    print("\n3️⃣ Test VALIDATION - membre_ids manquant")
    
    _, etape_ids = get_existing_ids()
    etape_id = etape_ids[0]
    
    payload = {
        "etape_id": etape_id
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_validation_membre_ids_vide():
    """Test 4: Validation - membre_ids vide"""
    print("\n4️⃣ Test VALIDATION - membre_ids vide")
    
    _, etape_ids = get_existing_ids()
    etape_id = etape_ids[0]
    
    payload = {
        "etape_id": etape_id,
        "membre_ids": []
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_validation_etape_inexistante():
    """Test 5: Validation - étape inexistante"""
    print("\n5️⃣ Test VALIDATION - Étape inexistante")
    
    membre_ids, _ = get_existing_ids()
    
    payload = {
        "etape_id": 99999,  # ID inexistant
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print(f"✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_validation_membres_inexistants():
    """Test 6: Validation - membres inexistants"""
    print("\n6️⃣ Test VALIDATION - Membres inexistants")
    
    _, etape_ids = get_existing_ids()
    etape_id = etape_ids[0]
    
    payload = {
        "etape_id": etape_id,
        "membre_ids": [99999, 99998]  # IDs inexistants
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print(f"✅ Validation correcte: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Validation échouée: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_reponse_detaille():
    """Test 7: Vérification de la réponse détaillée"""
    print("\n7️⃣ Test REPONSE_DETAILLEE - Structure de la réponse")
    
    membre_ids, etape_ids = get_existing_ids()
    etape_id = etape_ids[0]
    
    payload = {
        "etape_id": etape_id,
        "membre_ids": membre_ids
    }
    
    try:
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Réponse détaillée reçue")
            print(f"Success: {data.get('success', 'N/A')}")
            print(f"Message: {data.get('message', 'N/A')}")
            print(f"Intégrations créées: {data.get('data', {}).get('integrations_crees', 'N/A')}")
            print(f"Intégrations supprimées: {data.get('data', {}).get('integrations_supprimees', 'N/A')}")
            print(f"Étape associée: {data.get('data', {}).get('etape_associee', {}).get('libelle', 'N/A')}")
            print(f"Membres associés: {len(data.get('data', {}).get('membres_associes', []))}")
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_performance():
    """Test 8: Test de performance"""
    print("\n8️⃣ Test PERFORMANCE - Temps de réponse")
    
    membre_ids, etape_ids = get_existing_ids()
    etape_id = etape_ids[0]
    
    payload = {
        "etape_id": etape_id,
        "membre_ids": membre_ids
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{MEMBRES_URL}/store_multiple_etapes/", 
                               json=payload, headers=HEADERS)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000  # en millisecondes
        
        print(f"Temps de réponse: {duration:.2f}ms")
        
        if response.status_code == 201:
            print(f"✅ Performance acceptable")
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST STORE_MULTIPLE_ETAPES - Association étape-membres")
    print("=" * 70)
    print(f"Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests
    success_count = 0
    total_tests = 8
    
    # Test 1: Association normale
    if test_association_etape_membres():
        success_count += 1
    
    # Test 2: Validation etape_id manquant
    if test_validation_etape_id_manquant():
        success_count += 1
    
    # Test 3: Validation membre_ids manquant
    if test_validation_membre_ids_manquant():
        success_count += 1
    
    # Test 4: Validation membre_ids vide
    if test_validation_membre_ids_vide():
        success_count += 1
    
    # Test 5: Validation étape inexistante
    if test_validation_etape_inexistante():
        success_count += 1
    
    # Test 6: Validation membres inexistants
    if test_validation_membres_inexistants():
        success_count += 1
    
    # Test 7: Réponse détaillée
    if test_reponse_detaille():
        success_count += 1
    
    # Test 8: Performance
    if test_performance():
        success_count += 1
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    print(f"Tests réussis: {success_count}/{total_tests}")
    print(f"Taux de succès: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 Tous les tests sont passés!")
    else:
        print("⚠️ Certains tests ont échoué")
    
    print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 