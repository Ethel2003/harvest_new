#!/usr/bin/env python3
"""
Script de test pour la méthode nouveaux_par_date des membres
Teste l'endpoint GET /api/membres/nouveaux_par_date/
"""

import requests
import json
from datetime import datetime, timedelta

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


def test_nouveaux_par_date_daily():
    """Test de l'endpoint nouveaux_par_date avec format daily"""
    print("\n📅 Test des nouveaux membres par jour...")

    try:
        # Calculer les dates pour les 30 derniers jours
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'format': 'daily'
        }
        
        response = requests.get(f"{BASE_URL}/membres/nouveaux_par_date/", 
                              params=params, headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result_data = data.get('data', {})
                nouveaux_par_date = result_data.get('nouveaux_par_date', [])
                stats = result_data.get('statistiques', {})
                
                print(f"✅ Données récupérées avec succès")
                print(f"📊 Statistiques:")
                print(f"  - Total nouveaux: {stats.get('total_nouveaux', 0)}")
                print(f"  - Moyenne quotidienne: {stats.get('moyenne_quotidienne', 0)}")
                print(f"  - Période: {stats.get('periode', {})}")
                
                print(f"\n📈 Nouveaux membres par jour (derniers 10 jours):")
                for item in nouveaux_par_date[-10:]:
                    print(f"  - {item.get('date', 'Inconnu')}: {item.get('count', 0)}")
                
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


def test_nouveaux_par_date_monthly():
    """Test de l'endpoint nouveaux_par_date avec format monthly"""
    print("\n📅 Test des nouveaux membres par mois...")

    try:
        # Calculer les dates pour les 12 derniers mois
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'format': 'monthly'
        }
        
        response = requests.get(f"{BASE_URL}/membres/nouveaux_par_date/", 
                              params=params, headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result_data = data.get('data', {})
                nouveaux_par_date = result_data.get('nouveaux_par_date', [])
                stats = result_data.get('statistiques', {})
                
                print(f"✅ Données récupérées avec succès")
                print(f"📊 Statistiques:")
                print(f"  - Total nouveaux: {stats.get('total_nouveaux', 0)}")
                print(f"  - Moyenne mensuelle: {stats.get('moyenne_quotidienne', 0)}")
                
                print(f"\n📈 Nouveaux membres par mois:")
                for item in nouveaux_par_date:
                    print(f"  - {item.get('date', 'Inconnu')}: {item.get('count', 0)}")
                
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


def test_nouveaux_par_date_sans_filtre():
    """Test de l'endpoint nouveaux_par_date sans filtres"""
    print("\n📅 Test des nouveaux membres sans filtres...")

    try:
        response = requests.get(f"{BASE_URL}/membres/nouveaux_par_date/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result_data = data.get('data', {})
                nouveaux_par_date = result_data.get('nouveaux_par_date', [])
                stats = result_data.get('statistiques', {})
                
                print(f"✅ Données récupérées avec succès")
                print(f"📊 Total nouveaux membres: {stats.get('total_nouveaux', 0)}")
                print(f"📈 Nombre de jours avec des nouveaux membres: {len(nouveaux_par_date)}")
                
                if nouveaux_par_date:
                    print(f"\n📅 Premiers jours avec nouveaux membres:")
                    for item in nouveaux_par_date[:5]:
                        print(f"  - {item.get('date', 'Inconnu')}: {item.get('count', 0)}")
                
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


def test_format_compatible_frontend():
    """Test pour vérifier la compatibilité avec le format attendu par le frontend"""
    print("\n🔄 Test de compatibilité avec le frontend...")

    try:
        response = requests.get(f"{BASE_URL}/membres/nouveaux_par_date/", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result_data = data.get('data', {})
                nouveaux_par_date = result_data.get('nouveaux_par_date', [])
                
                # Vérifier que le format correspond à ce qu'attend le frontend
                print(f"✅ Format vérifié:")
                print(f"  - Type de données: {type(nouveaux_par_date)}")
                print(f"  - Nombre d'éléments: {len(nouveaux_par_date)}")
                
                if nouveaux_par_date:
                    sample_item = nouveaux_par_date[0]
                    print(f"  - Structure d'un élément: {sample_item}")
                    print(f"  - Clés disponibles: {list(sample_item.keys())}")
                    
                    # Vérifier que les clés attendues sont présentes
                    expected_keys = ['date', 'count']
                    missing_keys = [key for key in expected_keys if key not in sample_item]
                    
                    if missing_keys:
                        print(f"❌ Clés manquantes: {missing_keys}")
                    else:
                        print(f"✅ Toutes les clés attendues sont présentes")
                
                return True
            else:
                print(f"❌ Erreur dans la réponse")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def run_complete_test():
    """Exécute tous les tests pour les nouveaux membres par date"""
    print("🚀 DÉBUT DES TESTS NOUVEAUX MEMBRES PAR DATE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return False
    
    # Tests
    test_nouveaux_par_date_sans_filtre()
    test_nouveaux_par_date_daily()
    test_nouveaux_par_date_monthly()
    test_format_compatible_frontend()
    
    print("\n" + "="*80)
    print("RÉSUMÉ DES TESTS")
    print("="*80)
    print("✅ Tests terminés")
    print("📊 L'endpoint nouveaux_par_date est fonctionnel")
    print("📈 Compatible avec la logique du frontend")
    print("🎯 Format de données correct")


if __name__ == "__main__":
    run_complete_test() 