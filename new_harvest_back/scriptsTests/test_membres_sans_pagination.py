#!/usr/bin/env python3
"""
Script de test pour les nouveaux endpoints API des membres sans pagination
Teste les endpoints pour récupérer l'intégralité des données
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
MEMBRES_URL = f"{BASE_URL}/membres"
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

def test_tous_les_membres():
    """Test 1: Récupérer tous les membres sans pagination"""
    print("\n1️⃣ Test TOUS_LES_MEMBRES - Récupérer tous les membres")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['total']} membres récupérés avec succès")
            print(f"   Filtres appliqués: {data['filtres_appliques']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_tous_les_membres_avec_recherche():
    """Test 2: Récupérer tous les membres avec recherche"""
    print("\n2️⃣ Test TOUS_LES_MEMBRES avec recherche")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/?search=test", headers=HEADERS)
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

def test_tous_les_membres_avec_relations():
    """Test 3: Récupérer tous les membres avec relations"""
    print("\n3️⃣ Test TOUS_LES_MEMBRES avec relations")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/?avec_relations=true", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Membres avec relations récupérés: {data['total']} membres")
            if data['data']:
                membre_exemple = data['data'][0]
                print(f"   Exemple de membre avec relations:")
                print(f"   - ID: {membre_exemple.get('id')}")
                print(f"   - Nom: {membre_exemple.get('nom')}")
                print(f"   - Groupes: {len(membre_exemple.get('groupes', []))}")
                print(f"   - Étapes: {len(membre_exemple.get('etapes', []))}")
                print(f"   - Tags: {len(membre_exemple.get('tags', []))}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_tous_les_membres_avec_tri():
    """Test 4: Récupérer tous les membres avec tri"""
    print("\n4️⃣ Test TOUS_LES_MEMBRES avec tri")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/?ordering=-created_at", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tri par date de création décroissante: {data['total']} membres")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_membres_simples():
    """Test 5: Récupérer une liste simplifiée des membres"""
    print("\n5️⃣ Test MEMBRES_SIMPLES - Liste simplifiée")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/membres_simples/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Membres simples récupérés: {data['total']} membres")
            if data['data']:
                membre_exemple = data['data'][0]
                print(f"   Exemple de membre simple:")
                print(f"   - ID: {membre_exemple.get('id')}")
                print(f"   - Nom complet: {membre_exemple.get('nom_complet')}")
                print(f"   - Email: {membre_exemple.get('email')}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_membres_simples_avec_recherche():
    """Test 6: Récupérer membres simples avec recherche"""
    print("\n6️⃣ Test MEMBRES_SIMPLES avec recherche")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/membres_simples/?search=jean", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Recherche dans membres simples: {data['total']} résultats")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_filtrage_par_groupes():
    """Test 7: Filtrage par groupes"""
    print("\n7️⃣ Test filtrage par groupes")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/?groupes[]=1&groupes[]=2", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Filtrage par groupes: {data['total']} membres trouvés")
            print(f"   Groupes filtrés: {data['filtres_appliques']['groupes']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_filtrage_par_etapes():
    """Test 8: Filtrage par étapes"""
    print("\n8️⃣ Test filtrage par étapes")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/?etapes[]=1", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Filtrage par étapes: {data['total']} membres trouvés")
            print(f"   Étapes filtrées: {data['filtres_appliques']['etapes']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_filtrage_par_tags():
    """Test 9: Filtrage par tags"""
    print("\n9️⃣ Test filtrage par tags")
    
    try:
        response = requests.get(f"{MEMBRES_URL}/tous_les_membres/?tags[]=1&tags[]=2", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Filtrage par tags: {data['total']} membres trouvés")
            print(f"   Tags filtrés: {data['filtres_appliques']['tags']}")
            return True
        else:
            print(f"   ❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_performances():
    """Test 10: Tests de performance"""
    print("\n🔟 Test PERFORMANCES - Mesure des temps de réponse")
    
    endpoints = [
        f"{MEMBRES_URL}/tous_les_membres/",
        f"{MEMBRES_URL}/tous_les_membres/?avec_relations=true",
        f"{MEMBRES_URL}/membres_simples/",
        f"{MEMBRES_URL}/"  # Endpoint avec pagination pour comparaison
    ]
    
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(endpoint, headers=HEADERS)
            end_time = time.time()
            
            duration = (end_time - start_time) * 1000  # en millisecondes
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', len(data) if isinstance(data, list) else 0)
                print(f"   ✅ {endpoint.split('/')[-2]}: {duration:.2f}ms ({total} membres)")
            else:
                print(f"   ❌ {endpoint.split('/')[-2]}: {duration:.2f}ms (Erreur {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ {endpoint.split('/')[-2]}: Erreur - {e}")

def test_comparaison_pagination():
    """Test 11: Comparaison avec pagination"""
    print("\n1️⃣1️⃣ Test COMPARAISON - Avec vs Sans pagination")
    
    try:
        # Test avec pagination (endpoint standard)
        start_time = time.time()
        response_paginated = requests.get(f"{MEMBRES_URL}/?page_size=100", headers=HEADERS)
        end_time = time.time()
        duration_paginated = (end_time - start_time) * 1000
        
        # Test sans pagination (nouvel endpoint)
        start_time = time.time()
        response_all = requests.get(f"{MEMBRES_URL}/tous_les_membres/", headers=HEADERS)
        end_time = time.time()
        duration_all = (end_time - start_time) * 1000
        
        if response_paginated.status_code == 200 and response_all.status_code == 200:
            data_paginated = response_paginated.json()
            data_all = response_all.json()
            
            print(f"   📊 Comparaison des performances:")
            print(f"   - Avec pagination: {duration_paginated:.2f}ms ({len(data_paginated)} membres)")
            print(f"   - Sans pagination: {duration_all:.2f}ms ({data_all['total']} membres)")
            print(f"   - Différence: {abs(duration_all - duration_paginated):.2f}ms")
            
            return True
        else:
            print(f"   ❌ Échec de la comparaison")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour les membres sans pagination")
    print("=" * 70)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests des nouveaux endpoints
    test_tous_les_membres()
    test_tous_les_membres_avec_recherche()
    test_tous_les_membres_avec_relations()
    test_tous_les_membres_avec_tri()
    test_membres_simples()
    test_membres_simples_avec_recherche()
    test_filtrage_par_groupes()
    test_filtrage_par_etapes()
    test_filtrage_par_tags()
    test_performances()
    test_comparaison_pagination()
    
    print("\n" + "=" * 70)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests() 