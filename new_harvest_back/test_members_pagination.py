#!/usr/bin/env python3
"""
Script de test pour vérifier la pagination des membres
Teste l'endpoint /api/membres/ avec différents paramètres de pagination
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/membres/"

def test_members_pagination():
    """Test de la pagination des membres"""
    print("🧪 Test de la pagination des membres")
    print("=" * 50)
    
    # Test 1: Pagination de base
    print("\n1️⃣ Test pagination de base (page=1, page_size=10)")
    response = requests.get(f"{API_URL}?page=1&page_size=10")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Total membres: {data.get('count', 0)}")
        print(f"📄 Page actuelle: 1")
        print(f"📋 Membres dans cette page: {len(data.get('results', []))}")
        print(f"🔗 Page suivante: {data.get('next', 'Aucune')}")
        print(f"🔗 Page précédente: {data.get('previous', 'Aucune')}")
        
        # Afficher les premiers membres
        members = data.get('results', [])
        if members:
            print(f"\n👥 Premiers membres:")
            for i, member in enumerate(members[:3], 1):
                print(f"  {i}. {member.get('nom', 'N/A')} {member.get('prenom', 'N/A')} (ID: {member.get('id', 'N/A')})")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"📝 Réponse: {response.text}")
    
    # Test 2: Pagination avec recherche
    print("\n2️⃣ Test pagination avec recherche")
    response = requests.get(f"{API_URL}?page=1&page_size=5&search=Dupont")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Total résultats: {data.get('count', 0)}")
        print(f"📋 Membres trouvés: {len(data.get('results', []))}")
        
        members = data.get('results', [])
        if members:
            print(f"\n🔍 Membres trouvés:")
            for i, member in enumerate(members, 1):
                print(f"  {i}. {member.get('nom', 'N/A')} {member.get('prenom', 'N/A')}")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    # Test 3: Navigation entre les pages
    print("\n3️⃣ Test navigation entre les pages")
    
    # Page 1
    response1 = requests.get(f"{API_URL}?page=1&page_size=3")
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"📄 Page 1: {len(data1.get('results', []))} membres")
        print(f"🔗 Page suivante: {'Oui' if data1.get('next') else 'Non'}")
        
        # Page 2 si elle existe
        if data1.get('next'):
            response2 = requests.get(data1['next'])
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"📄 Page 2: {len(data2.get('results', []))} membres")
                print(f"🔗 Page précédente: {'Oui' if data2.get('previous') else 'Non'}")
            else:
                print(f"❌ Erreur page 2: {response2.status_code}")
    
    # Test 4: Différentes tailles de page
    print("\n4️⃣ Test différentes tailles de page")
    page_sizes = [5, 10, 20]
    
    for size in page_sizes:
        response = requests.get(f"{API_URL}?page=1&page_size={size}")
        if response.status_code == 200:
            data = response.json()
            print(f"📋 Page size {size}: {len(data.get('results', []))} membres")
        else:
            print(f"❌ Erreur page size {size}: {response.status_code}")
    
    # Test 5: Tri et pagination
    print("\n5️⃣ Test tri et pagination")
    response = requests.get(f"{API_URL}?page=1&page_size=5&ordering=nom")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Total membres: {data.get('count', 0)}")
        
        members = data.get('results', [])
        if members:
            print(f"\n📝 Membres triés par nom:")
            for i, member in enumerate(members, 1):
                print(f"  {i}. {member.get('nom', 'N/A')} {member.get('prenom', 'N/A')}")
    else:
        print(f"❌ Erreur: {response.status_code}")

def test_members_structure():
    """Test de la structure de réponse"""
    print("\n🔍 Test de la structure de réponse")
    print("=" * 50)
    
    response = requests.get(f"{API_URL}?page=1&page_size=1")
    
    if response.status_code == 200:
        data = response.json()
        
        # Vérifier la structure
        required_fields = ['count', 'next', 'previous', 'results']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print(f"❌ Champs manquants: {missing_fields}")
        else:
            print("✅ Structure de réponse correcte")
        
        # Vérifier le type des champs
        print(f"📊 count: {type(data['count'])} = {data['count']}")
        print(f"🔗 next: {type(data['next'])} = {data['next']}")
        print(f"🔗 previous: {type(data['previous'])} = {data['previous']}")
        print(f"📋 results: {type(data['results'])} (longueur: {len(data['results'])})")
        
        # Vérifier la structure d'un membre
        if data['results']:
            member = data['results'][0]
            print(f"\n👤 Structure d'un membre:")
            for key, value in member.items():
                print(f"  {key}: {type(value)} = {value}")
    
    else:
        print(f"❌ Erreur: {response.status_code}")

def test_error_handling():
    """Test de la gestion d'erreurs"""
    print("\n⚠️ Test de la gestion d'erreurs")
    print("=" * 50)
    
    # Test page invalide
    response = requests.get(f"{API_URL}?page=999&page_size=10")
    print(f"📄 Page 999: {response.status_code}")
    
    # Test page_size invalide
    response = requests.get(f"{API_URL}?page=1&page_size=0")
    print(f"📋 Page size 0: {response.status_code}")
    
    # Test paramètres invalides
    response = requests.get(f"{API_URL}?page=abc&page_size=def")
    print(f"🔤 Paramètres invalides: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Test de l'endpoint de pagination des membres")
    print("=" * 60)
    
    try:
        # Tests principaux
        test_members_pagination()
        test_members_structure()
        test_error_handling()
        
        print("\n✅ Tous les tests terminés avec succès!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion: Assurez-vous que le serveur Django est démarré")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}") 