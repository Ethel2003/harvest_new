#!/usr/bin/env python3
"""
Script de test pour les endpoints de filtrage des membres
Teste les filtres par groupes, étapes et tags
"""

import requests
import json
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')

import django
django.setup()

from core.models import Membre, Groupe, Etape, Tag, Regroupements, Integration, Etiquetage

# Configuration de l'API
BASE_URL = "http://localhost:8000/api"
LOGIN_URL = f"{BASE_URL}/login"
MEMBRES_URL = f"{BASE_URL}/membres"

def login():
    """Authentification pour obtenir un token"""
    login_data = {
        "email": "utilisateur1@example.com",  # Remplacer par un email valide
        "password": "motdepasse"  # Remplacer par un mot de passe valide
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('token')
        else:
            print(f"Erreur de connexion: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")
        return None

def test_endpoint(url, description, expected_status=200):
    """Teste un endpoint et affiche le résultat"""
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ Succès")
            data = response.json()
            print(f"Données reçues: {data}")
            if 'results' in data:
                membres = data['results']
                if isinstance(membres, list):
                    print(f"Nombre de membres trouvés: {len(membres)}")
                    if membres:
                        print("Premier membre:")
                        print(f"  - Nom: {membres[0].get('nom', 'N/A')}")
                        print(f"  - Prénom: {membres[0].get('prenom', 'N/A')}")
                        print(f"  - ID: {membres[0].get('id', 'N/A')}")
                else:
                    print(f"Données reçues: {type(membres)}")
            
            if 'filtres_appliques' in data:
                print(f"Filtres appliqués: {data['filtres_appliques']}")
                
        else:
            print("❌ Échec")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_filtres_membres():
    """Teste tous les endpoints de filtrage des membres"""
    
    # Test 1: Filtrage par groupes
    test_endpoint(
        f"{MEMBRES_URL}/par_groupes/?groupes[]=4&groupes[]=5",
        "Filtrage par groupes (IDs 4 et 5)"
    )
    
    # Test 2: Filtrage par étapes
    test_endpoint(
        f"{MEMBRES_URL}/par_etapes/?etapes[]=2&etapes[]=3",
        "Filtrage par étapes (IDs 2 et 3)"
    )
    
    # Test 3: Filtrage par tags
    test_endpoint(
        f"{MEMBRES_URL}/par_tags/?tags[]=2&tags[]=3",
        "Filtrage par tags (IDs 2 et 3)"
    )
    
    # Test 4: Filtrage combiné
    test_endpoint(
        f"{MEMBRES_URL}/filtres_combines/?groupes[]=4&etapes[]=2&tags[]=2",
        "Filtrage combiné (groupe 1, étape 1, tag 1)"
    )
    
    # Test 5: Endpoint principal avec filtres
    test_endpoint(
        f"{MEMBRES_URL}/?groupes[]=4&etapes[]=2&tags[]=2",
        "Endpoint principal avec filtres combinés"
    )
    
    # Test 6: Test avec des IDs inexistants
    test_endpoint(
        f"{MEMBRES_URL}/par_groupes/?groupes[]=999",
        "Filtrage par groupe inexistant (devrait retourner une liste vide)",
        200
    )
    
    # Test 7: Test sans paramètres (devrait retourner une erreur)
    test_endpoint(
        f"{MEMBRES_URL}/par_groupes/",
        "Filtrage par groupes sans paramètres (devrait retourner une erreur)",
        400
    )

def afficher_donnees_test():
    """Affiche les données disponibles pour les tests"""
    print("\n" + "="*60)
    print("DONNÉES DISPONIBLES POUR LES TESTS")
    print("="*60)
    
    # Groupes
    groupes = Groupe.objects.all()[:5]
    print(f"\nGroupes disponibles (premiers 5):")
    for groupe in groupes:
        print(f"  - ID: {groupe.id}, Nom: {groupe.nom}")
    
    # Étapes
    etapes = Etape.objects.all()[:5]
    print(f"\nÉtapes disponibles (premiers 5):")
    for etape in etapes:
        print(f"  - ID: {etape.id}, Libellé: {etape.libelle}")
    
    # Tags
    tags = Tag.objects.all()[:5]
    print(f"\nTags disponibles (premiers 5):")
    for tag in tags:
        print(f"  - ID: {tag.id}, Nom: {tag.name}")
    
    # Membres avec relations
    print(f"\nMembres avec regroupements:")
    membres_groupes = Membre.objects.filter(regroupements__isnull=False).distinct()[:3]
    for membre in membres_groupes:
        regroupements = membre.regroupements.filter(actif=True)
        print(f"  - Membre {membre.id}: {membre.nom} {membre.prenom}")
        for reg in regroupements:
            print(f"    * Groupe: {reg.groupe.nom} (ID: {reg.groupe.id})")
    
    print(f"\nMembres avec intégrations:")
    membres_integrations = Membre.objects.filter(integration__isnull=False).distinct()[:3]
    for membre in membres_integrations:
        integrations = membre.integration_set.all()
        print(f"  - Membre {membre.id}: {membre.nom} {membre.prenom}")
        for integ in integrations:
            print(f"    * Étape: {integ.etape.libelle} (ID: {integ.etape.id})")
    
    print(f"\nMembres avec étiquetages:")
    membres_tags = Membre.objects.filter(etiquetage__isnull=False).distinct()[:3]
    for membre in membres_tags:
        etiquetages = membre.etiquetage_set.all()
        print(f"  - Membre {membre.id}: {membre.nom} {membre.prenom}")
        for etiq in etiquetages:
            print(f"    * Tag: {etiq.tag.name} (ID: {etiq.tag.id})")

if __name__ == "__main__":
    print("🧪 TESTS DES ENDPOINTS DE FILTRAGE DES MEMBRES")
    print("="*60)
    
    # Authentification
    token = login()
    if not token:
        print("❌ Impossible de s'authentifier. Vérifiez les identifiants.")
        sys.exit(1)
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    print("✅ Authentification réussie")
    
    # Afficher les données disponibles
    afficher_donnees_test()
    
    # Lancer les tests
    print("\n🚀 LANCEMENT DES TESTS")
    test_filtres_membres()
    
    print("\n✅ Tests terminés!") 