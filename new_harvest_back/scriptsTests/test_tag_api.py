#!/usr/bin/env python3
"""
Script de test pour les endpoints API du modèle Tag
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


def test_create_tag():
    """Test de création d'un nouveau tag"""
    print("\n🔧 Test de création d'un tag...")

    tag_data = {
        "name": "Tag Test"
    }

    try:
        response = requests.post(f"{BASE_URL}/tags/", json=tag_data, headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response tag create: {response.json()}")

        if response.status_code == 201:
            data = response.json()
            print("✅ Tag créé avec succès")
            print(f"ID: {data['data']['id']}")
            return data["data"]["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_get_tags():
    """Test de récupération de la liste des tags"""
    print("\n📋 Test de récupération de la liste des tags...")

    try:
        response = requests.get(f"{BASE_URL}/tags/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response tags get: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} tags récupérés")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_get_tag(tag_id):
    """Test de récupération d'un tag spécifique"""
    print(f"\n🏷️ Test de récupération du tag {tag_id}...")

    try:
        response = requests.get(f"{BASE_URL}/tags/{tag_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get tag by id: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Tag récupéré avec succès")
            print(f"Name: {data['name']}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_update_tag(tag_id):
    """Test de mise à jour d'un tag"""
    print(f"\n✏️ Test de mise à jour du tag {tag_id}...")

    update_data = {"description": "Description mise à jour du tag", "color": "2"}

    try:
        response = requests.patch(
            f"{BASE_URL}/tags/{tag_id}/", json=update_data, headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        print(f"Response update tag: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Tag mis à jour avec succès")
            print(f"Nouvelle description: {data['data']['description']}")
            return data["data"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_search_tags():
    """Test de recherche de tags"""
    print("\n🔍 Test de recherche de tags...")

    try:
        # Recherche par libellé
        response = requests.get(f"{BASE_URL}/tags/?search=Test", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response search tag: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} tags trouvés pour 'Test'")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_ordering_tags():
    """Test de tri des tags"""
    print("\n📊 Test de tri des tags...")

    try:
        # Tri par name
        response = requests.get(f"{BASE_URL}/tags/?ordering=name", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response ordering tag: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} tags triés par name")


    except Exception as e:
        print(f"❌ Exception: {e}")


def test_filter_tags_by_color():
    """Test de filtrage des tags par couleur"""
    print("\n🎨 Test de filtrage des tags par couleur...")

    try:
        # Filtre par couleur
        response = requests.get(f"{BASE_URL}/tags/?color=1", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response filter tag by color: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} tags trouvés pour la couleur 1")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_create_multiple_tags():
    """Test de création de plusieurs tags"""
    print("\n📝 Test de création de plusieurs tags...")

    tags_data = [
        {"name": "Khayil"},
        {"name": "Khefale"},
        {"name": "Seignors"},
        {"name": "Chef de famille"},
        {"name": "Missionnaire"},
        {"name": "Leader"},
        {"name": "Référent"},
        {"name": "STAR"},
        {"name": "AP"},
        {"name": "Pasteur"},
        {"name": "Eunice"},
        {"name": "Abigaël"},
        {"name": "Anne"},
        {"name": "Esther"},
        {"name": "Assistant Evangéliste (AE)"},
        {"name": "Prédicateur"},
        {"name": "Modérateur"},
        {"name": "Conducteur de prière"},
        {"name": "Phillipe"},
        {"name": "Intelligence artificielle"},
        {"name": "Jeune Prodige"},
        {"name": "Parle en langues"},
        {"name": "Dimeur"},
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/tags/store_multiple/", json=tags_data, headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        print(f"Response create multiple tags: {response.json()}")

        if response.status_code == 201:
            print("✅ Plusieurs tags créés avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_delete_tag(tag_id):
    """Test de suppression d'un tag"""
    print(f"\n🗑️ Test de suppression du tag {tag_id}...")

    try:
        response = requests.delete(f"{BASE_URL}/tags/{tag_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response delete tag: {response.json()}")

        if response.status_code == 200:
            print("✅ Tag supprimé avec succès")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Tag")
    print("=" * 50)

    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return

    # Tests CRUD de base
    tag_id = test_create_tag()
    if tag_id:
        test_get_tags()
        test_get_tag(tag_id)
        test_update_tag(tag_id)
        test_search_tags()
        test_ordering_tags()
        test_filter_tags_by_color()

        # Test de suppression
        test_delete_tag(tag_id)

    # Test de création multiple
    test_create_multiple_tags()

    print("\n" + "=" * 50)
    print("✅ Tests terminés !")


if __name__ == "__main__":
    run_all_tests()
