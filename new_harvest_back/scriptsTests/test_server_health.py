#!/usr/bin/env python3
"""
Script de vérification de la santé du serveur Django
Vérifie que l'API est accessible et fonctionne correctement
"""

import requests
import sys
import time

# Configuration
BASE_URL = "http://localhost:8000/api"
TIMEOUT = 10

def check_server_health():
    """Vérifie que le serveur Django est accessible"""
    print("🔍 Vérification de la santé du serveur...")
    
    try:
        # Test de connexion basique
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        print(f"✅ Serveur accessible (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
        print("   Assurez-vous que Django est démarré avec: python manage.py runserver")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout lors de la connexion")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def check_api_endpoints():
    """Vérifie que les endpoints API sont accessibles"""
    print("\n🔍 Vérification des endpoints API...")
    
    endpoints = [
        "/membres/",
        "/categories-age/",
        "/departements/",
        "/tags/",
        "/groupes/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            if response.status_code in [200, 401, 403]:  # 401/403 = authentification requise
                print(f"✅ {endpoint} - Accessible (Status: {response.status_code})")
            else:
                print(f"⚠️ {endpoint} - Status inattendu: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Erreur: {e}")

def check_authentication():
    """Teste l'authentification"""
    print("\n🔐 Test d'authentification...")
    
    login_data = {
       "email": "utilisateur1@example.com",
        "password": "motdepasse"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, timeout=TIMEOUT)
        print(response.json())
        if response.status_code == 200:
            data = response.json()
            if 'token' in data['data']:
                print("✅ Authentification réussie")
                print(f"   Token: {data['data']['token'][:20]}...")
                return data['data']['token']
            else:
                print("❌ Token non trouvé dans la réponse")
                return None
        else:
            print(f"❌ Échec de l'authentification (Status: {response.status_code})")
            print(f"   Réponse: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return None

def test_membre_endpoint_with_auth(token):
    """Teste l'endpoint membres avec authentification"""
    print("\n👥 Test de l'endpoint membres avec authentification...")
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/membres/", headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint membres accessible - {len(data)} membres trouvés")
        else:
            print(f"❌ Erreur endpoint membres (Status: {response.status_code})")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def main():
    """Fonction principale"""
    print("🚀 Vérification de la santé du serveur Django")
    print("=" * 50)
    
    # Vérification de base
    if not check_server_health():
        print("\n❌ Le serveur n'est pas accessible. Arrêt des tests.")
        sys.exit(1)
    
    # Test d'authentification
    token = check_authentication()
    # Vérification des endpoints
    check_api_endpoints()
    
    
    if token:
        # Test avec authentification
        test_membre_endpoint_with_auth(token)
    
    print("\n" + "=" * 50)
    print("✅ Vérification terminée !")
    
    if token:
        print("\n💡 Le serveur semble fonctionner correctement.")
        print("   Vous pouvez maintenant exécuter les tests complets :")
        print("   python test_membre_api.py")
    else:
        print("\n⚠️ L'authentification a échoué.")
        print("   Vérifiez vos identifiants dans les scripts de test.")

if __name__ == "__main__":
    main() 