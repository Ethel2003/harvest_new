#!/usr/bin/env python3
"""
Script de test pour tous les endpoints de statistiques.
Ce script teste les endpoints suivants:
- /api/statistics/dashboard/
- /api/groupes/statistiques/
- /api/departements/statistiques/
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
    """Teste l'endpoint des statistiques du tableau de bord."""
    base_url = "http://localhost:8000"
    endpoint = "/api/statistics/dashboard/"
    
    print(f"🧪 Test de l'endpoint: {base_url}{endpoint}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}{endpoint}")
        if response.status_code == 401:
            print("✅ Correct: L'endpoint nécessite une authentification")
            return True
        else:
            print(f"❌ Erreur: L'endpoint devrait nécessiter une authentification (status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur Django")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

def test_groupes_statistiques_endpoint():
    """Teste l'endpoint des statistiques des groupes."""
    base_url = "http://localhost:8000"
    endpoint = "/api/groupes/statistiques/"
    
    print(f"\n🧪 Test de l'endpoint: {base_url}{endpoint}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}{endpoint}")
        if response.status_code == 401:
            print("✅ Correct: L'endpoint nécessite une authentification")
            return True
        else:
            print(f"❌ Erreur: L'endpoint devrait nécessiter une authentification (status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur Django")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

def test_departements_statistiques_endpoint():
    """Teste l'endpoint des statistiques des départements."""
    base_url = "http://localhost:8000"
    endpoint = "/api/departements/statistiques/"
    
    print(f"\n🧪 Test de l'endpoint: {base_url}{endpoint}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}{endpoint}")
        if response.status_code == 401:
            print("✅ Correct: L'endpoint nécessite une authentification")
            return True
        else:
            print(f"❌ Erreur: L'endpoint devrait nécessiter une authentification (status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur Django")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

def display_current_statistics():
    """Affiche les statistiques actuelles de la base de données."""
    print("\n📊 Statistiques actuelles dans la base de données:")
    print("=" * 50)
    
    try:
        departments_count = Departement.objects.count()
        groups_count = Groupe.objects.count()
        users_count = User.objects.count()
        members_count = Membre.objects.count()
        
        print(f"📊 Départements: {departments_count}")
        print(f"👥 Groupes: {groups_count}")
        print(f"👤 Utilisateurs: {users_count}")
        print(f"👨‍👩‍👧‍👦 Membres: {members_count}")
        
        # Afficher les détails des groupes
        print(f"\n📋 Détails des groupes:")
        for groupe in Groupe.objects.all():
            membres_count = groupe.regroupements.count()
            print(f"  - {groupe.nom}: {membres_count} membres")
        
        # Afficher les détails des départements
        print(f"\n📋 Détails des départements:")
        for departement in Departement.objects.all():
            serviteurs_count = departement.serviteurs.filter(actif=True).count()
            print(f"  - {departement.nom}: {serviteurs_count} serviteurs")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques: {str(e)}")
        return False

def create_test_data():
    """Crée des données de test pour vérifier les statistiques."""
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

def test_with_authentication():
    """Teste les endpoints avec authentification (nécessite un token valide)."""
    print("\n🔐 Test avec authentification")
    print("=" * 50)
    print("⚠️  Pour tester avec authentification:")
    print("1. Connectez-vous via POST /api/login/ avec vos identifiants")
    print("2. Utilisez le token reçu pour appeler les endpoints")
    print("3. Exemple de requête:")
    print("   curl -X GET http://localhost:8000/api/statistics/dashboard/ \\")
    print("     -H \"Authorization: Token votre_token_ici\"")
    print("\n4. Format attendu des réponses:")
    print("   - Dashboard: {\"departments\": 5, \"groups\": 12, \"users\": 8, \"members\": 150}")
    print("   - Groupes: {\"success\": true, \"data\": {\"groupes\": [...], \"statistiques_globales\": {...}}}")
    print("   - Départements: {\"success\": true, \"data\": {\"departements\": [...], \"statistiques_globales\": {...}}}")

if __name__ == "__main__":
    print("🚀 Test de tous les endpoints de statistiques")
    print("=" * 60)
    
    # Créer des données de test si demandé
    if len(sys.argv) > 1 and sys.argv[1] == "--create-data":
        create_test_data()
    
    # Tester tous les endpoints
    success_count = 0
    total_tests = 3
    
    success_count += 1 if test_dashboard_stats_endpoint() else 0
    success_count += 1 if test_groupes_statistiques_endpoint() else 0
    success_count += 1 if test_departements_statistiques_endpoint() else 0
    
    # Afficher les statistiques actuelles
    display_current_statistics()
    
    # Instructions pour les tests avec authentification
    test_with_authentication()
    
    print(f"\n📊 Résumé des tests: {success_count}/{total_tests} réussis")
    
    if success_count == total_tests:
        print("✅ Tous les tests sont passés avec succès!")
        print("\n🎯 Les endpoints sont prêts à être utilisés par le frontend")
    else:
        print("❌ Certains tests ont échoué!")
        print("   Vérifiez que le serveur Django est démarré")
        print("   Vérifiez que les URLs sont correctement configurées")
        sys.exit(1) 