#!/bin/bash

# Script de test pour les routes API du modèle Membre avec cURL
# Ce script teste toutes les fonctionnalités CRUD et les actions personnalisées

# Configuration
BASE_URL="http://localhost:8000/api"
TOKEN=""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Démarrage des tests API pour le modèle Membre${NC}"
echo "=================================================="

# Fonction pour afficher les résultats
print_result() {
    local status=$1
    local message=$2
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✅ $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

# 1. Authentification
echo -e "\n${YELLOW}🔐 Authentification...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin",
        "password": "admin123"
    }')

if echo "$LOGIN_RESPONSE" | grep -q "token"; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Authentification réussie${NC}"
    echo "Token: ${TOKEN:0:20}..."
else
    echo -e "${RED}❌ Échec de l'authentification${NC}"
    echo "Réponse: $LOGIN_RESPONSE"
    exit 1
fi

# 2. Test de création d'un membre
echo -e "\n${YELLOW}🔧 Test de création d'un membre...${NC}"
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/membres/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d '{
        "nom": "Dupont",
        "prenom": "Jean",
        "adresse": "123 Rue de la Paix",
        "ville": "Paris",
        "telephone": "+33123456789",
        "email": "jean.dupont@email.com",
        "profession": "Ingénieur",
        "nationalite": "Française",
        "color": "1",
        "genre": "masculin",
        "date_naissance": "1990-05-15",
        "situation_matrimoniale": "marie",
        "statut": "membre"
    }')

if echo "$CREATE_RESPONSE" | grep -q "Nouveau élément créé"; then
    MEMBRE_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    echo -e "${GREEN}✅ Membre créé avec succès (ID: $MEMBRE_ID)${NC}"
else
    echo -e "${RED}❌ Erreur lors de la création${NC}"
    echo "Réponse: $CREATE_RESPONSE"
    exit 1
fi

# 3. Test de récupération de la liste des membres
echo -e "\n${YELLOW}📋 Test de récupération de la liste des membres...${NC}"
LIST_RESPONSE=$(curl -s -X GET "$BASE_URL/membres/" \
    -H "Authorization: Token $TOKEN")

if echo "$LIST_RESPONSE" | grep -q "\["; then
    MEMBRE_COUNT=$(echo "$LIST_RESPONSE" | grep -o '"id":[0-9]*' | wc -l)
    echo -e "${GREEN}✅ $MEMBRE_COUNT membres récupérés${NC}"
else
    echo -e "${RED}❌ Erreur lors de la récupération${NC}"
    echo "Réponse: $LIST_RESPONSE"
fi

# 4. Test de récupération d'un membre spécifique
echo -e "\n${YELLOW}👤 Test de récupération du membre $MEMBRE_ID...${NC}"
GET_RESPONSE=$(curl -s -X GET "$BASE_URL/membres/$MEMBRE_ID/" \
    -H "Authorization: Token $TOKEN")

if echo "$GET_RESPONSE" | grep -q '"nom"'; then
    NOM=$(echo "$GET_RESPONSE" | grep -o '"nom":"[^"]*"' | cut -d'"' -f4)
    PRENOM=$(echo "$GET_RESPONSE" | grep -o '"prenom":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Membre récupéré: $PRENOM $NOM${NC}"
else
    echo -e "${RED}❌ Erreur lors de la récupération${NC}"
    echo "Réponse: $GET_RESPONSE"
fi

# 5. Test de mise à jour d'un membre
echo -e "\n${YELLOW}✏️ Test de mise à jour du membre $MEMBRE_ID...${NC}"
UPDATE_RESPONSE=$(curl -s -X PATCH "$BASE_URL/membres/$MEMBRE_ID/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d '{
        "profession": "Développeur Senior",
        "ville": "Lyon",
        "telephone": "+33456789012"
    }')

if echo "$UPDATE_RESPONSE" | grep -q "Modification effectuée"; then
    echo -e "${GREEN}✅ Membre mis à jour avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de la mise à jour${NC}"
    echo "Réponse: $UPDATE_RESPONSE"
fi

# 6. Test de recherche de membres
echo -e "\n${YELLOW}🔍 Test de recherche de membres...${NC}"
SEARCH_RESPONSE=$(curl -s -X GET "$BASE_URL/membres/?search=Dupont" \
    -H "Authorization: Token $TOKEN")

if echo "$SEARCH_RESPONSE" | grep -q "\["; then
    SEARCH_COUNT=$(echo "$SEARCH_RESPONSE" | grep -o '"id":[0-9]*' | wc -l)
    echo -e "${GREEN}✅ $SEARCH_COUNT membres trouvés pour 'Dupont'${NC}"
else
    echo -e "${RED}❌ Erreur lors de la recherche${NC}"
    echo "Réponse: $SEARCH_RESPONSE"
fi

# 7. Test de tri des membres
echo -e "\n${YELLOW}📊 Test de tri des membres...${NC}"
ORDER_RESPONSE=$(curl -s -X GET "$BASE_URL/membres/?ordering=nom" \
    -H "Authorization: Token $TOKEN")

if echo "$ORDER_RESPONSE" | grep -q "\["; then
    ORDER_COUNT=$(echo "$ORDER_RESPONSE" | grep -o '"id":[0-9]*' | wc -l)
    echo -e "${GREEN}✅ $ORDER_COUNT membres triés par nom${NC}"
else
    echo -e "${RED}❌ Erreur lors du tri${NC}"
    echo "Réponse: $ORDER_RESPONSE"
fi

# 8. Test de création de plusieurs membres
echo -e "\n${YELLOW}👥 Test de création de plusieurs membres...${NC}"
MULTIPLE_RESPONSE=$(curl -s -X POST "$BASE_URL/membres/store_multiple/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d '[
        {
            "nom": "Martin",
            "prenom": "Sophie",
            "adresse": "456 Avenue des Fleurs",
            "ville": "Marseille",
            "telephone": "+33456789012",
            "email": "sophie.martin@email.com",
            "profession": "Designer",
            "nationalite": "Française",
            "color": "2",
            "genre": "feminin",
            "date_naissance": "1988-12-03",
            "situation_matrimoniale": "celibataire",
            "statut": "inscrit"
        },
        {
            "nom": "Bernard",
            "prenom": "Pierre",
            "adresse": "789 Boulevard Central",
            "ville": "Toulouse",
            "telephone": "+33567890123",
            "email": "pierre.bernard@email.com",
            "profession": "Médecin",
            "nationalite": "Française",
            "color": "3",
            "genre": "masculin",
            "date_naissance": "1975-08-20",
            "situation_matrimoniale": "marie",
            "statut": "membre"
        }
    ]')

if echo "$MULTIPLE_RESPONSE" | grep -q "Enregistrement effectué"; then
    echo -e "${GREEN}✅ Plusieurs membres créés avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de la création multiple${NC}"
    echo "Réponse: $MULTIPLE_RESPONSE"
fi

# 9. Test d'ajout de tags multiples (nécessite des tags existants)
echo -e "\n${YELLOW}🏷️ Test d'ajout de tags multiples...${NC}"
TAG_RESPONSE=$(curl -s -X POST "$BASE_URL/membres/taged_multiple/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d "{
        \"tag_ids\": [1, 2],
        \"membre_ids\": [$MEMBRE_ID]
    }")

if echo "$TAG_RESPONSE" | grep -q "Tags ajoutés"; then
    echo -e "${GREEN}✅ Tags ajoutés avec succès${NC}"
else
    echo -e "${YELLOW}⚠️ Erreur lors de l'ajout de tags (peut nécessiter des tags existants)${NC}"
    echo "Réponse: $TAG_RESPONSE"
fi

# 10. Test de suppression d'un membre
echo -e "\n${YELLOW}🗑️ Test de suppression du membre $MEMBRE_ID...${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/membres/$MEMBRE_ID/" \
    -H "Authorization: Token $TOKEN")

if echo "$DELETE_RESPONSE" | grep -q "Suppression effectuée"; then
    echo -e "${GREEN}✅ Membre supprimé avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de la suppression${NC}"
    echo "Réponse: $DELETE_RESPONSE"
fi

# 11. Test de suppression multiple
echo -e "\n${YELLOW}🗑️ Test de suppression multiple...${NC}"
# D'abord récupérer la liste pour avoir des IDs
LIST_FOR_DELETE=$(curl -s -X GET "$BASE_URL/membres/" \
    -H "Authorization: Token $TOKEN")

if echo "$LIST_FOR_DELETE" | grep -q "\["; then
    # Extraire les 2 derniers IDs (si disponibles)
    IDS=$(echo "$LIST_FOR_DELETE" | grep -o '"id":[0-9]*' | tail -2 | cut -d':' -f2 | tr '\n' ',' | sed 's/,$//')
    if [ ! -z "$IDS" ]; then
        DELETE_MULTIPLE_RESPONSE=$(curl -s -X POST "$BASE_URL/membres/destroy_multiple/" \
            -H "Content-Type: application/json" \
            -H "Authorization: Token $TOKEN" \
            -d "{\"ids\": [$IDS]}")
        
        if echo "$DELETE_MULTIPLE_RESPONSE" | grep -q "Suppression des éléments"; then
            echo -e "${GREEN}✅ Suppression multiple réussie${NC}"
        else
            echo -e "${RED}❌ Erreur lors de la suppression multiple${NC}"
            echo "Réponse: $DELETE_MULTIPLE_RESPONSE"
        fi
    else
        echo -e "${YELLOW}⚠️ Aucun membre disponible pour la suppression multiple${NC}"
    fi
else
    echo -e "${RED}❌ Impossible de récupérer la liste pour la suppression multiple${NC}"
fi

echo -e "\n${BLUE}=================================================="
echo -e "✅ Tests terminés !${NC}" 