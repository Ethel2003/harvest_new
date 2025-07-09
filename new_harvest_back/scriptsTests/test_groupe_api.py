#!/usr/bin/env python3
"""
Script de test pour les endpoints API du modèle Groupe
Teste toutes les fonctionnalités CRUD et les actions personnalisées
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

def test_create_groupe():
    """Test de création d'un nouveau groupe"""
    print("\n🔧 Test de création d'un groupe...")
    
    groupe_data = {
        "nom": "Groupe Test",
        "description": "Description du groupe de test",
        "color": "2",
        "critere": 2  # Nécessite un critère existant
    }
    
    try:
        response = requests.post(f"{BASE_URL}/groupes/", json=groupe_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response groupe create: {response.json()}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Groupe créé avec succès")
            print(f"ID: {data['data']['id']}")
            return data["data"]["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_create_multiple_groupes():
    """Test de création de plusieurs groupes"""
    print("\n📝 Test de création de plusieurs groupes...")
    
    groupes_data = [
        	{
		"nom" : "FR Admirable",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Agneau de Dieu",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Alpha",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Amen",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Le Fidèle",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Fils de David",
		"description" : None,
		"color" : "1",
		"critere" : 2        
	},
	{
		"nom" : "FR Lion de la tribu de Juda",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Oméga",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Parakletos",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Prince de paix",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Le Rocher",
		"description" : None,
		"color" : "1",
		"critere" : 2
	},
	{
		"nom" : "FR Le Véritable",
		"description" : None,
		"color" : "1",
		"critere" : 2
	}
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/groupes/store_multiple/", json=groupes_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response create multiple groupes: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Plusieurs groupes créées avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_get_groupes():
    """Test de récupération de la liste des groupes"""
    print("\n📋 Test de récupération de la liste des groupes...")
    
    try:
        response = requests.get(f"{BASE_URL}/groupes/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response groupes get: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} groupes récupérés")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_groupe(groupe_id):
    """Test de récupération d'un groupe spécifique"""
    print(f"\n👥 Test de récupération du groupe {groupe_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/groupes/{groupe_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get groupe by id: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Groupe récupéré avec succès")
            print(f"Nom: {data['nom']}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_update_groupe(groupe_id):
    """Test de mise à jour d'un groupe"""
    print(f"\n✏️ Test de mise à jour du groupe {groupe_id}...")
    
    update_data = {
        "description": "Description mise à jour du groupe",
        "color": "3"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/groupes/{groupe_id}/", json=update_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response update groupe: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Groupe mis à jour avec succès")
            print(f"Nouvelle description: {data['data']['description']}")
            return data["data"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_search_groupes():
    """Test de recherche de groupes"""
    print("\n🔍 Test de recherche de groupes...")
    
    try:
        # Recherche par nom
        response = requests.get(f"{BASE_URL}/groupes/?search=Test", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response search groupe: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} groupes trouvés pour 'Test'")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_ordering_groupes():
    """Test de tri des groupes"""
    print("\n📊 Test de tri des groupes...")
    
    try:
        # Tri par nom
        response = requests.get(f"{BASE_URL}/groupes/?ordering=nom", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response ordering groupe: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} groupes triés par nom")
            
        # Tri par date de création (plus récent en premier)
        response = requests.get(f"{BASE_URL}/groupes/?ordering=-created_at", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} groupes triés par date de création")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_insert_membre_to_groupe(groupe_id):
    """Test d'ajout d'un membre à un groupe"""
    print(f"\n👤 Test d'ajout d'un membre au groupe {groupe_id}...")
    
    # D'abord récupérer un membre existant
    try:
        membres_response = requests.get(f"{BASE_URL}/membres/", headers=HEADERS)
        if membres_response.status_code == 200:
            membres_data = membres_response.json()
            if membres_data['results']:
                membre_id = membres_data['results'][0]['id']
                
                insert_data = {"membre_id": membre_id}
                
                response = requests.post(f"{BASE_URL}/groupes/{groupe_id}/insert_membre/", 
                                       json=insert_data, headers=HEADERS)
                print(f"Status: {response.status_code}")
                print(f"Response insert membre: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Membre ajouté au groupe avec succès")
                else:
                    print(f"❌ Erreur: {response.text}")
            else:
                print("⚠️ Aucun membre disponible pour le test")
        else:
            print("❌ Impossible de récupérer les membres")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_remove_membre_from_groupe(groupe_id):
    """Test de retrait d'un membre d'un groupe"""
    print(f"\n👤 Test de retrait d'un membre du groupe {groupe_id}...")
    
    # D'abord récupérer un membre existant
    try:
        membres_response = requests.get(f"{BASE_URL}/membres/", headers=HEADERS)
        if membres_response.status_code == 200:
            membres_data = membres_response.json()
            if membres_data['results']:
                membre_id = membres_data['results'][0]['id']
                
                remove_data = {"membre_id": membre_id}
                
                response = requests.post(f"{BASE_URL}/groupes/{groupe_id}/remove_membre/", 
                                       json=remove_data, headers=HEADERS)
                print(f"Status: {response.status_code}")
                print(f"Response remove membre: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Membre retiré du groupe avec succès")
                else:
                    print(f"❌ Erreur: {response.text}")
            else:
                print("⚠️ Aucun membre disponible pour le test")
        else:
            print("❌ Impossible de récupérer les membres")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_delete_groupe(groupe_id):
    """Test de suppression d'un groupe"""
    print(f"\n🗑️ Test de suppression du groupe {groupe_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/groupes/{groupe_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response delete groupe: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Groupe supprimé avec succès")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Groupe")
    print("=" * 50)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests CRUD de base
    groupe_id = test_create_groupe()
    if groupe_id:
        test_get_groupes()
        test_get_groupe(groupe_id)
        test_update_groupe(groupe_id)
        test_search_groupes()
        test_ordering_groupes()
        
        # Tests d'actions personnalisées
        test_insert_membre_to_groupe(groupe_id)
        test_remove_membre_from_groupe(groupe_id)
        
        # Test de suppression
        test_delete_groupe(groupe_id)
        test_create_multiple_groupes()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests() 