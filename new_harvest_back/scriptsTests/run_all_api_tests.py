#!/usr/bin/env python3
"""
Script principal pour exécuter tous les tests API
Teste les endpoints pour Groupe, Etape, Tag et Departement
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def run_test_script(script_name, description):
    """Exécute un script de test spécifique"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        # Exécuter le script Python
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        # Afficher la sortie
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"⚠️ Erreurs: {result.stderr}")
        
        # Vérifier le code de retour
        if result.returncode == 0:
            print(f"✅ {description} - Tests terminés avec succès")
            return True
        else:
            print(f"❌ {description} - Tests échoués (code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {script_name}: {e}")
        return False

def check_server_health():
    """Vérifie que le serveur Django est accessible"""
    import requests
    
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur Django accessible")
            return True
        else:
            print(f"❌ Serveur Django accessible mais code: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Serveur Django non accessible")
        print("💡 Assurez-vous que le serveur Django est démarré sur http://localhost:8000")
        return False

def main():
    """Fonction principale"""
    print("🧪 SCRIPT DE TEST COMPLET DES ENDPOINTS API")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Vérifier que le serveur est accessible
    if not check_server_health():
        print("\n❌ Impossible de continuer sans serveur accessible")
        print("💡 Démarrez le serveur Django avec: python manage.py runserver")
        return
    
    # Liste des scripts à exécuter
    test_scripts = [
        ("test_groupe_api.py", "Tests API pour le modèle Groupe"),
        ("test_etape_api.py", "Tests API pour le modèle Etape"),
        ("test_tag_api.py", "Tests API pour le modèle Tag"),
        ("test_departement_api.py", "Tests API pour le modèle Departement"),
        ("test_users_statistiques.py", "Tests API pour les statistiques des utilisateurs")
    ]
    
    # Statistiques
    total_tests = len(test_scripts)
    successful_tests = 0
    failed_tests = 0
    
    # Exécuter chaque script
    for script_name, description in test_scripts:
        if run_test_script(script_name, description):
            successful_tests += 1
        else:
            failed_tests += 1
        
        # Pause entre les tests
        time.sleep(2)
    
    # Résumé final
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES TESTS")
    print(f"{'='*60}")
    print(f"✅ Tests réussis: {successful_tests}/{total_tests}")
    print(f"❌ Tests échoués: {failed_tests}/{total_tests}")
    
    if failed_tests == 0:
        print("🎉 Tous les tests sont passés avec succès !")
    else:
        print(f"⚠️ {failed_tests} test(s) ont échoué. Vérifiez les logs ci-dessus.")
    
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 