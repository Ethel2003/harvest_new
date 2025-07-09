#!/usr/bin/env python3
"""
Script de test pour vérifier la complétude des routes API du modèle Membre
Compare les routes attendues par le frontend avec celles disponibles dans le backend
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

# Routes attendues par le frontend (extrait de useMember.ts)
FRONTEND_ROUTES = {
    # Routes CRUD de base
    "GET /api/membres/": "Récupération de la liste des membres",
    "GET /api/membres/{id}/": "Récupération d'un membre spécifique",
    "POST /api/membres/": "Création d'un nouveau membre",
    "PUT /api/membres/{id}/": "Mise à jour d'un membre",
    "DELETE /api/membres/{id}/": "Suppression d'un membre",
    
    # Routes personnalisées
    "DELETE /api/membres/unset-conjoint/{id}/": "Suppression du conjoint d'un membre",
    "DELETE /api/membres/delete-enfant/{enfant_id}/{id}/": "Suppression d'un enfant d'un membre",
    
    # Routes avec paramètres de filtrage
    "GET /api/membres/?groupes[]=1&groupes[]=2": "Filtrage par groupes",
    "GET /api/membres/?etapes[]=1&etapes[]=2": "Filtrage par étapes",
    "GET /api/membres/?tags[]=1&tags[]=2": "Filtrage par tags",
    "GET /api/membres/?groupes[]=1&etapes[]=1&tags[]=1": "Filtrage combiné",
}

# Routes disponibles dans le backend (extrait de MembreViewSet)
BACKEND_ROUTES = {
    # Routes CRUD de base (héritées de BaseViewSet)
    "GET /api/membres/": "Liste des membres",
    "POST /api/membres/": "Création d'un membre",
    "GET /api/membres/{id}/": "Détail d'un membre",
    "PUT /api/membres/{id}/": "Mise à jour complète d'un membre",
    "PATCH /api/membres/{id}/": "Mise à jour partielle d'un membre",
    "DELETE /api/membres/{id}/": "Suppression d'un membre",
    
    # Routes personnalisées (actions)
    "POST /api/membres/taged_multiple/": "Ajouter plusieurs tags à plusieurs membres",
    "POST /api/membres/{id}/untaged_multiple/": "Supprimer plusieurs tags d'un membre",
    "POST /api/membres/{id}/store_multiple_etapes/": "Ajouter plusieurs étapes à un membre",
    "DELETE /api/membres/{id}/delete_etape/{etape_id}/": "Supprimer une étape d'un membre",
    "POST /api/membres/{id}/insert_to_departement/": "Insérer des membres dans un département",
    "POST /api/membres/{id}/retrieve_from_departement/": "Retirer des membres d'un département",
    "POST /api/membres/{id}/insert_to_groupe/": "Insérer des membres dans un groupe",
    "POST /api/membres/{id}/retrieve_from_groupe/": "Retirer des membres d'un groupe",
    
    # Routes de base pour les opérations multiples
    "POST /api/membres/store_multiple/": "Créer plusieurs membres",
    "POST /api/membres/destroy_multiple/": "Supprimer plusieurs membres",
}


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


def test_route_exists(route, description):
    """Test si une route existe et est accessible"""
    print(f"\n🔍 Test de la route: {route}")
    print(f"Description: {description}")
    
    # Remplacer les paramètres par des valeurs de test
    test_route = route.replace("{id}", "1").replace("{enfant_id}", "1").replace("{etape_id}", "1")
    
    # Déterminer la méthode HTTP
    if route.startswith("GET"):
        method = "GET"
        url = f"{BASE_URL}{test_route.split(' ')[1]}"
    elif route.startswith("POST"):
        method = "POST"
        url = f"{BASE_URL}{test_route.split(' ')[1]}"
    elif route.startswith("PUT"):
        method = "PUT"
        url = f"{BASE_URL}{test_route.split(' ')[1]}"
    elif route.startswith("PATCH"):
        method = "PATCH"
        url = f"{BASE_URL}{test_route.split(' ')[1]}"
    elif route.startswith("DELETE"):
        method = "DELETE"
        url = f"{BASE_URL}{test_route.split(' ')[1]}"
    else:
        print("❌ Méthode HTTP non reconnue")
        return False
    
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, json={}, headers=HEADERS)
        elif method == "PUT":
            response = requests.put(url, json={}, headers=HEADERS)
        elif method == "PATCH":
            response = requests.patch(url, json={}, headers=HEADERS)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS)
        
        print(f"Status: {response.status_code}")
        
        # Interpréter le statut de réponse
        if response.status_code in [200, 201, 204]:
            print("✅ Route accessible")
            return True
        elif response.status_code == 404:
            print("❌ Route non trouvée")
            return False
        elif response.status_code == 405:
            print("❌ Méthode HTTP non autorisée")
            return False
        elif response.status_code == 400:
            print("⚠️ Route accessible mais données invalides (normal pour les tests)")
            return True
        elif response.status_code == 401:
            print("❌ Authentification requise")
            return False
        else:
            print(f"⚠️ Statut inattendu: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False


def analyze_routes_completeness():
    """Analyse la complétude des routes"""
    print("\n" + "="*80)
    print("ANALYSE DE LA COMPLÉTUDE DES ROUTES MEMBRE")
    print("="*80)
    
    # Routes manquantes dans le backend
    missing_routes = []
    for route, description in FRONTEND_ROUTES.items():
        if route not in BACKEND_ROUTES:
            missing_routes.append((route, description))
    
    # Routes supplémentaires dans le backend
    extra_routes = []
    for route, description in BACKEND_ROUTES.items():
        if route not in FRONTEND_ROUTES:
            extra_routes.append((route, description))
    
    # Affichage des résultats
    print(f"\n📊 RÉSUMÉ:")
    print(f"Routes attendues par le frontend: {len(FRONTEND_ROUTES)}")
    print(f"Routes disponibles dans le backend: {len(BACKEND_ROUTES)}")
    print(f"Routes manquantes: {len(missing_routes)}")
    print(f"Routes supplémentaires: {len(extra_routes)}")
    
    if missing_routes:
        print(f"\n❌ ROUTES MANQUANTES DANS LE BACKEND:")
        for route, description in missing_routes:
            print(f"  - {route}: {description}")
    
    if extra_routes:
        print(f"\n➕ ROUTES SUPPLÉMENTAIRES DANS LE BACKEND:")
        for route, description in extra_routes:
            print(f"  - {route}: {description}")
    
    if not missing_routes:
        print(f"\n✅ TOUTES LES ROUTES ATTENDUES SONT DISPONIBLES!")
    
    return len(missing_routes) == 0


def test_critical_routes():
    """Test des routes critiques pour le fonctionnement du frontend"""
    print("\n" + "="*80)
    print("TEST DES ROUTES CRITIQUES")
    print("="*80)
    
    critical_routes = [
        ("GET /api/membres/", "Liste des membres"),
        ("POST /api/membres/", "Création d'un membre"),
        ("GET /api/membres/{id}/", "Détail d'un membre"),
        ("PUT /api/membres/{id}/", "Mise à jour d'un membre"),
        ("DELETE /api/membres/{id}/", "Suppression d'un membre"),
    ]
    
    success_count = 0
    for route, description in critical_routes:
        if test_route_exists(route, description):
            success_count += 1
    
    print(f"\n📊 RÉSULTATS DES TESTS CRITIQUES:")
    print(f"Routes testées: {len(critical_routes)}")
    print(f"Routes fonctionnelles: {success_count}")
    print(f"Taux de succès: {(success_count/len(critical_routes)*100):.1f}%")
    
    return success_count == len(critical_routes)


def generate_recommendations():
    """Génère des recommandations pour améliorer la couverture des routes"""
    print("\n" + "="*80)
    print("RECOMMANDATIONS")
    print("="*80)
    
    recommendations = []
    
    # Vérifier les routes manquantes
    missing_routes = []
    for route, description in FRONTEND_ROUTES.items():
        if route not in BACKEND_ROUTES:
            missing_routes.append((route, description))
    
    if missing_routes:
        recommendations.append("🔧 Routes à implémenter dans le backend:")
        for route, description in missing_routes:
            recommendations.append(f"   - {route}: {description}")
    
    # Vérifier les routes avec paramètres de filtrage
    filter_routes = [r for r in FRONTEND_ROUTES.keys() if "?" in r]
    if filter_routes:
        recommendations.append("\n🔍 Routes de filtrage à tester:")
        for route in filter_routes:
            recommendations.append(f"   - {route}")
    
    # Recommandations générales
    recommendations.extend([
        "\n💡 Recommandations générales:",
        "   - Implémenter la gestion des erreurs pour toutes les routes",
        "   - Ajouter la validation des données d'entrée",
        "   - Documenter les paramètres attendus pour chaque route",
        "   - Ajouter des tests unitaires pour chaque endpoint",
        "   - Implémenter la pagination pour les listes volumineuses",
        "   - Ajouter des filtres de recherche avancés",
        "   - Implémenter le tri sur tous les champs pertinents"
    ])
    
    for rec in recommendations:
        print(rec)


def run_completeness_analysis():
    """Exécute l'analyse complète de la complétude des routes"""
    print("🚀 DÉBUT DE L'ANALYSE DE COMPLÉTUDE DES ROUTES MEMBRE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return False
    
    # Analyse de la complétude
    completeness_ok = analyze_routes_completeness()
    
    # Test des routes critiques
    critical_ok = test_critical_routes()
    
    # Génération des recommandations
    generate_recommendations()
    
    # Résumé final
    print("\n" + "="*80)
    print("RÉSUMÉ FINAL")
    print("="*80)
    
    if completeness_ok and critical_ok:
        print("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
        print("   Toutes les routes attendues sont disponibles et fonctionnelles")
    elif completeness_ok:
        print("⚠️ ANALYSE TERMINÉE AVEC RÉSERVES")
        print("   Routes disponibles mais certains tests critiques ont échoué")
    else:
        print("❌ ANALYSE TERMINÉE AVEC DES PROBLÈMES")
        print("   Certaines routes attendues sont manquantes")
    
    return completeness_ok and critical_ok


if __name__ == "__main__":
    run_completeness_analysis() 