#!/usr/bin/env python3
"""
Script de test amélioré pour l'endpoint evolution_membres
Teste l'endpoint avec différents scénarios de paramètres
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Membre

def test_evolution_membres_without_params():
    """
    Teste l'endpoint sans aucun paramètre
    """
    print("\n🔍 Test 1: Sans paramètres")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    endpoint = "/api/membres/evolution_membres/"
    
    # Authentification
    token = get_auth_token()
    if not token:
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    try:
        # Test sans aucun paramètre
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        print(f"URL appelée: {base_url}{endpoint}")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Succès! Données récupérées: {len(evolution_data)} points")
                if evolution_data:
                    print("📊 Exemple de données:")
                    for i, point in enumerate(evolution_data[:3]):
                        print(f"   {point['date']}: {point['value']} membres")
                    if len(evolution_data) > 3:
                        print(f"   ... et {len(evolution_data) - 3} autres points")
                else:
                    print("ℹ️ Aucune donnée disponible")
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def test_evolution_membres_with_format_only():
    """
    Teste l'endpoint avec seulement le paramètre format
    """
    print("\n🔍 Test 2: Avec format seulement")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    endpoint = "/api/membres/evolution_membres/"
    
    # Authentification
    token = get_auth_token()
    if not token:
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test avec format daily
    try:
        response = requests.get(f"{base_url}{endpoint}?format=daily", headers=headers)
        print(f"URL appelée: {base_url}{endpoint}?format=daily")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Succès! Données quotidiennes: {len(evolution_data)} points")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test avec format monthly
    try:
        response = requests.get(f"{base_url}{endpoint}?format=monthly", headers=headers)
        print(f"URL appelée: {base_url}{endpoint}?format=monthly")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Succès! Données mensuelles: {len(evolution_data)} points")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_evolution_membres_with_dates():
    """
    Teste l'endpoint avec des paramètres de date
    """
    print("\n🔍 Test 3: Avec paramètres de date")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    endpoint = "/api/membres/evolution_membres/"
    
    # Authentification
    token = get_auth_token()
    if not token:
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test avec start_date seulement
    try:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        response = requests.get(f"{base_url}{endpoint}?start_date={start_date}", headers=headers)
        print(f"URL appelée: {base_url}{endpoint}?start_date={start_date}")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Succès! Données depuis {start_date}: {len(evolution_data)} points")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test avec start_date et end_date
    try:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{base_url}{endpoint}?start_date={start_date}&end_date={end_date}", headers=headers)
        print(f"URL appelée: {base_url}{endpoint}?start_date={start_date}&end_date={end_date}")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Succès! Données de {start_date} à {end_date}: {len(evolution_data)} points")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_evolution_membres_all_params():
    """
    Teste l'endpoint avec tous les paramètres
    """
    print("\n🔍 Test 4: Avec tous les paramètres")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    endpoint = "/api/membres/evolution_membres/"
    
    # Authentification
    token = get_auth_token()
    if not token:
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    try:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        format_type = 'daily'
        
        url = f"{base_url}{endpoint}?start_date={start_date}&end_date={end_date}&format={format_type}"
        response = requests.get(url, headers=headers)
        print(f"URL appelée: {url}")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Succès! Données complètes: {len(evolution_data)} points")
                if evolution_data:
                    print("📊 Données récupérées:")
                    for point in evolution_data:
                        print(f"   {point['date']}: {point['value']} membres")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_url_generation():
    """
    Teste la génération des URLs avec différents paramètres
    """
    print("\n🔍 Test 5: Génération d'URLs")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    endpoint = "/api/membres/evolution_membres/"
    
    test_cases = [
        {"name": "Aucun paramètre", "params": {}},
        {"name": "Format seulement", "params": {"format": "daily"}},
        {"name": "Start date seulement", "params": {"start_date": "2024-01-01"}},
        {"name": "End date seulement", "params": {"end_date": "2024-12-31"}},
        {"name": "Start et end date", "params": {"start_date": "2024-01-01", "end_date": "2024-12-31"}},
        {"name": "Tous les paramètres", "params": {"start_date": "2024-01-01", "end_date": "2024-12-31", "format": "monthly"}},
        {"name": "Dates vides", "params": {"start_date": "", "end_date": "", "format": "daily"}},
    ]
    
    for test_case in test_cases:
        params = test_case["params"]
        query_params = []
        
        for key, value in params.items():
            if value and value.strip() != "":
                query_params.append(f"{key}={value}")
        
        query_string = "&".join(query_params)
        url = f"{base_url}{endpoint}{'?' + query_string if query_string else ''}"
        
        print(f"📋 {test_case['name']}:")
        print(f"   URL: {url}")
        print(f"   Paramètres: {params}")
        print()

def get_auth_token():
    """
    Récupère un token d'authentification
    """
    base_url = "http://localhost:8000"
    
    # Créer un utilisateur de test si nécessaire
    try:
        user = User.objects.get(username='test_user')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✅ Utilisateur de test créé: {user.username}")
    
    # Authentification
    login_data = {
        'username': 'test_user',
        'password': 'testpass123'
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/login/", json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print("✅ Authentification réussie")
            return token
        else:
            print(f"❌ Échec de l'authentification: {login_response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que le serveur Django est en cours d'exécution.")
        return None

def afficher_statistiques_membres():
    """
    Affiche des statistiques sur les membres existants
    """
    print("\n📊 Statistiques des membres existants:")
    print("=" * 50)
    
    total_membres = Membre.objects.count()
    print(f"Total des membres: {total_membres}")
    
    if total_membres > 0:
        membres_avec_date = Membre.objects.filter(created_at__isnull=False).count()
        print(f"Membres avec date de création: {membres_avec_date}")
        
        if membres_avec_date > 0:
            premier_membre = Membre.objects.filter(created_at__isnull=False).order_by('created_at').first()
            dernier_membre = Membre.objects.filter(created_at__isnull=False).order_by('created_at').last()
            
            print(f"Premier membre créé: {premier_membre.created_at}")
            print(f"Dernier membre créé: {dernier_membre.created_at}")
            
            # Afficher quelques exemples de dates
            print("\n📅 Exemples de dates de création:")
            membres_exemples = Membre.objects.filter(created_at__isnull=False).order_by('created_at')[:5]
            for membre in membres_exemples:
                print(f"   {membre.nom} {membre.prenom}: {membre.created_at}")

if __name__ == "__main__":
    print("🚀 Test amélioré de l'endpoint evolution_membres")
    print("=" * 60)
    
    # Afficher les statistiques existantes
    afficher_statistiques_membres()
    
    # Tests des différents scénarios
    test_evolution_membres_without_params()
    test_evolution_membres_with_format_only()
    test_evolution_membres_with_dates()
    test_evolution_membres_all_params()
    test_url_generation()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés") 