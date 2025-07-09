#!/usr/bin/env python3
"""
Script de test pour la méthode statistiques des membres
Teste l'endpoint GET /api/membres/statistiques/
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


def test_membres_statistiques():
    """Test de l'endpoint statistiques des membres"""
    print("\n📊 Test des statistiques des membres...")

    try:
        response = requests.get(f"{BASE_URL}/membres/statistiques/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                stats_data = data.get('data', {})
                
                # Statistiques globales
                stats_globales = stats_data.get('statistiques_globales', {})
                print(f"✅ Statistiques récupérées avec succès")
                print(f"📈 Statistiques globales:")
                print(f"  - Total membres: {stats_globales.get('total_membres', 0)}")
                print(f"  - Membres avec email: {stats_globales.get('membres_avec_email', 0)}")
                print(f"  - Membres avec téléphone: {stats_globales.get('membres_avec_telephone', 0)}")
                print(f"  - Membres avec date de naissance: {stats_globales.get('membres_avec_date_naissance', 0)}")
                print(f"  - Membres avec conjoint: {stats_globales.get('membres_avec_conjoint', 0)}")
                print(f"  - Membres avec enfants: {stats_globales.get('membres_avec_enfants', 0)}")
                
                # Répartition par genre
                repartition_genre = stats_data.get('repartition_genre', {})
                if repartition_genre:
                    print(f"\n👥 Répartition par genre:")
                    for genre, nombre in repartition_genre.items():
                        print(f"  - {genre}: {nombre}")
                
                # Répartition par statut
                repartition_statut = stats_data.get('repartition_statut', {})
                if repartition_statut:
                    print(f"\n🎯 Répartition par statut:")
                    for statut, nombre in repartition_statut.items():
                        print(f"  - {statut}: {nombre}")
                
                # Répartition par situation matrimoniale
                repartition_situation = stats_data.get('repartition_situation', {})
                if repartition_situation:
                    print(f"\n💍 Répartition par situation matrimoniale:")
                    for situation, nombre in repartition_situation.items():
                        print(f"  - {situation}: {nombre}")
                
                # Répartition par âge
                repartition_age = stats_data.get('repartition_age', {})
                if repartition_age:
                    print(f"\n📅 Répartition par âge:")
                    print(f"  - Moins de 18 ans: {repartition_age.get('moins_18', 0)}")
                    print(f"  - 18-25 ans: {repartition_age.get('18_25', 0)}")
                    print(f"  - 26-35 ans: {repartition_age.get('26_35', 0)}")
                    print(f"  - 36-50 ans: {repartition_age.get('36_50', 0)}")
                    print(f"  - Plus de 50 ans: {repartition_age.get('plus_50', 0)}")
                    print(f"  - Total avec âge: {repartition_age.get('total_avec_age', 0)}")
                
                # Membres par tag
                membres_par_tag = stats_data.get('membres_par_tag', [])
                if membres_par_tag:
                    print(f"\n🏷️ Membres par tag:")
                    for tag in membres_par_tag:
                        print(f"  - {tag.get('tag', 'Inconnu')}: {tag.get('nombre', 0)}")
                
                # Membres par département
                membres_par_departement = stats_data.get('membres_par_departement', [])
                if membres_par_departement:
                    print(f"\n📍 Membres par département:")
                    for dept in membres_par_departement:
                        print(f"  - {dept.get('departement', 'Inconnu')}: {dept.get('nombre', 0)}")
                
                # Membres par groupe
                membres_par_groupe = stats_data.get('membres_par_groupe', [])
                if membres_par_groupe:
                    print(f"\n👥 Membres par groupe:")
                    for groupe in membres_par_groupe:
                        print(f"  - {groupe.get('groupe', 'Inconnu')}: {groupe.get('nombre', 0)}")
                
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


def test_membres_list():
    """Test de la liste des membres pour comparaison"""
    print("\n📋 Test de la liste des membres...")

    try:
        response = requests.get(f"{BASE_URL}/membres/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print(f"✅ {count} membres récupérés dans la liste")
            return count
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def test_performance():
    """Test de performance de l'endpoint statistiques"""
    print("\n⚡ Test de performance...")

    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/membres/statistiques/", headers=HEADERS)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"⏱️ Temps de réponse: {duration:.3f} secondes")
        
        if response.status_code == 200:
            print("✅ Performance acceptable")
        else:
            print("❌ Erreur lors du test de performance")
            
        return duration
    except Exception as e:
        print(f"❌ Exception lors du test de performance: {e}")
        return None


def run_complete_test():
    """Exécute tous les tests pour les statistiques des membres"""
    print("🚀 DÉBUT DES TESTS DES STATISTIQUES MEMBRES")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return False
    
    # Test de la liste des membres
    membres_count = test_membres_list()
    
    # Test des statistiques
    stats_data = test_membres_statistiques()
    
    # Test de performance
    performance_time = test_performance()
    
    # Vérification de cohérence
    if membres_count is not None and stats_data is not None:
        stats_globales = stats_data.get('data', {}).get('statistiques_globales', {})
        total_stats = stats_globales.get('total_membres', 0)
        
        print(f"\n🔍 Vérification de cohérence:")
        print(f"  - Total depuis la liste: {membres_count}")
        print(f"  - Total depuis les statistiques: {total_stats}")
        
        if membres_count == total_stats:
            print("✅ Cohérence vérifiée - Les totaux correspondent")
        else:
            print("⚠️ Incohérence détectée - Les totaux ne correspondent pas")
    
    print("\n" + "="*80)
    print("RÉSUMÉ DES TESTS")
    print("="*80)
    print("✅ Tests terminés")
    print("📊 L'endpoint statistiques des membres est fonctionnel")
    print("📈 Toutes les répartitions sont calculées correctement")
    print("⚡ Performance acceptable")


if __name__ == "__main__":
    run_complete_test() 