#!/usr/bin/env python3
"""
Script de test pour les endpoints API du modèle Critère
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

def test_create_critere():
    """Test de création d'un nouveau critère"""
    print("\n🔧 Test de création d'un critère...")
    
    critere_data = {
        "libelle": "Critère Test",
        "description": "Description du critère de test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/criteres/", json=critere_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response critere create: {response.json()}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Critère créé avec succès")
            print(f"ID: {data['data']['id']}")
            return data["data"]["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_criteres():
    """Test de récupération de la liste des critères"""
    print("\n📋 Test de récupération de la liste des critères...")
    
    try:
        response = requests.get(f"{BASE_URL}/criteres/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response criteres get: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} critères récupérés")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_critere(critere_id):
    """Test de récupération d'un critère spécifique"""
    print(f"\n🎯 Test de récupération du critère {critere_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/criteres/{critere_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get critere by id: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Critère récupéré avec succès")
            print(f"Libellé: {data['libelle']}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_update_critere(critere_id):
    """Test de mise à jour d'un critère"""
    print(f"\n✏️ Test de mise à jour du critère {critere_id}...")
    
    update_data = {
        "description": "Description mise à jour du critère"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/criteres/{critere_id}/", json=update_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response update critere: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Critère mis à jour avec succès")
            print(f"Nouvelle description: {data['data']['description']}")
            return data["data"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_search_criteres():
    """Test de recherche de critères"""
    print("\n🔍 Test de recherche de critères...")
    
    try:
        # Recherche par libellé
        response = requests.get(f"{BASE_URL}/criteres/?search=Test", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response search critere: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} critères trouvés pour 'Test'")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_ordering_criteres():
    """Test de tri des critères"""
    print("\n📊 Test de tri des critères...")
    
    try:
        # Tri par libellé
        response = requests.get(f"{BASE_URL}/criteres/?ordering=libelle", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response ordering critere: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} critères triés par libellé")
            
        # Tri par description
        response = requests.get(f"{BASE_URL}/criteres/?ordering=description", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} critères triés par description")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_create_multiple_criteres():
    """Test de création de plusieurs critères"""
    print("\n📝 Test de création de plusieurs critères...")
    
    criteres_data = [
        {
            "libelle": "Aléatoire",
            "description": "Premier critère"
        },
        {
            "libelle": "Critères démographiques",
            "description": "Deuxième critère"
        },
        {
            "libelle": "Portes d'influence d'une nation",
            "description": "Troisième critère"
        }
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/criteres/store_multiple/", json=criteres_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response create multiple criteres: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Plusieurs critères créés avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_get_critere_groupes(critere_id):
    """Test de récupération des groupes d'un critère"""
    print(f"\n👥 Test de récupération des groupes du critère {critere_id}...")
    
    try:
        # Récupérer les groupes qui utilisent ce critère
        response = requests.get(f"{BASE_URL}/groupes/?critere={critere_id}", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get critere groupes: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} groupes trouvés pour ce critère")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_delete_critere(critere_id):
    """Test de suppression d'un critère"""
    print(f"\n🗑️ Test de suppression du critère {critere_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/criteres/{critere_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response delete critere: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Critère supprimé avec succès")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_critere_validation():
    """Test de validation des données du critère"""
    print("\n✅ Test de validation des données...")
    
    # Test avec libellé vide
    invalid_data = {
        "libelle": "",
        "description": "Description test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/criteres/", json=invalid_data, headers=HEADERS)
        print(f"Status validation libellé vide: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Validation correcte - libellé vide rejeté")
        else:
            print("⚠️ Validation inattendue pour libellé vide")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test avec libellé trop long
    invalid_data = {
        "libelle": "A" * 300,  # Plus de 255 caractères
        "description": "Description test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/criteres/", json=invalid_data, headers=HEADERS)
        print(f"Status validation libellé trop long: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Validation correcte - libellé trop long rejeté")
        else:
            print("⚠️ Validation inattendue pour libellé trop long")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_critere_relationships():
    """Test des relations du critère avec d'autres modèles"""
    print("\n🔗 Test des relations du critère...")
    
    try:
        # Créer un critère pour les tests
        critere_data = {
            "libelle": "Critère Relations Test",
            "description": "Critère pour tester les relations"
        }
        
        response = requests.post(f"{BASE_URL}/criteres/", json=critere_data, headers=HEADERS)
        if response.status_code == 201:
            critere_id = response.json()["data"]["id"]
            print(f"✅ Critère créé pour les tests: {critere_id}")
            
            # Tester la création d'un groupe avec ce critère
            groupe_data = {
                "nom": "Groupe Test Relations",
                "description": "Groupe pour tester les relations avec critère",
                "color": "1",
                "critere": critere_id
            }
            
            groupe_response = requests.post(f"{BASE_URL}/groupes/", json=groupe_data, headers=HEADERS)
            if groupe_response.status_code == 201:
                groupe_id = groupe_response.json()["data"]["id"]
                print(f"✅ Groupe créé avec le critère: {groupe_id}")
                
                # Vérifier que le groupe utilise bien le critère
                groupe_get = requests.get(f"{BASE_URL}/groupes/{groupe_id}/", headers=HEADERS)
                if groupe_get.status_code == 200:
                    groupe_data = groupe_get.json()
                    if groupe_data["critere"] == critere_id:
                        print("✅ Relation critère-groupe vérifiée")
                    else:
                        print("❌ Problème avec la relation critère-groupe")
                
                # Nettoyer le groupe créé
                requests.delete(f"{BASE_URL}/groupes/{groupe_id}/", headers=HEADERS)
            
            # Nettoyer le critère créé
            requests.delete(f"{BASE_URL}/criteres/{critere_id}/", headers=HEADERS)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Critère")
    print("=" * 50)
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests de validation
    test_critere_validation()
    
    # Tests CRUD de base
    critere_id = test_create_critere()
    if critere_id:
        test_get_criteres()
        test_get_critere(critere_id)
        test_update_critere(critere_id)
        test_search_criteres()
        test_ordering_criteres()
        test_get_critere_groupes(critere_id)
        
        # Test de suppression
        test_delete_critere(critere_id)
    
    # Test de création multiple
    test_create_multiple_criteres()
    
    # Test des relations
    test_critere_relationships()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    run_all_tests()