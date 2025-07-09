#!/usr/bin/env python3
"""
Script de test pour les endpoints API du modèle Departement
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

def test_create_departement():
    """Test de création d'un nouveau département"""
    print("\n🔧 Test de création d'un département...")
    
    departement_data = {
        "nom": "Département Test",
        "description": "Description du département de test",
        "code": "DT001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/departements/", json=departement_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response departement create: {response.json()}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Département créé avec succès")
            print(f"ID: {data['data']['id']}")
            return data["data"]["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_departements():
    """Test de récupération de la liste des départements"""
    print("\n📋 Test de récupération de la liste des départements...")
    
    try:
        response = requests.get(f"{BASE_URL}/departements/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response departements get: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} départements récupérés")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_departement(departement_id):
    """Test de récupération d'un département spécifique"""
    print(f"\n🏢 Test de récupération du département {departement_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/departements/{departement_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get departement by id: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Département récupéré avec succès")
            print(f"Nom: {data['nom']}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_update_departement(departement_id):
    """Test de mise à jour d'un département"""
    print(f"\n✏️ Test de mise à jour du département {departement_id}...")
    
    update_data = {
        "description": "Description mise à jour du département",
        "code": "DT002"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/departements/{departement_id}/", json=update_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response update departement: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Département mis à jour avec succès")
            print(f"Nouvelle description: {data['data']['description']}")
            return data["data"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_search_departements():
    """Test de recherche de départements"""
    print("\n🔍 Test de recherche de départements...")
    
    try:
        # Recherche par nom
        response = requests.get(f"{BASE_URL}/departements/?search=Test", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response search departement: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} départements trouvés pour 'Test'")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_ordering_departements():
    """Test de tri des départements"""
    print("\n📊 Test de tri des départements...")
    
    try:
        # Tri par nom
        response = requests.get(f"{BASE_URL}/departements/?ordering=nom", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response ordering departement: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} départements triés par nom")
            
        # Tri par code
        response = requests.get(f"{BASE_URL}/departements/?ordering=code", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} départements triés par code")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_filter_departements_by_code():
    """Test de filtrage des départements par code"""
    print("\n🔢 Test de filtrage des départements par code...")
    
    try:
        # Filtre par code
        response = requests.get(f"{BASE_URL}/departements/?code=DT001", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response filter departement by code: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} départements trouvés pour le code DT001")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_create_multiple_departements():
    """Test de création de plusieurs départements"""
    print("\n📝 Test de création de plusieurs départements...")
    
    departements_data = [
        {
		"nom" : "Accueil",
		"mission" : "Voluptates culpa voluptatem praesentium iusto.",
		"color" : "yellow",
	},
	{
		"nom" : "Intégration",
		"mission" : "Sit quibusdam quia itaque non sed.",
		"color" : "blue",
	},
	{
		"nom" : "Entretien",
		"mission" : "Officiis saepe commodi nostrum rerum est.",
		"color" : "neon",
	},
	{
		"nom" : "Audiovisuel",
		"mission" : "Qui quae amet et repellat.",
		"color" : "brown",
	},
	{
		"nom" : "Chorale",
		"mission" : "Facilis repudiandae sed est maiores quisquam ut autem.",
		"color" : "blue",
	},
	{
		"nom" : "Coordination",
		"mission" : "Dicta ducimus a saepe fugiat optio optio.",
		"color" : "grey",
	},
	{
		"nom" : "Communication",
		"mission" : "Expedita illum tempore minima nulla est sapiente aut.",
		"color" : "warning",
	},
	{
		"nom" : "MiFI",
		"mission" : "Veritatis dolorem quos voluptas non similique et harum.",
		"color" : "primary",
	},
	{
		"nom" : "MFI",
		"mission" : "Voluptatem commodi sint soluta et.",
		"color" : "info",
	},
	{
		"nom" : "MHI",
		"mission" : "In est ut consectetur occaecati et nulla ut.",
		"color" : "yellow",
	},
	{
		"nom" : "Santé divine",
		"mission" : None,
		"color" : "info",
	},
	{
		"nom" : "Conciergerie",
		"mission" : None,
		"color" : "purple",
	},
	{
		"nom" : "DSIIT",
		"mission" : None,
		"color" : "brown",
	}
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/departements/store_multiple/", json=departements_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response create multiple departements: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Plusieurs départements créés avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_get_departement_membres(departement_id):
    """Test de récupération des membres d'un département"""
    print(f"\n👥 Test de récupération des membres du département {departement_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/departements/{departement_id}/membres/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get departement membres: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} membres trouvés dans le département")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_delete_departement(departement_id):
    """Test de suppression d'un département"""
    print(f"\n🗑️ Test de suppression du département {departement_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/departements/{departement_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response delete departement: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Département supprimé avec succès")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Departement")
    print("=" * 50)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests CRUD de base
    departement_id = test_create_departement()
    if departement_id:
        test_get_departements()
        test_get_departement(departement_id)
        test_update_departement(departement_id)
        test_search_departements()
        test_ordering_departements()
        test_filter_departements_by_code()
        test_get_departement_membres(departement_id)
        
        # Test de suppression
        test_delete_departement(departement_id)
    
    # Test de création multiple
    test_create_multiple_departements()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests() 