 #!/bin/bash

# Script bash pour exécuter les tests API
# Usage: ./run_tests.sh [option]

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que Python est installé
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 n'est pas installé"
        exit 1
    fi
    print_success "Python3 détecté"
}

# Vérifier que le serveur Django est accessible
check_server() {
    print_header "Vérification du serveur Django"
    
    if curl -s http://localhost:8000/api/ > /dev/null; then
        print_success "Serveur Django accessible"
    else
        print_error "Serveur Django non accessible"
        print_warning "Démarrez le serveur avec: python manage.py runserver"
        exit 1
    fi
}

# Installer les dépendances si nécessaire
install_dependencies() {
    print_header "Vérification des dépendances"
    
    if ! python3 -c "import requests" 2>/dev/null; then
        print_warning "Module 'requests' non trouvé, installation..."
        pip3 install requests
        print_success "Module 'requests' installé"
    else
        print_success "Module 'requests' déjà installé"
    fi
}

# Exécuter tous les tests
run_all_tests() {
    print_header "Exécution de tous les tests API"
    python3 run_all_api_tests.py
}

# Exécuter un test spécifique
run_specific_test() {
    local test_name=$1
    local script_name=""
    
    case $test_name in
        "groupe"|"groupes")
            script_name="test_groupe_api.py"
            ;;
        "etape"|"etapes")
            script_name="test_etape_api.py"
            ;;
        "tag"|"tags")
            script_name="test_tag_api.py"
            ;;
        "departement"|"departements")
            script_name="test_departement_api.py"
            ;;
        *)
            print_error "Test inconnu: $test_name"
            show_usage
            exit 1
            ;;
    esac
    
    print_header "Exécution du test: $test_name"
    python3 "$script_name"
}

# Afficher l'aide
show_usage() {
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  all                    Exécuter tous les tests"
    echo "  groupe|groupes         Tester les endpoints Groupe"
    echo "  etape|etapes           Tester les endpoints Etape"
    echo "  tag|tags               Tester les endpoints Tag"
    echo "  departement|departements Tester les endpoints Departement"
    echo "  help                   Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 all                 # Exécuter tous les tests"
    echo "  $0 groupe              # Tester seulement les groupes"
    echo "  $0 etapes              # Tester seulement les étapes"
}

# Fonction principale
main() {
    print_header "🧪 Script de Test API - Harvest Platform"
    
    # Vérifications préalables
    check_python
    install_dependencies
    check_server
    
    # Traitement des arguments
    case "${1:-all}" in
        "all")
            run_all_tests
            ;;
        "groupe"|"groupes"|"etape"|"etapes"|"tag"|"tags"|"departement"|"departements")
            run_specific_test "$1"
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            print_error "Option inconnue: $1"
            show_usage
            exit 1
            ;;
    esac
    
    print_header "🎉 Tests terminés !"
}

# Exécuter le script principal
main "$@"