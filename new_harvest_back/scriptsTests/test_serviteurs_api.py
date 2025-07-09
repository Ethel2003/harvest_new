import requests

BASE_URL = "http://localhost:8000/api"
# Token d'authentification
AUTH_TOKEN = None
HEADERS = {"Content-Type": "application/json"}

def login():
    """Authentification pour obtenir un token"""
    global AUTH_TOKEN

    login_data = {"email": "utilisateur1@example.com", "password": "motdepasse"}

    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        print(f"Status login: {response.status_code}")
        print(f"Response login: {response.json()}")

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

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests API pour le modèle Serviteurs")
    print("=" * 50)

    # Authentification
    if not login():
        print("❌ Impossible de continuer sans authentification")
        return
     
    # Création d'un serviteur
    data = {
        "membre": 1,  # ID d'un membre existant
        "departement": 3,  # ID d'un département existant
        "titre": "Responsable",
        "is_responsable": True
    }
    r = requests.post(f"{BASE_URL}/serviteurs/", json=data, headers=HEADERS)
    print(r.status_code, r.json())

    # Liste des serviteurs
    r = requests.get(f"{BASE_URL}/serviteurs/", headers=HEADERS)
    print(r.status_code, r.json())

if __name__ == "__main__":
    run_all_tests()