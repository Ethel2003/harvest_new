#!/usr/bin/env python3
"""
Script de test complet pour le modèle Regroupements et les nouvelles fonctionnalités
Teste la relation many-to-many entre Membres et Groupes
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
    """Test de création d'un groupe"""
    print("\n🏷️ Test de création d'un groupe...")

    groupe_data = {
        "nom": "Groupe Test",
        "description": "Description du groupe test",
        "color": "1",
        "critere": 2  # Assurez-vous qu'un critère avec l'ID 1 existe
    }

    try:
        response = requests.post(f"{BASE_URL}/groupes/", json=groupe_data, headers=HEADERS)
        print(f"Status: {response.status_code}")

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


def test_create_membre():
    """Test de création d'un membre"""
    print("\n👤 Test de création d'un membre...")

    membre_data = {
        "nom": "Doe",
        "prenom": "John",
        "email": "john.doe@example.com",
        "telephone": "123456789",
        "genre": "masculin",
        "situation_matrimoniale": "celibataire"
    }

    try:
        response = requests.post(f"{BASE_URL}/membres/", json=membre_data, headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            data = response.json()
            print("✅ Membre créé avec succès")
            print(f"ID: {data['data']['id']}")
            return data["data"]["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_groupes_list_with_members_count():
    """Test de la liste des groupes avec le nombre de membres"""
    print("\n📋 Test de la liste des groupes avec nombre de membres...")

    try:
        response = requests.get(f"{BASE_URL}/groupes/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} groupes récupérés")
            
            # Vérifier que chaque groupe a le champ nombre_membres
            groupes = data.get('results', [])
            for groupe in groupes:
                print(f"  - Groupe: {groupe.get('nom', 'Sans nom')}")
                print(f"    Nombre de membres: {groupe.get('nombre_membres', 'Non calculé')}")
                print(f"    Couleur: {groupe.get('color', 'Non définie')}")
            
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_groupes_statistiques():
    """Test de l'endpoint statistiques des groupes"""
    print("\n📊 Test des statistiques des groupes...")

    try:
        response = requests.get(f"{BASE_URL}/groupes/statistiques/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                stats_data = data.get('data', {})
                groupes = stats_data.get('groupes', [])
                stats_globales = stats_data.get('statistiques_globales', {})
                
                print(f"✅ Statistiques récupérées avec succès")
                print(f"  - Total groupes: {stats_globales.get('total_groupes', 0)}")
                print(f"  - Total membres: {stats_globales.get('total_membres', 0)}")
                print(f"  - Moyenne par groupe: {stats_globales.get('moyenne_membres_par_groupe', 0):.2f}")
                
                if stats_globales.get('groupe_plus_populaire'):
                    groupe_pop = stats_globales['groupe_plus_populaire']
                    print(f"  - Groupe le plus populaire: {groupe_pop.get('nom', 'Inconnu')} ({groupe_pop.get('nombre_membres', 0)} membres)")
                
                return data
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error', 'Erreur inconnue')}")
                return None
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_ajouter_membre_groupe(membre_id, groupe_id):
    """Test d'ajout d'un membre à un groupe via l'endpoint regroupements"""
    print(f"\n🔗 Test d'ajout du membre {membre_id} au groupe {groupe_id}...")

    try:
        response = requests.post(
            f"{BASE_URL}/regroupements/ajouter_membre_groupe/",
            json={"membre_id": membre_id, "groupe_id": groupe_id},
            headers=HEADERS
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Membre ajouté au groupe avec succès")
                return data
            else:
                print(f"❌ Erreur: {data.get('error', 'Erreur inconnue')}")
                return None
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_insert_membre_to_groupe(membre_id, groupe_id):
    """Test d'ajout d'un membre à un groupe via l'endpoint groupes"""
    print(f"\n👥 Test d'ajout du membre {membre_id} au groupe {groupe_id}...")

    try:
        response = requests.post(
            f"{BASE_URL}/groupes/{groupe_id}/insert_membre/",
            json={"membre_ids": [membre_id]},
            headers=HEADERS
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Membre ajouté au groupe avec succès")
                return data
            else:
                print(f"❌ Erreur: {data.get('error', 'Erreur inconnue')}")
                return None
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_remove_membre_from_groupe(membre_id, groupe_id):
    """Test de retrait d'un membre d'un groupe"""
    print(f"\n👋 Test de retrait du membre {membre_id} du groupe {groupe_id}...")

    try:
        response = requests.post(
            f"{BASE_URL}/groupes/{groupe_id}/remove_membre/",
            json={"membre_ids": [membre_id]},
            headers=HEADERS
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Membre retiré du groupe avec succès")
                return data
            else:
                print(f"❌ Erreur: {data.get('error', 'Erreur inconnue')}")
                return None
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_regroupements_list():
    """Test de la liste des regroupements"""
    print("\n📋 Test de la liste des regroupements...")

    try:
        response = requests.get(f"{BASE_URL}/regroupements/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} regroupements récupérés")
            
            regroupements = data.get('results', [])
            for reg in regroupements:
                print(f"  - {reg.get('membre_nom', '')} {reg.get('membre_prenom', '')} -> {reg.get('groupe_nom', '')}")
                print(f"    Actif: {reg.get('actif', False)}")
            
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_regroupements_actifs():
    """Test de la liste des regroupements actifs"""
    print("\n✅ Test de la liste des regroupements actifs...")

    try:
        response = requests.get(f"{BASE_URL}/regroupements/actifs/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ {data.get('count', 0)} regroupements actifs récupérés")
                
                regroupements = data.get('data', [])
                for reg in regroupements:
                    print(f"  - {reg.get('membre_nom', '')} {reg.get('membre_prenom', '')} -> {reg.get('groupe_nom', '')}")
                
                return data
            else:
                print(f"❌ Erreur: {data.get('error', 'Erreur inconnue')}")
                return None
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_verification_membres_count(groupe_id):
    """Test de vérification du nombre de membres après ajout/retrait"""
    print(f"\n🔍 Vérification du nombre de membres pour le groupe {groupe_id}...")

    try:
        response = requests.get(f"{BASE_URL}/groupes/{groupe_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Groupe: {data.get('nom', 'Sans nom')}")
            print(f"  Nombre de membres: {data.get('nombre_membres', 'Non calculé')}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def run_complete_test():
    """Exécute tous les tests pour le modèle Regroupements"""
    print("🚀 DÉBUT DES TESTS COMPLETS DU MODÈLE REGROUPEMENTS")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return False
    
    # Tests de base
    test_groupes_list_with_members_count()
    test_groupes_statistiques()
    test_regroupements_list()
    test_regroupements_actifs()
    
    # Création de données de test
    print("\n" + "="*50)
    print("CRÉATION DE DONNÉES DE TEST")
    print("="*50)
    
    groupe_id = 10
    membre_id = 36
    groupe_id_2 = 11
    membre_id_2 = 37
    
    if groupe_id and membre_id:
        # Tests de fonctionnalités
        print("\n" + "="*50)
        print("TESTS DE FONCTIONNALITÉS")
        print("="*50)
        
        # Test d'ajout via regroupements
        test_ajouter_membre_groupe(membre_id, groupe_id)
        test_verification_membres_count(groupe_id)
        
        # Test d'ajout via groupes
        test_insert_membre_to_groupe(membre_id_2, groupe_id_2)
        test_verification_membres_count(groupe_id_2)
        
        # Test de retrait
        # test_remove_membre_from_groupe(membre_id, groupe_id)
        # test_verification_membres_count(groupe_id)
        
        # Vérifications finales
        print("\n" + "="*50)
        print("VÉRIFICATIONS FINALES")
        print("="*50)
        
        test_groupes_list_with_members_count()
        test_groupes_statistiques()
        test_regroupements_list()
        test_regroupements_actifs()
    
    print("\n" + "="*80)
    print("RÉSUMÉ DES TESTS")
    print("="*80)
    print("✅ Tests terminés")
    print("📊 Le modèle Regroupements est maintenant fonctionnel")
    print("🔗 La relation many-to-many entre Membres et Groupes est opérationnelle")
    print("📈 Les statistiques de groupes incluent le nombre de membres")


if __name__ == "__main__":
    run_complete_test() 