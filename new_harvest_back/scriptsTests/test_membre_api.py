#!/usr/bin/env python3
"""
Script de test pour les routes API du modèle Membre
Ce script teste toutes les fonctionnalités CRUD et les actions personnalisées
"""

import requests
import json
import time
from datetime import datetime, date
import uuid

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Token d'authentification (à remplacer par un vrai token)
AUTH_TOKEN = None


def login():
    """Authentification pour obtenir un token"""
    global AUTH_TOKEN

    login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}

    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        print(response.json())
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


def test_create_membre():
    """Test de création d'un nouveau membre"""
    print("\n🔧 Test de création d'un membre...")

    membre_data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "adresse": "123 Rue de la Paix",
        "ville": "Paris",
        "telephone": "+33123456789",
        "email": "jean.dupont@email.com",
        "profession": "Ingénieur",
        "nationalite": "Française",
        "color": "1",
        "genre": "masculin",
        "date_naissance": "1990-05-15",
        "situation_matrimoniale": "marie",
        "statut": "membre",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/membres/", json=membre_data, headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        print(f"Response member create : {response.json()}")

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


def test_get_membres():
    """Test de récupération de la liste des membres"""
    print("\n📋 Test de récupération de la liste des membres...")

    try:
        response = requests.get(f"{BASE_URL}/membres/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response member get : {response.json()}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} membres récupérés")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_get_membre(membre_id):
    """Test de récupération d'un membre spécifique"""
    print(f"\n👤 Test de récupération du membre {membre_id}...")

    try:
        response = requests.get(f"{BASE_URL}/membres/{membre_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response get member by id : {response.json()}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Membre récupéré avec succès")
            print(f"Nom: {data['prenom']} {data['nom']}")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_update_membre(membre_id):
    """Test de mise à jour d'un membre"""
    print(f"\n✏️ Test de mise à jour du membre {membre_id}...")

    update_data = {
        "profession": "Développeur Senior",
        "ville": "Lyon",
        "telephone": "+33456789012",
    }

    try:
        response = requests.patch(
            f"{BASE_URL}/membres/{membre_id}/", json=update_data, headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        print(f"Response update member : {response.json()}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Membre mis à jour avec succès")
            print(f"Nouvelle profession: {data['data']['profession']}")
            return data["data"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_search_membres():
    """Test de recherche de membres"""
    print("\n🔍 Test de recherche de membres...")

    try:
        # Recherche par nom
        response = requests.get(f"{BASE_URL}/membres/?search=Dupont", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response search member : {response.json()}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['count']} membres trouvés pour 'Dupont'")
        else:
            print(f"❌ Erreur: {response.text}")

        # Recherche par email
        response = requests.get(
            f"{BASE_URL}/membres/?search=jean.dupont", headers=HEADERS
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {len(data)} membres trouvés pour 'jean.dupont'")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_ordering_membres():
    """Test de tri des membres"""
    print("\n📊 Test de tri des membres...")

    try:
        # Tri par nom
        response = requests.get(f"{BASE_URL}/membres/?ordering=nom", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response ordering member : {response.json()}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {len(data)} membres triés par nom")

        # Tri par date de création (plus récent en premier)
        response = requests.get(
            f"{BASE_URL}/membres/?ordering=-created_at", headers=HEADERS
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {len(data)} membres triés par date de création")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_create_multiple_membres():
    """Test de création de plusieurs membres en une fois"""
    print("\n👥 Test de création de plusieurs membres...")

    membres_data = [
        {
            "nom": "Martin",
            "prenom": "Sophie",
            "adresse": "456 Avenue des Fleurs",
            "ville": "Marseille",
            "telephone": "+33456789012",
            "email": "sophie.martin@email.com",
            "profession": "Designer",
            "nationalite": "Française",
            "color": "2",
            "genre": "feminin",
            "date_naissance": "1988-12-03",
            "situation_matrimoniale": "celibataire",
            "statut": "inscrit",
        },
        {
            "nom": "Bernard",
            "prenom": "Pierre",
            "adresse": "789 Boulevard Central",
            "ville": "Toulouse",
            "telephone": "+33567890123",
            "email": "pierre.bernard@email.com",
            "profession": "Médecin",
            "nationalite": "Française",
            "color": "3",
            "genre": "masculin",
            "date_naissance": "1975-08-20",
            "situation_matrimoniale": "marie",
            "statut": "membre",
        },
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/membres/store_multiple/", json=membres_data, headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        print(f"Response create multiple members : {response.json()}")
        if response.status_code == 201:
            print("✅ Plusieurs membres créés avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_delete_multiple_membres():
    """Test de suppression de plusieurs membres"""
    print("\n🗑️ Test de suppression de plusieurs membres...")

    # D'abord, récupérer la liste des membres
    membres = test_get_membres()
    if membres and len(membres) >= 2:
        # Prendre les 2 derniers membres créés
        ids_to_delete = [membres[-1]["id"], membres[-2]["id"]]

        delete_data = {"ids": ids_to_delete}

        try:
            response = requests.post(
                f"{BASE_URL}/membres/destroy_multiple/",
                json=delete_data,
                headers=HEADERS,
            )
            print(f"Status: {response.status_code}")
            print(f"Response delete multiple members : {response.json()}")
            if response.status_code == 200:
                print("✅ Plusieurs membres supprimés avec succès")
            else:
                print(f"❌ Erreur: {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")


def test_membre_actions(membre_id):
    """Test des actions personnalisées sur un membre"""
    print(f"\n⚙️ Test des actions personnalisées sur le membre {membre_id}...")

    # Test d'ajout de tags multiples (nécessite d'abord des tags)
    print("\n🏷️ Test d'ajout de tags multiples...")
    tag_data = {
        "tag_ids": [1, 2],  # Remplacez par de vrais IDs de tags
        "membre_ids": [membre_id],
    }

    try:
        response = requests.post(
            f"{BASE_URL}/membres/taged_multiple/", json=tag_data, headers=HEADERS
        )
        print(f"Status: {response.status_code}")
        print(f"Response membre actions : {response.json()}")
        if response.status_code == 200:
            print("✅ Tags ajoutés avec succès")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_delete_membre(membre_id):
    """Test de suppression d'un membre"""
    print(f"\n🗑️ Test de suppression du membre {membre_id}...")

    try:
        response = requests.delete(f"{BASE_URL}/membres/{membre_id}/", headers=HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response delete member : {response.json()}")
        if response.status_code == 200:
            print("✅ Membre supprimé avec succès")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Membre")
    print("=" * 50)

    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return

    # Tests CRUD de base
    # membre_id = test_create_membre()
    # if membre_id:
    #     test_get_membres()
    #     test_get_membre(membre_id)
    #     test_update_membre(membre_id)
    #     test_search_membres()
    #     test_ordering_membres()

    #     # Tests d'actions personnalisées
    #     test_membre_actions(membre_id)

    #     # Tests de suppression
    #     test_delete_membre(membre_id)

    # Tests de création/suppression multiple
    test_create_multiple_membres()
    # test_delete_multiple_membres()

    print("\n" + "=" * 50)
    print("✅ Tests terminés !")


if __name__ == "__main__":
    run_all_tests()
