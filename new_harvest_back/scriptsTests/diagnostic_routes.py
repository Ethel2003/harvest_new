#!/usr/bin/env python3
"""
Script de diagnostic pour vérifier l'état des routes de l'API
"""

import requests
import sys
import os

# Configuration de l'API
BASE_URL = "http://localhost:8000/api"

def test_endpoint(url, description=""):
    """Teste un endpoint et affiche le résultat"""
    print(f"\n{'='*50}")
    print(f"Test: {description}")
    print(f"URL: {url}")
    print(f"{'='*50}")
    
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Endpoint accessible")
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   Nombre d'éléments: {len(data)}")
                elif isinstance(data, dict) and 'data' in data:
                    print(f"   Nombre d'éléments: {len(data['data'])}")
                else:
                    print(f"   Type de réponse: {type(data)}")
            except:
                print(f"   Réponse: {response.text[:200]}...")
        elif response.status_code == 401:
            print("🔐 Endpoint accessible mais nécessite une authentification")
        elif response.status_code == 404:
            print("❌ Endpoint non trouvé")
        else:
            print(f"⚠️ Statut inattendu: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
        print("   Vérifiez que le serveur Django est démarré sur localhost:8000")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_authentification():
    """Teste l'authentification"""
    print("\n🔐 TEST D'AUTHENTIFICATION")
    print("="*50)
    
    login_data = {
        "email": "utilisateur1@example.com",
        "password": "motdepasse"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('token')
            if token:
                print("✅ Authentification réussie")
                return token
            else:
                print("❌ Token non trouvé dans la réponse")
                return None
        else:
            print(f"❌ Échec de l'authentification: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return None

def test_endpoints_avec_auth(token):
    """Teste les endpoints avec authentification"""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔐 TESTS AVEC AUTHENTIFICATION")
    print("="*50)
    
    # Test des endpoints principaux
    endpoints = [
        (f"{BASE_URL}/integrations/", "Liste des intégrations"),
        (f"{BASE_URL}/etiquetages/", "Liste des étiquetages"),
        (f"{BASE_URL}/membres/", "Liste des membres"),
        (f"{BASE_URL}/etapes/", "Liste des étapes"),
        (f"{BASE_URL}/tags/", "Liste des tags"),
    ]
    
    for url, description in endpoints:
        try:
            response = requests.get(url, headers=headers)
            print(f"\n{description}:")
            print(f"  URL: {url}")
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✅ Accessible")
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"  Nombre d'éléments: {len(data)}")
                    elif isinstance(data, dict) and 'data' in data:
                        print(f"  Nombre d'éléments: {len(data['data'])}")
                except:
                    pass
            elif response.status_code == 404:
                print("  ❌ Non trouvé")
            else:
                print(f"  ⚠️ Statut: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")

def afficher_routes_disponibles():
    """Affiche les routes disponibles"""
    print("\n📋 ROUTES DISPONIBLES")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API root accessible")
            try:
                data = response.json()
                print("Routes disponibles:")
                for key, value in data.items():
                    print(f"  - {key}: {value}")
            except:
                print(f"Réponse: {response.text[:500]}...")
        else:
            print(f"❌ API root non accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC DES ROUTES DE L'API")
    print("="*60)
    
    # Test de l'API root
    afficher_routes_disponibles()
    
    # Test des endpoints sans authentification
    print("\n🔓 TESTS SANS AUTHENTIFICATION")
    test_endpoint(f"{BASE_URL}/integrations/", "Intégrations (sans auth)")
    test_endpoint(f"{BASE_URL}/etiquetages/", "Étiquetages (sans auth)")
    
    # Test d'authentification
    token = test_authentification()
    
    # Test des endpoints avec authentification
    if token:
        test_endpoints_avec_auth(token)
    else:
        print("\n⚠️ Impossible de tester les endpoints authentifiés")
    
    print("\n" + "="*60)
    print("📝 RECOMMANDATIONS")
    print("="*60)
    
    print("1. Si les endpoints retournent 404:")
    print("   - Redémarrez le serveur Django")
    print("   - Vérifiez que les ViewSets sont bien enregistrés dans urls.py")
    
    print("\n2. Si l'authentification échoue:")
    print("   - Vérifiez les credentials dans le script")
    print("   - Créez un superutilisateur si nécessaire")
    
    print("\n3. Si le serveur ne répond pas:")
    print("   - Vérifiez que Django est démarré sur localhost:8000")
    print("   - Vérifiez les logs du serveur")

if __name__ == "__main__":
    main() 