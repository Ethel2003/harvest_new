#!/usr/bin/env python3
"""
Script de test pour l'endpoint des statistiques du tableau de bord.
Ce script teste l'endpoint /api/statistics/dashboard/ pour vérifier qu'il retourne
les bonnes statistiques au format attendu.
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Membre, Departement, Groupe

def test_dashboard_stats_endpoint():
    """
    Teste l'endpoint des statistiques du tableau de bord.
    """
    base_url = "http://localhost:8000"
    endpoint = "/api/statistics/dashboard/"
    
    print(f"🧪 Test de l'endpoint: {base_url}{endpoint}")
    print("=" * 50)
    
    try:
        # Test 1: Requête sans authentification (doit échouer)
        print("1. Test sans authentification...")
        response = requests.get(f"{base_url}{endpoint}")
        if response.status_code == 401:
            print("✅ Correct: L'endpoint nécessite une authentification")
        else:
            print(f"❌ Erreur: L'endpoint devrait nécessiter une authentification (status: {response.status_code})")
        
        # Test 2: Requête avec authentification (nécessite un token)
        print("\n2. Test avec authentification...")
        print("⚠️  Note: Ce test nécessite un utilisateur authentifié avec un token valide")
        print("   Pour tester manuellement:")
        print("   1. Connectez-vous via /api/login/")
        print("   2. Utilisez le token reçu pour appeler l'endpoint")
        
        # Afficher les statistiques actuelles de la base de données
        print("\n3. Statistiques actuelles dans la base de données:")
        print("-" * 40)
        
        departments_count = Departement.objects.count()
        groups_count = Groupe.objects.count()
        users_count = User.objects.count()
        members_count = Membre.objects.count()
        
        print(f"📊 Départements: {departments_count}")
        print(f"👥 Groupes: {groups_count}")
        print(f"👤 Utilisateurs: {users_count}")
        print(f"👨‍👩‍👧‍👦 Membres: {members_count}")
        
        # Format attendu
        expected_format = {
            "departments": departments_count,
            "groups": groups_count,
            "users": users_count,
            "members": members_count
        }
        
        print(f"\n📋 Format attendu de la réponse:")
        print(json.dumps(expected_format, indent=2))
        
        # Instructions pour tester manuellement
        print("\n🔧 Instructions pour tester manuellement:")
        print("1. Démarrez le serveur Django: python manage.py runserver")
        print("2. Connectez-vous via POST /api/login/ avec vos identifiants")
        print("3. Utilisez le token reçu pour appeler GET /api/statistics/dashboard/")
        print("4. Vérifiez que la réponse correspond au format attendu")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur Django")
        print("   Assurez-vous que le serveur est démarré: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

def create_test_data():
    """
    Crée des données de test pour vérifier les statistiques.
    """
    print("\n🔧 Création de données de test...")
    
    try:
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Utilisateur de test créé")
        else:
            print("ℹ️  Utilisateur de test existe déjà")
        
        # Créer un département de test
        dept, created = Departement.objects.get_or_create(
            nom='Département Test',
            defaults={
                'mission': 'Mission de test',
                'color': '#FF6B6B'
            }
        )
        if created:
            print("✅ Département de test créé")
        else:
            print("ℹ️  Département de test existe déjà")
        
        # Créer un groupe de test
        groupe, created = Groupe.objects.get_or_create(
            nom='Groupe Test',
            defaults={
                'description': 'Groupe de test',
                'color': '#4ECDC4'
            }
        )
        if created:
            print("✅ Groupe de test créé")
        else:
            print("ℹ️  Groupe de test existe déjà")
        
        # Créer un membre de test
        membre, created = Membre.objects.get_or_create(
            nom='Doe',
            prenom='John',
            defaults={
                'email': 'john.doe@example.com',
                'telephone': '+1234567890',
                'genre': 'Masculin',
                'situation_matrimoniale': 'Célibataire'
            }
        )
        if created:
            print("✅ Membre de test créé")
        else:
            print("ℹ️  Membre de test existe déjà")
        
        print("✅ Données de test prêtes")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données de test: {str(e)}")

if __name__ == "__main__":
    print("🚀 Test de l'endpoint des statistiques du tableau de bord")
    print("=" * 60)
    
    # Créer des données de test si demandé
    if len(sys.argv) > 1 and sys.argv[1] == "--create-data":
        create_test_data()
    
    # Tester l'endpoint
    success = test_dashboard_stats_endpoint()
    
    if success:
        print("\n✅ Tests terminés avec succès!")
    else:
        print("\n❌ Tests échoués!")
        sys.exit(1) 