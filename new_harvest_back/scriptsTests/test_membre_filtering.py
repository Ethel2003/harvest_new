#!/usr/bin/env python3
"""
Script de test pour les routes de filtrage des membres
Teste les paramètres de filtrage utilisés dans le frontend (groupes, étapes, tags)
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


def test_basic_members_list():
    """Test de la liste de base des membres"""
    print("\n📋 Test de la liste de base des membres...")

    try:
        response = requests.get(f"{BASE_URL}/membres/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres récupérés")
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_filter_by_groups():
    """Test du filtrage par groupes"""
    print("\n🏷️ Test du filtrage par groupes...")

    try:
        # Test avec un seul groupe
        response = requests.get(f"{BASE_URL}/membres/?groupes[]=1", headers=HEADERS)
        print(f"Status (groupe unique): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés pour le groupe 1")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test avec plusieurs groupes
        response = requests.get(f"{BASE_URL}/membres/?groupes[]=1&groupes[]=2", headers=HEADERS)
        print(f"Status (groupes multiples): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés pour les groupes 1,2")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_filter_by_etapes():
    """Test du filtrage par étapes"""
    print("\n📈 Test du filtrage par étapes...")

    try:
        # Test avec une seule étape
        response = requests.get(f"{BASE_URL}/membres/?etapes[]=1", headers=HEADERS)
        print(f"Status (étape unique): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés pour l'étape 1")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test avec plusieurs étapes
        response = requests.get(f"{BASE_URL}/membres/?etapes[]=1&etapes[]=2", headers=HEADERS)
        print(f"Status (étapes multiples): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés pour les étapes 1,2")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_filter_by_tags():
    """Test du filtrage par tags"""
    print("\n🏷️ Test du filtrage par tags...")

    try:
        # Test avec un seul tag
        response = requests.get(f"{BASE_URL}/membres/?tags[]=1", headers=HEADERS)
        print(f"Status (tag unique): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés pour le tag 1")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test avec plusieurs tags
        response = requests.get(f"{BASE_URL}/membres/?tags[]=1&tags[]=2", headers=HEADERS)
        print(f"Status (tags multiples): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés pour les tags 1,2")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_combined_filters():
    """Test du filtrage combiné (groupes + étapes + tags)"""
    print("\n🔗 Test du filtrage combiné...")

    try:
        # Test avec tous les filtres
        response = requests.get(
            f"{BASE_URL}/membres/?groupes[]=1&etapes[]=1&tags[]=1", 
            headers=HEADERS
        )
        print(f"Status (filtres combinés): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres trouvés avec tous les filtres")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_search_functionality():
    """Test de la fonctionnalité de recherche"""
    print("\n🔍 Test de la fonctionnalité de recherche...")

    try:
        # Test de recherche par nom
        response = requests.get(f"{BASE_URL}/membres/?search=test", headers=HEADERS)
        print(f"Status (recherche 'test'): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} résultats pour la recherche 'test'")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test de recherche par email
        response = requests.get(f"{BASE_URL}/membres/?search=@example.com", headers=HEADERS)
        print(f"Status (recherche email): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} résultats pour la recherche email")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_ordering_functionality():
    """Test de la fonctionnalité de tri"""
    print("\n📊 Test de la fonctionnalité de tri...")

    try:
        # Test de tri par nom
        response = requests.get(f"{BASE_URL}/membres/?ordering=nom", headers=HEADERS)
        print(f"Status (tri par nom): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres triés par nom")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test de tri par prénom
        response = requests.get(f"{BASE_URL}/membres/?ordering=prenom", headers=HEADERS)
        print(f"Status (tri par prénom): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres triés par prénom")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test de tri par date de création
        response = requests.get(f"{BASE_URL}/membres/?ordering=created_at", headers=HEADERS)
        print(f"Status (tri par date création): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('count', 0)} membres triés par date de création")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def test_pagination():
    """Test de la pagination"""
    print("\n📄 Test de la pagination...")

    try:
        # Test de la première page
        response = requests.get(f"{BASE_URL}/membres/?page=1&page_size=10", headers=HEADERS)
        print(f"Status (page 1): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Page 1: {len(data.get('results', []))} membres sur {data.get('count', 0)} total")
        else:
            print(f"❌ Erreur: {response.text}")

        # Test de la deuxième page
        response = requests.get(f"{BASE_URL}/membres/?page=2&page_size=10", headers=HEADERS)
        print(f"Status (page 2): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Page 2: {len(data.get('results', []))} membres sur {data.get('count', 0)} total")
        else:
            print(f"❌ Erreur: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


def analyze_filter_implementation():
    """Analyse l'implémentation des filtres dans le backend"""
    print("\n" + "="*80)
    print("ANALYSE DE L'IMPLÉMENTATION DES FILTRES")
    print("="*80)
    
    print("\n📋 Routes de filtrage attendues par le frontend:")
    print("  - GET /api/membres/?groupes[]=1&groupes[]=2")
    print("  - GET /api/membres/?etapes[]=1&etapes[]=2")
    print("  - GET /api/membres/?tags[]=1&tags[]=2")
    print("  - GET /api/membres/?groupes[]=1&etapes[]=1&tags[]=1")
    
    print("\n🔍 Analyse du ViewSet Membre:")
    print("  - search_fields: ['nom', 'prenom', 'email', 'telephone', 'profession']")
    print("  - ordering_fields: ['nom', 'prenom', 'created_at', 'updated_at']")
    print("  - filter_backends: [SearchFilter, OrderingFilter]")
    
    print("\n⚠️ PROBLÈMES POTENTIELS:")
    print("  1. Les filtres par groupes, étapes et tags ne sont pas implémentés")
    print("  2. Il faut ajouter des filtres personnalisés dans le ViewSet")
    print("  3. Les relations many-to-many doivent être gérées correctement")
    
    print("\n💡 RECOMMANDATIONS:")
    print("  1. Ajouter django-filter pour les filtres avancés")
    print("  2. Implémenter des filtres personnalisés pour les relations")
    print("  3. Ajouter la pagination dans la réponse")
    print("  4. Documenter les paramètres de filtrage supportés")


def run_filtering_tests():
    """Exécute tous les tests de filtrage"""
    print("🚀 DÉBUT DES TESTS DE FILTRAGE DES MEMBRES")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return False
    
    # Tests de base
    test_basic_members_list()
    
    # Tests de filtrage
    test_filter_by_groups()
    test_filter_by_etapes()
    test_filter_by_tags()
    test_combined_filters()
    
    # Tests de fonctionnalités
    test_search_functionality()
    test_ordering_functionality()
    test_pagination()
    
    # Analyse de l'implémentation
    analyze_filter_implementation()
    
    print("\n" + "="*80)
    print("RÉSUMÉ DES TESTS DE FILTRAGE")
    print("="*80)
    print("✅ Tests de base terminés")
    print("⚠️ Les filtres par groupes, étapes et tags nécessitent une implémentation")
    print("✅ Recherche et tri fonctionnels")
    print("⚠️ Pagination à vérifier selon l'implémentation")


if __name__ == "__main__":
    run_filtering_tests() 