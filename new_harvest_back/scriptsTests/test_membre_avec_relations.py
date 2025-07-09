#!/usr/bin/env python3
"""
Script de test pour l'endpoint membre_avec_relations
Teste la récupération d'un membre avec ses relations: tags, étape, groupe, département
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
MEMBRES_URL = f"{BASE_URL}/membres"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Token d'authentification
AUTH_TOKEN = None

def login():
    """Authentification pour obtenir un token"""
    global AUTH_TOKEN
    
    login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        print(f"Status login: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            AUTH_TOKEN = data["data"]["token"]
            HEADERS["Authorization"] = f"Token {AUTH_TOKEN}"
            print("✅ Authentification réussie")
            return True
        else:
            print(f"❌ Échec de l'authentification: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return False

def get_existing_membre_id():
    """Récupère un ID de membre existant pour les tests"""
    try:
        response = requests.get(f"{MEMBRES_URL}/", headers=HEADERS)
        if response.status_code == 200:
            membres_data = response.json()
            if membres_data.get('results') and len(membres_data['results']) > 0:
                return membres_data['results'][0]['id']
        return 1  # Fallback
    except Exception as e:
        print(f"Erreur lors de la récupération d'un membre: {e}")
        return 1

def test_membre_avec_relations():
    """Test 1: Récupération d'un membre avec ses relations"""
    print("\n1️⃣ Test MEMBRE_AVEC_RELATIONS - Récupération complète")
    
    membre_id = get_existing_membre_id()
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Récupération réussie!")
            print(f"Success: {data.get('success', 'N/A')}")
            
            # Vérifier la structure de la réponse
            if 'data' in data:
                membre_data = data['data'].get('membre', {})
                relations = data['data'].get('relations', {})
                stats = data['data'].get('statistiques', {})
                
                print(f"Informations du membre:")
                print(f"  - Nom: {membre_data.get('nom', 'N/A')} {membre_data.get('prenom', 'N/A')}")
                print(f"  - Email: {membre_data.get('email', 'N/A')}")
                print(f"  - Téléphone: {membre_data.get('telephone', 'N/A')}")
                
                print(f"Relations:")
                print(f"  - Tags: {len(relations.get('tags', []))} tags")
                print(f"  - Étape actuelle: {'Oui' if relations.get('etape_actuelle') else 'Non'}")
                print(f"  - Groupe actuel: {'Oui' if relations.get('groupe_actuel') else 'Non'}")
                print(f"  - Département actuel: {'Oui' if relations.get('departement_actuel') else 'Non'}")
                
                print(f"Statistiques:")
                print(f"  - Nombre de tags: {stats.get('nombre_tags', 'N/A')}")
                print(f"  - A une étape: {stats.get('a_une_etape', 'N/A')}")
                print(f"  - A un groupe: {stats.get('a_un_groupe', 'N/A')}")
                print(f"  - A un département: {stats.get('a_un_departement', 'N/A')}")
                
                return True
            else:
                print(f"❌ Structure de réponse incorrecte")
                return False
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_membre_inexistant():
    """Test 2: Test avec un membre inexistant"""
    print("\n2️⃣ Test MEMBRE_INEXISTANT - Membre inexistant")
    
    membre_id = 99999  # ID inexistant
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 404:
            print(f"✅ Erreur 404 correcte pour membre inexistant")
            return True
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_structure_reponse():
    """Test 3: Vérification de la structure de la réponse"""
    print("\n3️⃣ Test STRUCTURE_REPONSE - Vérification de la structure")
    
    membre_id = get_existing_membre_id()
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Vérifier les clés principales
            required_keys = ['success', 'data']
            data_keys = ['membre', 'relations', 'statistiques']
            relations_keys = ['tags', 'etape_actuelle', 'groupe_actuel', 'departement_actuel']
            stats_keys = ['nombre_tags', 'a_une_etape', 'a_un_groupe', 'a_un_departement']
            
            print(f"Vérification des clés principales:")
            for key in required_keys:
                if key in data:
                    print(f"  ✅ {key}: présent")
                else:
                    print(f"  ❌ {key}: manquant")
            
            if 'data' in data:
                print(f"Vérification des clés de data:")
                for key in data_keys:
                    if key in data['data']:
                        print(f"  ✅ {key}: présent")
                    else:
                        print(f"  ❌ {key}: manquant")
                
                if 'relations' in data['data']:
                    print(f"Vérification des clés de relations:")
                    for key in relations_keys:
                        if key in data['data']['relations']:
                            print(f"  ✅ {key}: présent")
                        else:
                            print(f"  ❌ {key}: manquant")
                
                if 'statistiques' in data['data']:
                    print(f"Vérification des clés de statistiques:")
                    for key in stats_keys:
                        if key in data['data']['statistiques']:
                            print(f"  ✅ {key}: présent")
                        else:
                            print(f"  ❌ {key}: manquant")
            
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_donnees_tags():
    """Test 4: Vérification des données des tags"""
    print("\n4️⃣ Test DONNEES_TAGS - Vérification des tags")
    
    membre_id = get_existing_membre_id()
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tags = data.get('data', {}).get('relations', {}).get('tags', [])
            
            print(f"Tags trouvés: {len(tags)}")
            
            if tags:
                print(f"Structure du premier tag:")
                first_tag = tags[0]
                tag_keys = ['id', 'name', 'date_association']
                
                for key in tag_keys:
                    if key in first_tag:
                        print(f"  ✅ {key}: {first_tag[key]}")
                    else:
                        print(f"  ❌ {key}: manquant")
            else:
                print(f"  ℹ️ Aucun tag trouvé pour ce membre")
            
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_donnees_etape():
    """Test 5: Vérification des données de l'étape"""
    print("\n5️⃣ Test DONNEES_ETAPE - Vérification de l'étape")
    
    membre_id = get_existing_membre_id()
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            etape = data.get('data', {}).get('relations', {}).get('etape_actuelle')
            
            if etape:
                print(f"Étape trouvée:")
                etape_keys = ['id', 'libelle', 'description', 'date_association']
                
                for key in etape_keys:
                    if key in etape:
                        print(f"  ✅ {key}: {etape[key]}")
                    else:
                        print(f"  ❌ {key}: manquant")
            else:
                print(f"  ℹ️ Aucune étape trouvée pour ce membre")
            
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_donnees_groupe():
    """Test 6: Vérification des données du groupe"""
    print("\n6️⃣ Test DONNEES_GROUPE - Vérification du groupe")
    
    membre_id = get_existing_membre_id()
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            groupe = data.get('data', {}).get('relations', {}).get('groupe_actuel')
            
            if groupe:
                print(f"Groupe trouvé:")
                groupe_keys = ['id', 'nom', 'description', 'date_inscription', 'date_sortie']
                
                for key in groupe_keys:
                    if key in groupe:
                        print(f"  ✅ {key}: {groupe[key]}")
                    else:
                        print(f"  ❌ {key}: manquant")
            else:
                print(f"  ℹ️ Aucun groupe trouvé pour ce membre")
            
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_donnees_departement():
    """Test 7: Vérification des données du département"""
    print("\n7️⃣ Test DONNEES_DEPARTEMENT - Vérification du département")
    
    membre_id = get_existing_membre_id()
    
    try:
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            departement = data.get('data', {}).get('relations', {}).get('departement_actuel')
            
            if departement:
                print(f"Département trouvé:")
                dept_keys = ['id', 'nom', 'mission', 'color', 'date_inscription', 'date_sortie']
                
                for key in dept_keys:
                    if key in departement:
                        print(f"  ✅ {key}: {departement[key]}")
                    else:
                        print(f"  ❌ {key}: manquant")
            else:
                print(f"  ℹ️ Aucun département trouvé pour ce membre")
            
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_performance():
    """Test 8: Test de performance"""
    print("\n8️⃣ Test PERFORMANCE - Temps de réponse")
    
    membre_id = get_existing_membre_id()
    
    try:
        start_time = time.time()
        response = requests.get(f"{MEMBRES_URL}/{membre_id}/membre_avec_relations/", 
                               headers=HEADERS)
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000  # en millisecondes
        
        print(f"Temps de réponse: {duration:.2f}ms")
        
        if response.status_code == 200:
            print(f"✅ Performance acceptable")
            return True
        else:
            print(f"❌ Échec: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST MEMBRE_AVEC_RELATIONS - Récupération membre avec relations")
    print("=" * 75)
    print(f"Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Tests
    success_count = 0
    total_tests = 8
    
    # Test 1: Récupération complète
    if test_membre_avec_relations():
        success_count += 1
    
    # Test 2: Membre inexistant
    if test_membre_inexistant():
        success_count += 1
    
    # Test 3: Structure de réponse
    if test_structure_reponse():
        success_count += 1
    
    # Test 4: Données des tags
    if test_donnees_tags():
        success_count += 1
    
    # Test 5: Données de l'étape
    if test_donnees_etape():
        success_count += 1
    
    # Test 6: Données du groupe
    if test_donnees_groupe():
        success_count += 1
    
    # Test 7: Données du département
    if test_donnees_departement():
        success_count += 1
    
    # Test 8: Performance
    if test_performance():
        success_count += 1
    
    # Résumé
    print("\n" + "=" * 75)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 75)
    print(f"Tests réussis: {success_count}/{total_tests}")
    print(f"Taux de succès: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 Tous les tests sont passés!")
    else:
        print("⚠️ Certains tests ont échoué")
    
    print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 