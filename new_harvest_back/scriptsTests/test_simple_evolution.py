#!/usr/bin/env python3
"""
Test simple de l'endpoint evolution_membres
"""

import os
import sys
import django
import requests
import json

# Ajouter le répertoire parent au path Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
django.setup()

def test_endpoint_with_auth():
    """Test de l'endpoint avec authentification"""
    
    base_url = "http://localhost:8000"
    
    # D'abord, créer un token d'authentification
    try:
        # Créer un utilisateur de test si nécessaire
        from django.contrib.auth.models import User
        from rest_framework.authtoken.models import Token
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Utilisateur de test créé")
        
        # Créer ou récupérer le token
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print("✅ Token créé")
        else:
            print("✅ Token récupéré")
        
        # Headers avec authentification
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        
        # Test de l'endpoint sans paramètres
        print("\n🔍 Test de l'endpoint sans paramètres:")
        response = requests.get(f"{base_url}/api/membres/evolution_membres/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Succès! Données: {len(data.get('data', []))} éléments")
            print(f"   📊 Premier élément: {data.get('data', [])[:1]}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test de l'endpoint avec paramètre format=daily
        print("\n🔍 Test de l'endpoint avec format=daily:")
        response = requests.get(f"{base_url}/api/membres/evolution_membres/?format=daily", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Succès! Données: {len(data.get('data', []))} éléments")
            print(f"   📊 Premier élément: {data.get('data', [])[:1]}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test de l'endpoint avec paramètre format=monthly
        print("\n🔍 Test de l'endpoint avec format=monthly:")
        response = requests.get(f"{base_url}/api/membres/evolution_membres/?format=monthly", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Succès! Données: {len(data.get('data', []))} éléments")
            print(f"   📊 Premier élément: {data.get('data', [])[:1]}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test avec paramètres de date
        print("\n🔍 Test avec paramètres de date:")
        response = requests.get(f"{base_url}/api/membres/evolution_membres/?start_date=2024-01-01&end_date=2024-12-31", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Succès! Données: {len(data.get('data', []))} éléments")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"💥 Erreur lors du test: {str(e)}")

def check_url_patterns():
    """Vérification des patterns d'URL"""
    print("\n🔧 Vérification des patterns d'URL")
    print("=" * 50)
    
    try:
        from django.urls import get_resolver
        from core.views import MembreViewSet
        
        resolver = get_resolver()
        
        # Afficher tous les patterns d'URL
        def print_patterns(patterns, level=0):
            indent = "  " * level
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    print(f"{indent}📁 {pattern.pattern} -> {len(pattern.url_patterns)} sous-patterns")
                    print_patterns(pattern.url_patterns, level + 1)
                else:
                    print(f"{indent}🔗 {pattern.pattern} -> {pattern.callback}")
        
        print_patterns(resolver.url_patterns)
        
        # Vérifier spécifiquement les actions du MembreViewSet
        print(f"\n🎯 Actions du MembreViewSet:")
        for attr in dir(MembreViewSet):
            if hasattr(getattr(MembreViewSet, attr), 'mapping'):
                action = getattr(MembreViewSet, attr)
                print(f"   - {attr}: {action.mapping}")
                
    except Exception as e:
        print(f"💥 Erreur lors de la vérification des patterns: {str(e)}")

if __name__ == "__main__":
    print("🚀 Test simple de l'endpoint evolution_membres")
    print("=" * 50)
    
    check_url_patterns()
    test_endpoint_with_auth()
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé") 