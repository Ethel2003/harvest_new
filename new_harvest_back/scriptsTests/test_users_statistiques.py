#!/usr/bin/env python3
"""
Script de test pour l'endpoint des statistiques des utilisateurs
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN_HERE'  # Remplacez par votre token
}

def test_users_statistiques():
    """Test de l'endpoint statistiques des utilisateurs"""
    print("\n📊 Test des statistiques des utilisateurs...")

    try:
        response = requests.get(f"{BASE_URL}/users/statistiques/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                stats_data = data.get('data', {})
                
                # Statistiques globales
                stats_globales = stats_data.get('statistiques_globales', {})
                print(f"✅ Statistiques récupérées avec succès")
                print(f"📈 Statistiques globales:")
                print(f"  - Total utilisateurs: {stats_globales.get('total_users', 0)}")
                print(f"  - Utilisateurs actifs: {stats_globales.get('users_actifs', 0)}")
                print(f"  - Utilisateurs inactifs: {stats_globales.get('users_inactifs', 0)}")
                print(f"  - Nouveaux utilisateurs: {stats_globales.get('nouveaux_users', 0)}")
                
                # Répartition par rôles
                repartition_roles = stats_data.get('repartition_roles', {})
                if repartition_roles:
                    print(f"\n👥 Répartition par rôles:")
                    for role, nombre in repartition_roles.items():
                        print(f"  - {role}: {nombre}")
                else:
                    print(f"\n👥 Aucune répartition par rôles disponible")
                
                # Répartition par date de création
                repartition_date = stats_data.get('repartition_date_creation', {})
                if repartition_date:
                    print(f"\n📅 Répartition par date de création:")
                    for date, nombre in repartition_date.items():
                        print(f"  - {date}: {nombre} utilisateurs")
                else:
                    print(f"\n📅 Aucune répartition par date disponible")
                
                return True
            else:
                print(f"❌ Erreur dans la réponse: {data.get('error', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_users_list():
    """Test de la liste des utilisateurs pour comparaison"""
    print("\n📋 Test de la liste des utilisateurs...")

    try:
        response = requests.get(f"{BASE_URL}/users/", headers=HEADERS)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get('count', 0)
            print(f"✅ {count} utilisateurs récupérés dans la liste")
            return count
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    """Fonction principale"""
    print("🚀 Démarrage des tests des statistiques des utilisateurs")
    print("=" * 60)
    
    # Test des statistiques
    stats_success = test_users_statistiques()
    
    # Test de la liste pour comparaison
    users_count = test_users_list()
    
    print("\n" + "=" * 60)
    if stats_success:
        print("✅ Tests des statistiques des utilisateurs terminés avec succès")
    else:
        print("❌ Tests des statistiques des utilisateurs échoués")
    
    if users_count is not None:
        print(f"📊 Nombre d'utilisateurs dans la liste: {users_count}")

if __name__ == "__main__":
    main() 