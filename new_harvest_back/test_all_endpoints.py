#!/usr/bin/env python3
"""
Script de test pour vérifier tous les endpoints adaptés
Teste les endpoints /api/groupes/statistiques/, /api/tags/tous_les_tags/, /api/etapes/
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"

def test_groupes_statistiques():
    """Test de l'endpoint /api/groupes/statistiques/"""
    print("🏢 Test de l'endpoint /api/groupes/statistiques/")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/groupes/statistiques/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        
        # Vérifier la structure
        if 'groupes' in data and 'statistiques_globales' in data:
            print("✅ Structure de réponse correcte")
            
            groupes = data['groupes']
            stats = data['statistiques_globales']
            
            print(f"📊 Statistiques globales:")
            print(f"  - Total groupes: {stats.get('total_groupes', 0)}")
            print(f"  - Total membres: {stats.get('total_membres', 0)}")
            print(f"  - Moyenne membres par groupe: {stats.get('moyenne_membres_par_groupe', 0):.2f}")
            
            if stats.get('groupe_plus_populaire'):
                pop = stats['groupe_plus_populaire']
                print(f"  - Groupe le plus populaire: {pop.get('nom', 'N/A')} ({pop.get('membres_count', 0)} membres)")
            
            print(f"\n📋 Groupes ({len(groupes)} trouvés):")
            for i, groupe in enumerate(groupes[:5], 1):  # Afficher les 5 premiers
                print(f"  {i}. {groupe.get('nom', 'N/A')} (ID: {groupe.get('id', 'N/A')}, {groupe.get('membres_count', 0)} membres)")
            
            if len(groupes) > 5:
                print(f"  ... et {len(groupes) - 5} autres groupes")
        else:
            print("❌ Structure de réponse incorrecte")
            print(f"📝 Réponse: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"📝 Réponse: {response.text}")

def test_tags_tous_les_tags():
    """Test de l'endpoint /api/tags/tous_les_tags/"""
    print("\n🏷️ Test de l'endpoint /api/tags/tous_les_tags/")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/tags/tous_les_tags/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        
        # Vérifier que c'est un tableau
        if isinstance(data, list):
            print("✅ Structure de réponse correcte (tableau)")
            print(f"📊 Total tags: {len(data)}")
            
            print(f"\n🏷️ Tags ({len(data)} trouvés):")
            for i, tag in enumerate(data[:10], 1):  # Afficher les 10 premiers
                print(f"  {i}. {tag.get('name', 'N/A').strip()} (ID: {tag.get('id', 'N/A')})")
            
            if len(data) > 10:
                print(f"  ... et {len(data) - 10} autres tags")
        else:
            print("❌ Structure de réponse incorrecte (devrait être un tableau)")
            print(f"📝 Réponse: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"📝 Réponse: {response.text}")

def test_etapes():
    """Test de l'endpoint /api/etapes/"""
    print("\n📋 Test de l'endpoint /api/etapes/")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/etapes/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        
        # Vérifier la structure
        if isinstance(data, list):
            print("✅ Structure de réponse correcte (tableau)")
            print(f"📊 Total étapes: {len(data)}")
            
            print(f"\n📋 Étapes ({len(data)} trouvées):")
            for i, etape in enumerate(data, 1):
                print(f"  {i}. {etape.get('libelle', 'N/A')} (ID: {etape.get('id', 'N/A')})")
                if etape.get('description'):
                    print(f"     Description: {etape.get('description', 'N/A')}")
        else:
            print("❌ Structure de réponse incorrecte (devrait être un tableau)")
            print(f"📝 Réponse: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"📝 Réponse: {response.text}")

def test_etapes_pagination():
    """Test de l'endpoint /api/etapes/ avec pagination"""
    print("\n📋 Test de l'endpoint /api/etapes/ avec pagination")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/etapes/?page=1&page_size=5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        
        # Vérifier si c'est paginé ou non
        if isinstance(data, dict) and 'results' in data:
            print("✅ Structure de réponse paginée")
            print(f"📊 Total étapes: {data.get('count', 0)}")
            print(f"📋 Étapes dans cette page: {len(data.get('results', []))}")
            print(f"🔗 Page suivante: {data.get('next', 'Aucune')}")
            
            etapes = data.get('results', [])
            for i, etape in enumerate(etapes, 1):
                print(f"  {i}. {etape.get('libelle', 'N/A')} (ID: {etape.get('id', 'N/A')})")
        elif isinstance(data, list):
            print("✅ Structure de réponse simple (tableau)")
            print(f"📊 Total étapes: {len(data)}")
            
            for i, etape in enumerate(data[:5], 1):
                print(f"  {i}. {etape.get('libelle', 'N/A')} (ID: {etape.get('id', 'N/A')})")
        else:
            print("❌ Structure de réponse inattendue")
            print(f"📝 Réponse: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"📝 Réponse: {response.text}")

def test_search_functionality():
    """Test des fonctionnalités de recherche"""
    print("\n🔍 Test des fonctionnalités de recherche")
    print("=" * 60)
    
    # Test recherche dans les groupes
    print("\n🏢 Recherche dans les groupes:")
    response = requests.get(f"{BASE_URL}/api/groupes/statistiques/?search=FR")
    if response.status_code == 200:
        data = response.json()
        groupes = data.get('groupes', [])
        print(f"✅ {len(groupes)} groupes trouvés avec 'FR'")
    else:
        print(f"❌ Erreur recherche groupes: {response.status_code}")
    
    # Test recherche dans les tags
    print("\n🏷️ Recherche dans les tags:")
    response = requests.get(f"{BASE_URL}/api/tags/tous_les_tags/?search=Leader")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data)} tags trouvés avec 'Leader'")
    else:
        print(f"❌ Erreur recherche tags: {response.status_code}")

def test_error_handling():
    """Test de la gestion d'erreurs"""
    print("\n⚠️ Test de la gestion d'erreurs")
    print("=" * 60)
    
    # Test endpoint inexistant
    response = requests.get(f"{BASE_URL}/api/groupes/inexistant/")
    print(f"📄 Endpoint inexistant: {response.status_code}")
    
    # Test paramètres invalides
    response = requests.get(f"{BASE_URL}/api/tags/tous_les_tags/?page=abc")
    print(f"🔤 Paramètres invalides: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Test de tous les endpoints adaptés")
    print("=" * 80)
    
    try:
        # Tests principaux
        test_groupes_statistiques()
        test_tags_tous_les_tags()
        test_etapes()
        test_etapes_pagination()
        test_search_functionality()
        test_error_handling()
        
        print("\n✅ Tous les tests terminés avec succès!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion: Assurez-vous que le serveur Django est démarré")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}") 