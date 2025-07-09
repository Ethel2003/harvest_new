#!/usr/bin/env python3
"""
Script de test pour les endpoints API du modèle Etape
Teste toutes les fonctionnalités CRUD
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
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

def test_create_etape():
    """Test de création d'une nouvelle étape"""
    print("\n🔧 Test de création d'une étape...")
    
    etape_data = {
        "libelle": "Étape Test",
        "description": "Description de l'étape de test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/etapes/", json=etape_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response etape create: {response.json()}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Étape créée avec succès")
            print(f"ID: {data['data']['id']}")
            return data["data"]["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_etapes():
    """Test de récupération de la liste des étapes"""
    print("\n📋 Test de récupération de la liste des étapes...")
    
    try:
        response = requests.get(f"{BASE_URL}/etapes/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response etapes get: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} étapes récupérées")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_etape(etape_id):
    """Test de récupération d'une étape spécifique"""
    print(f"\n📈 Test de récupération de l'étape {etape_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/etapes/{etape_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get etape by id: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Étape récupérée avec succès")
            print(f"Libellé: {data['libelle']}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_update_etape(etape_id):
    """Test de mise à jour d'une étape"""
    print(f"\n✏️ Test de mise à jour de l'étape {etape_id}...")
    
    update_data = {
        "description": "Description mise à jour de l'étape"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/etapes/{etape_id}/", json=update_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response update etape: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Étape mise à jour avec succès")
            print(f"Nouvelle description: {data['data']['description']}")
            return data["data"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_search_etapes():
    """Test de recherche d'étapes"""
    print("\n🔍 Test de recherche d'étapes...")
    
    try:
        # Recherche par libellé
        response = requests.get(f"{BASE_URL}/etapes/?search=Test", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response search etape: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} étapes trouvées pour 'Test'")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_ordering_etapes():
    """Test de tri des étapes"""
    print("\n📊 Test de tri des étapes...")
    
    try:
        # Tri par libellé
        response = requests.get(f"{BASE_URL}/etapes/?ordering=libelle", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response ordering etape: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} étapes triées par libellé")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_create_multiple_etapes():
    """Test de création de plusieurs étapes"""
    print("\n📝 Test de création de plusieurs étapes...")
    
    etapes_data = [
        {
		"libelle" : "BDR",
		"description" : "La formation de bienvenue qui accueille les nouveaux arrivants"
	},
	{
		"libelle" : "Intégration dans une FR",
		"description" : "Le nouveau membre intègre un groupe où il sentira en famille et pourra communier avec des frères et soeurs"
	},
	{
		"libelle" : "Le PCNC",
		"description" : "Un ensemble de formation pour faire asseoir les fondements du royaume et la maturité spirituelle"
	},
	{
		"libelle" : "Le service",
		"description" : "L'intégration dans un département où le membre apprend à mettre ses dons et capacités au service de la communauté"
	}
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/etapes/store_multiple/", json=etapes_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response create multiple etapes: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Plusieurs étapes créées avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_delete_etape(etape_id):
    """Test de suppression d'une étape"""
    print(f"\n🗑️ Test de suppression de l'étape {etape_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/etapes/{etape_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response delete etape: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Étape supprimée avec succès")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Etape")
    print("=" * 50)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests CRUD de base
    etape_id = test_create_etape()
    if etape_id:
        test_get_etapes()
        test_get_etape(etape_id)
        test_update_etape(etape_id)
        test_search_etapes()
        test_ordering_etapes()
        
        # Test de suppression
        test_delete_etape(etape_id)
    
    # Test de création multiple
    test_create_multiple_etapes()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests() 