#!/usr/bin/env python3
"""
Script de diagnostic pour le problème 404 avec l'endpoint evolution_membres
"""

import os
import sys
import django
import requests
from datetime import datetime

# Ajouter le répertoire parent au path Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
django.setup()

def test_evolution_membres_endpoint():
    """Test de l'endpoint evolution_membres avec différentes URLs"""
    
    base_url = "http://localhost:8000"
    
    # URLs à tester
    urls_to_test = [
        "/api/membres/evolution_membres/",
        "/api/membres/evolution_membres/?format=daily",
        "/api/membres/evolution_membres/?format=monthly",
        "/api/membres/",  # Test de l'endpoint de base
        "/api/membres/nouveaux_par_date/",  # Test d'un autre endpoint personnalisé
    ]
    
    print("🔍 Diagnostic de l'endpoint evolution_membres")
    print("=" * 50)
    
    for url in urls_to_test:
        full_url = base_url + url
        print(f"\n📡 Test de: {full_url}")
        
        try:
            response = requests.get(full_url, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                print("   ✅ Succès!")
                if 'application/json' in response.headers.get('content-type', ''):
                    try:
                        data = response.json()
                        print(f"   📊 Données reçues: {len(str(data))} caractères")
                        if isinstance(data, dict) and 'data' in data:
                            print(f"   📈 Nombre d'éléments: {len(data['data'])}")
                    except:
                        print("   ⚠️  Réponse JSON invalide")
            elif response.status_code == 404:
                print("   ❌ 404 - Endpoint non trouvé")
                print(f"   📄 Contenu de la page: {response.text[:200]}...")
            else:
                print(f"   ⚠️  Status inattendu: {response.status_code}")
                print(f"   📄 Contenu: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Erreur de connexion - Le serveur Django n'est peut-être pas démarré")
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout - Le serveur met trop de temps à répondre")
        except Exception as e:
            print(f"   💥 Erreur: {str(e)}")

def check_django_urls():
    """Vérification des URLs Django configurées"""
    print("\n🔧 Vérification de la configuration Django")
    print("=" * 50)
    
    try:
        from django.urls import get_resolver
        from django.conf import settings
        
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        
        print(f"📋 URLs racines configurées: {len(url_patterns)}")
        
        # Chercher les patterns pour l'API
        api_patterns = []
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for sub_pattern in pattern.url_patterns:
                    if 'api' in str(sub_pattern.pattern) or 'membres' in str(sub_pattern.pattern):
                        api_patterns.append(sub_pattern)
        
        print(f"🔗 Patterns API trouvés: {len(api_patterns)}")
        
        # Vérifier spécifiquement les actions du MembreViewSet
        from core.views import MembreViewSet
        actions = [attr for attr in dir(MembreViewSet) if hasattr(getattr(MembreViewSet, attr), 'mapping')]
        print(f"🎯 Actions du MembreViewSet: {actions}")
        
        # Vérifier si evolution_membres est dans les actions
        if hasattr(MembreViewSet, 'evolution_membres'):
            action_decorator = getattr(MembreViewSet, 'evolution_membres')
            if hasattr(action_decorator, 'mapping'):
                print("✅ L'action evolution_membres est correctement décorée")
                print(f"   Mapping: {action_decorator.mapping}")
            else:
                print("❌ L'action evolution_membres n'a pas de mapping")
        else:
            print("❌ L'action evolution_membres n'existe pas dans MembreViewSet")
            
    except Exception as e:
        print(f"💥 Erreur lors de la vérification des URLs: {str(e)}")

def check_server_status():
    """Vérification du statut du serveur Django"""
    print("\n🖥️  Vérification du statut du serveur")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Serveur Django accessible (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur Django non accessible")
        print("💡 Assurez-vous que le serveur Django est démarré avec:")
        print("   python manage.py runserver 8000")
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification du serveur: {str(e)}")

if __name__ == "__main__":
    print("🚀 Démarrage du diagnostic de l'endpoint evolution_membres")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    check_server_status()
    check_django_urls()
    test_evolution_membres_endpoint()
    
    print("\n" + "=" * 50)
    print("🏁 Diagnostic terminé")
    print("\n💡 Solutions possibles:")
    print("1. Redémarrer le serveur Django: python manage.py runserver 8000")
    print("2. Vérifier que l'action evolution_membres est bien décorée avec @action")
    print("3. Vérifier que le MembreViewSet est bien enregistré dans le router")
    print("4. Vérifier les logs du serveur Django pour plus de détails") 