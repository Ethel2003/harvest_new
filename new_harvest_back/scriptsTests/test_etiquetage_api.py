#!/usr/bin/env python3
"""
Script de test pour les endpoints API du modèle Integration
Teste toutes les fonctionnalités CRUD
"""

import requests
import json
import time
from datetime import date

# Configuration
BASE_URL = "http://localhost:8000/api"
ETIQUETAGES_URL = f"{BASE_URL}/etiquetages"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Token d'authentification
AUTH_TOKEN = None

test_data = {}

def login():
    """Authentification pour obtenir un token"""
    global AUTH_TOKEN
    
    login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        print(f"Status login: {response.status_code}")
        print(f"Response login: {response.json()}")
        
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

def test_create_etiquetage():
    """Test 1: CREATE - Créer une nouvelle etiquetage"""
    print("\n1️⃣ Test CREATE - Créer une etiquetage")
    etiquetage_data = {
        "membre": 2,
        "tag": 2
    }
    
    try:
        response = requests.post(f"{ETIQUETAGES_URL}/", json=etiquetage_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            etiquetage_id = data['data']['id']
            test_data['etiquetage_id'] = etiquetage_id
            print(f"   ✅ Etiquetage créée avec succès (ID: {etiquetage_id})")
            print(f"   Données: {data['data']}")
            return etiquetage_id  # ✅ Correction : retourner l'ID
        else:
            print(f"   ❌ Échec de création: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def test_get_etiquetages():
    """Test 2: LIST - Lister toutes les etiquetages"""
    print("\n2️⃣ Test LIST - Lister toutes les etiquetages")
    try:
        response = requests.get(f"{ETIQUETAGES_URL}", headers=HEADERS)
        print(f"   Status: {response.status_code}")
            
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else len(data.get('data', []))
            print(f"   ✅ {count} etiquetages récupérées")
            return True
        else:
            print(f"   ❌ Échec de listage: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_get_etiquetage(etiquetage_id):
    """Test 3: READ - Récupérer une etiquetage spécifique"""
    print(f"\n3️⃣ Test READ - Lire l'etiquetage {etiquetage_id}")
    
    try:
        response = requests.get(f"{ETIQUETAGES_URL}/{etiquetage_id}/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Etiquetage récupérée avec succès")
            print(f"   Données: {data}")
            return True
        else:
            print(f"   ❌ Échec de lecture: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_update_etiquetage(etiquetage_id):
    """Test 4: UPDATE - Mettre à jour une etiquetage"""
    print(f"\n4️⃣ Test UPDATE - Mettre à jour l'etiquetage {etiquetage_id}")
    update_data = {
        "tag": 15  # Changer pour le deuxième tag
    }
    try:
        response = requests.patch(f"{ETIQUETAGES_URL}/{etiquetage_id}/", json=update_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Etiquetage mise à jour avec succès")
            print(f"   Données mises à jour: {data['data']}")
            return True
        else:
            print(f"   ❌ Échec de mise à jour: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_delete_etiquetage(etiquetage_id):
    """Test 5: DELETE - Supprimer une etiquetage"""
    print(f"\n5️⃣ Test DELETE - Supprimer l'etiquetage {etiquetage_id}")
    try:
        response = requests.delete(f"{ETIQUETAGES_URL}/{etiquetage_id}/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Etiquetage supprimée avec succès")
            return True
        else:
            print(f"   ❌ Échec de suppression: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_verification_etiquetage(etiquetage_id):
    """Test 6: VERIFICATION - Vérifier que l'etiquetage est supprimée"""
    print(f"\n6️⃣ Test VERIFICATION - Vérifier la suppression de l'etiquetage {etiquetage_id}")
    try:
        response = requests.get(f"{ETIQUETAGES_URL}/{etiquetage_id}/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            print(f"   ✅ Etiquetage bien supprimée (404 attendu)")
            return True
        else:
            print(f"   ⚠️ Etiquetage encore accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_create_multiple_etiquetages():
    """Test 7: CREATE MULTIPLE - Créer plusieurs etiquetages"""
    print("\n" + "="*60)
    print("🧪 TESTS OPÉRATIONS AVANCÉES")
    print("="*60)
    
    print("\n7️⃣ Test CREATE MULTIPLE - Créer plusieurs etiquetages")
    etiquetages_data = [
            {
                "membre": 3,
                "tag": 3
            },
            {
                "membre": 4,
                "tag": 2
            }
        ]
    try:
        response = requests.post(f"{ETIQUETAGES_URL}/store_multiple/", json=etiquetages_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            print(f"   ✅ Etiquetages multiples créées avec succès")
            return True
        else:
            print(f"   ❌ Échec de création multiple: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Integration")
    print("=" * 60)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests d'opérations avancées
    if test_create_multiple_etiquetages():
        print("✅ Tests d'opérations avancées réussis")
    else:
        print("❌ Échec des tests d'opérations avancées")
    # Tests CRUD de base
    # etiquetage_id = test_create_etiquetage()
    test_get_etiquetages()
    # if etiquetage_id:
    #     # Tests de lecture et mise à jour
    #     test_get_etiquetages()
    #     test_get_etiquetage(etiquetage_id)
    #     test_update_etiquetage(etiquetage_id)
        
      
        
    #     # Tests de suppression (optionnel - décommentez si vous voulez tester)
    #     # test_delete_integration(integration_id)
    #     # test_verification_integration(integration_id)
    # else:
    #     print("❌ Impossible de continuer sans ID d'intégration")
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests()