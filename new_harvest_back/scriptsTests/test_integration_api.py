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
INTEGRATIONS_URL = f"{BASE_URL}/integrations"
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

def test_create_integration():
    """Test 1: CREATE - Créer une nouvelle intégration"""
    print("\n1️⃣ Test CREATE - Créer une intégration")
    integration_data = {
        "membre": 1,
        "etape": 2,
        "created_at": date.today().isoformat(),
        "membership": False
    }
    
    try:
        response = requests.post(f"{INTEGRATIONS_URL}/", json=integration_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            integration_id = data['data']['id']
            test_data['integration_id'] = integration_id
            print(f"   ✅ Intégration créée avec succès (ID: {integration_id})")
            print(f"   Données: {data['data']}")
            return integration_id  # ✅ Correction : retourner l'ID
        else:
            print(f"   ❌ Échec de création: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def test_get_integrations():
    """Test 2: LIST - Lister toutes les intégrations"""
    print("\n2️⃣ Test LIST - Lister toutes les intégrations")
    try:
        response = requests.get(f"{INTEGRATIONS_URL}", headers=HEADERS)
        print(f"   Status: {response.status_code}")
            
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else len(data.get('data', []))
            print(f"   ✅ {count} intégrations récupérées")
            return True
        else:
            print(f"   ❌ Échec de listage: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_get_integration(integration_id):
    """Test 3: READ - Récupérer une intégration spécifique"""
    print(f"\n3️⃣ Test READ - Lire l'intégration {integration_id}")
    
    try:
        response = requests.get(f"{INTEGRATIONS_URL}/{integration_id}/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Intégration récupérée avec succès")
            print(f"   Données: {data}")
            return True
        else:
            print(f"   ❌ Échec de lecture: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_update_integration(integration_id):
    """Test 4: UPDATE - Mettre à jour une intégration"""
    print(f"\n4️⃣ Test UPDATE - Mettre à jour l'intégration {integration_id}")
    update_data = {
        "membership": True
    }
    
    try:
        response = requests.patch(f"{INTEGRATIONS_URL}/{integration_id}/", json=update_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Intégration mise à jour avec succès")
            print(f"   Données mises à jour: {data['data']}")
            return True
        else:
            print(f"   ❌ Échec de mise à jour: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_delete_integration(integration_id):
    """Test 5: DELETE - Supprimer une intégration"""
    print(f"\n5️⃣ Test DELETE - Supprimer l'intégration {integration_id}")
    try:
        response = requests.delete(f"{INTEGRATIONS_URL}/{integration_id}/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Intégration supprimée avec succès")
            return True
        else:
            print(f"   ❌ Échec de suppression: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_verification_integration(integration_id):
    """Test 6: VERIFICATION - Vérifier que l'intégration est supprimée"""
    print(f"\n6️⃣ Test VERIFICATION - Vérifier la suppression de l'intégration {integration_id}")
    try:
        response = requests.get(f"{INTEGRATIONS_URL}/{integration_id}/", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            print(f"   ✅ Intégration bien supprimée (404 attendu)")
            return True
        else:
            print(f"   ⚠️ Intégration encore accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_create_multiple_integrations():
    """Test 7: CREATE MULTIPLE - Créer plusieurs intégrations"""
    print("\n" + "="*60)
    print("🧪 TESTS OPÉRATIONS AVANCÉES")
    print("="*60)
    
    print("\n7️⃣ Test CREATE MULTIPLE - Créer plusieurs intégrations")
    integrations_data = [
        {
            "membre": 2,
            "etape": 4,
            "created_at": date.today().isoformat(),
            "membership": False
        },
        {
            "membre": 3,
            "etape": 3,
            "created_at": date.today().isoformat(),
            "membership": True
        },
        {
            "membre": 4,
            "etape": 2,
            "created_at": date.today().isoformat(),
            "membership": True
        },
        {
            "membre": 5,
            "etape": 5,
            "created_at": date.today().isoformat(),
            "membership": False
        },
        {
            "membre": 6,
            "etape": 4,
            "created_at": date.today().isoformat(),
            "membership": False
        },
        {
            "membre": 7,
            "etape": 3,
            "created_at": date.today().isoformat(),
            "membership": True
        }
    ]
    
    try:
        response = requests.post(f"{INTEGRATIONS_URL}/store_multiple/", json=integrations_data, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            print(f"   ✅ Intégrations multiples créées avec succès")
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
    if test_create_multiple_integrations():
        print("✅ Tests d'opérations avancées réussis")
    else:
        print("❌ Échec des tests d'opérations avancées")
    # Tests CRUD de base
    # integration_id = test_create_integration()
    
    # if integration_id:
    #     # Tests de lecture et mise à jour
    #     test_get_integrations()
    #     test_get_integration(integration_id)
    #     test_update_integration(integration_id)
        
      
        
        # Tests de suppression (optionnel - décommentez si vous voulez tester)
        # test_delete_integration(integration_id)
        # test_verification_integration(integration_id)
    # else:
    #     print("❌ Impossible de continuer sans ID d'intégration")
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests()