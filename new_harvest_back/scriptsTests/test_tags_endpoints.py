#!/usr/bin/env python3
"""
Script de test pour les nouveaux endpoints API du modèle Tag
Teste toutes les fonctionnalités avancées des tags
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
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

def test_tous_les_tags():
    """Test 1: Récupérer tous les tags"""
    print("\n1️⃣ Test TOUS_LES_TAGS - Récupérer tous les tags")
    
    try:
        response = requests.get(f"{TAGS_URL}/tous_les_tags/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['total']} tags récupérés avec succès")
            print(f"   Filtres appliqués: {data['filtres_appliques']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_tous_les_tags_avec_recherche():
    """Test 2: Récupérer tous les tags avec recherche"""
    print("\n2️⃣ Test TOUS_LES_TAGS avec recherche")
    
    try:
        response = requests.get(f"{TAGS_URL}/tous_les_tags/?search=test", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Recherche réussie: {data['total']} résultats trouvés")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_tous_les_tags_avec_membres():
    """Test 3: Récupérer tous les tags avec nombre de membres"""
    print("\n3️⃣ Test TOUS_LES_TAGS avec membres")
    
    try:
        response = requests.get(f"{TAGS_URL}/tous_les_tags/?avec_membres=true", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tags avec membres récupérés: {data['total']} tags")
            if data['data']:
                print(f"   Exemple: {data['data'][0]}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_statistiques_tags():
    """Test 4: Récupérer les statistiques des tags"""
    print("\n4️⃣ Test STATISTIQUES - Statistiques des tags")
    
    try:
        response = requests.get(f"{TAGS_URL}/statistiques/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
            print(f"   ✅ Statistiques récupérées:")
            print(f"   - Total tags: {stats['total_tags']}")
            print(f"   - Tags non utilisés: {stats['tags_non_utilises']}")
            print(f"   - Tags populaires: {len(stats['tags_populaires'])}")
            print(f"   - Répartition: {stats['repartition']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_avec_membres():
    """Test 5: Récupérer tags avec nombre de membres"""
    print("\n5️⃣ Test AVEC_MEMBRES - Tags avec nombre de membres")
    
    try:
        response = requests.get(f"{TAGS_URL}/avec_membres/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tags avec membres: {data['total']} tags")
            if data['data']:
                print(f"   Exemple: {data['data'][0]}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_avec_membres_filtres():
    """Test 6: Récupérer tags avec filtres par nombre de membres"""
    print("\n6️⃣ Test AVEC_MEMBRES avec filtres")
    
    try:
        response = requests.get(f"{TAGS_URL}/avec_membres/?min_membres=1&ordering=-nombre_membres", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tags filtrés: {data['total']} tags avec au moins 1 membre")
            print(f"   Filtres appliqués: {data['filtres_appliques']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_creer_multiple():
    """Test 7: Créer plusieurs tags en une fois"""
    print("\n7️⃣ Test CREER_MULTIPLE - Créer plusieurs tags")
    
    tags_data = {
        "tags": [
            "Tag Test 1",
            "Tag Test 2", 
            "Tag Test 3",
            "Tag Test 4",
            "Tag Test 5"
        ]
    }
    
    try:
        response = requests.post(f"{TAGS_URL}/creer_multiple/", json=tags_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Création multiple réussie:")
            print(f"   - Tags créés: {len(data['data']['tags_crees'])}")
            print(f"   - Tags existants: {data['data']['tags_existants']}")
            print(f"   - Total traités: {data['data']['total_traites']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_endpoints_standards():
    """Test 8: Endpoints CRUD standards"""
    print("\n8️⃣ Test ENDPOINTS STANDARDS - CRUD de base")
    
    # Test LIST
    try:
        response = requests.get(f"{TAGS_URL}/", headers=HEADERS)
        print(f"   Status LIST: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Liste des tags: {len(data)} tags")
            
            # Test CREATE si des tags existent
            if data:
                tag_id = data[0]['id']
                
                # Test GET ONE
                response_get = requests.get(f"{TAGS_URL}/{tag_id}/", headers=HEADERS)
                print(f"   Status GET ONE: {response_get.status_code}")
                
                if response_get.status_code == 200:
                    print(f"   ✅ Tag récupéré: {response_get.json()['data']['name']}")
                else:
                    print(f"   ❌ Échec GET ONE: {response_get.text}")
            
            return True
        else:
            print(f"   ❌ Échec LIST: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_performances():
    """Test 9: Tests de performance"""
    print("\n9️⃣ Test PERFORMANCES - Mesure des temps de réponse")
    
    endpoints = [
        f"{TAGS_URL}/tous_les_tags/",
        f"{TAGS_URL}/statistiques/",
        f"{TAGS_URL}/avec_membres/",
        f"{TAGS_URL}/"
    ]
    
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(endpoint, headers=HEADERS)
            end_time = time.time()
            
            duration = (end_time - start_time) * 1000  # en millisecondes
            
            if response.status_code == 200:
                print(f"   ✅ {endpoint.split('/')[-2]}: {duration:.2f}ms")
            else:
                print(f"   ❌ {endpoint.split('/')[-2]}: {duration:.2f}ms (Erreur {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ {endpoint.split('/')[-2]}: Erreur - {e}")

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour les nouveaux endpoints Tag")
    print("=" * 60)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests des nouveaux endpoints
    test_tous_les_tags()
    test_tous_les_tags_avec_recherche()
    test_tous_les_tags_avec_membres()
    test_statistiques_tags()
    test_avec_membres()
    test_avec_membres_filtres()
    test_creer_multiple()
    test_endpoints_standards()
    test_performances()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests() 