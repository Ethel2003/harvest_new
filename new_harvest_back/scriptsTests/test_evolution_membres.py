#!/usr/bin/env python3
"""
Script de test pour l'endpoint evolution_membres
Teste l'endpoint GET /api/membres/evolution_membres/
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Configuration Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
# django.setup()

# from django.contrib.auth.models import User
from core.models import Membre

def test_evolution_membres_endpoint():
    """
    Teste l'endpoint evolution_membres avec différentes configurations
    """
    
    # Configuration de base
    base_url = "http://localhost:8000"
    endpoint = "/api/membres/evolution_membres/"
    
    # # Créer un utilisateur de test si nécessaire
    # try:
    #     user = User.objects.get(username='test_user')
    # except User.DoesNotExist:
    #     user = User.objects.create_user(
    #         username='test_user',
    #         email='test@example.com',
    #         password='testpass123'
    #     )
    #     print(f"✅ Utilisateur de test créé: {user.username}")
    
    # Authentification
    login_data = {
        'email': 'utilisateur1@example.com',
        'password': 'motdepasse'
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/login/", json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            headers = {'Authorization': f'Token {token}'}
            print("✅ Authentification réussie")
        else:
            print(f"❌ Échec de l'authentification: {login_response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que le serveur Django est en cours d'exécution.")
        return
    
    # Test 1: Récupération de l'évolution par défaut (format daily)
    print("\n📊 Test 1: Évolution par défaut (format daily)")
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Données récupérées: {len(evolution_data)} points de données")
                if evolution_data:
                    print("📈 Exemple de données:")
                    for i, point in enumerate(evolution_data[:5]):  # Afficher les 5 premiers
                        print(f"   {point['date']}: {point['value']} membres")
                    if len(evolution_data) > 5:
                        print(f"   ... et {len(evolution_data) - 5} autres points")
                else:
                    print("ℹ️ Aucune donnée d'évolution disponible")
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 2: Format mensuel
    print("\n📊 Test 2: Format mensuel")
    try:
        response = requests.get(f"{base_url}{endpoint}?format=monthly", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Données mensuelles récupérées: {len(evolution_data)} points de données")
                if evolution_data:
                    print("📈 Exemple de données mensuelles:")
                    for i, point in enumerate(evolution_data[:5]):
                        print(f"   {point['date']}: {point['value']} membres")
                    if len(evolution_data) > 5:
                        print(f"   ... et {len(evolution_data) - 5} autres points")
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 3: Filtrage par date
    print("\n📊 Test 3: Filtrage par date (7 derniers jours)")
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        response = requests.get(
            f"{base_url}{endpoint}?start_date={start_date}&end_date={end_date}",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                print(f"✅ Données filtrées récupérées: {len(evolution_data)} points de données")
                print(f"📅 Période: {start_date} à {end_date}")
                if evolution_data:
                    print("📈 Données de la période:")
                    for point in evolution_data:
                        print(f"   {point['date']}: {point['value']} membres")
                else:
                    print("ℹ️ Aucune donnée pour cette période")
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # Test 4: Format de réponse
    print("\n📊 Test 4: Vérification du format de réponse")
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                evolution_data = data.get('data', [])
                if evolution_data:
                    # Vérifier le format de chaque point de données
                    format_correct = True
                    for point in evolution_data:
                        if not isinstance(point, dict) or 'date' not in point or 'value' not in point:
                            format_correct = False
                            break
                        if not isinstance(point['value'], int):
                            format_correct = False
                            break
                    
                    if format_correct:
                        print("✅ Format de réponse correct")
                        print(f"📋 Structure: {len(evolution_data)} objets avec 'date' et 'value'")
                    else:
                        print("❌ Format de réponse incorrect")
                else:
                    print("ℹ️ Aucune donnée à vérifier")
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def afficher_statistiques_membres():
    """
    Affiche des statistiques sur les membres existants
    """
    print("\n📊 Statistiques des membres existants:")
    
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
            membres_exemples = Membre.objects.filter(created_at__isnull=False).order_by('created_at')[:10]
            for membre in membres_exemples:
                print(f"   {membre.nom} {membre.prenom}: {membre.created_at}")

if __name__ == "__main__":
    print("🚀 Test de l'endpoint evolution_membres")
    print("=" * 50)
    
    # Afficher les statistiques existantes
    afficher_statistiques_membres()
    
    # Tester l'endpoint
    test_evolution_membres_endpoint()
    
    print("\n" + "=" * 50)
    print("✅ Test terminé") 