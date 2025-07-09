#!/usr/bin/env python3
"""
Script pour créer des données de test pour les endpoints de filtrage des membres
"""

import os
import sys
import django
from datetime import date

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
django.setup()

from core.models import (
    Membre, Groupe, Etape, Tag, Regroupements, Integration, Etiquetage,
    CategorieAge, Critere
)

def creer_donnees_test():
    """Crée des données de test pour les endpoints de filtrage"""
    
    print("🔧 Création des données de test...")
    
    # Créer des catégories d'âge
    print("  - Création des catégories d'âge...")
    cat_jeune, _ = CategorieAge.objects.get_or_create(
        libelle="Jeunes (18-25 ans)",
        defaults={'min_age': 18, 'max_age': 25}
    )
    cat_adulte, _ = CategorieAge.objects.get_or_create(
        libelle="Adultes (26-50 ans)",
        defaults={'min_age': 26, 'max_age': 50}
    )
    
    # Créer des critères
    print("  - Création des critères...")
    critere_jeunes, _ = Critere.objects.get_or_create(
        libelle="Jeunes",
        defaults={'description': "Critère pour les jeunes"}
    )
    critere_adultes, _ = Critere.objects.get_or_create(
        libelle="Adultes",
        defaults={'description': "Critère pour les adultes"}
    )
    
    # Créer des groupes
    print("  - Création des groupes...")
    groupe_jeunes, _ = Groupe.objects.get_or_create(
        nom="Groupe Jeunes",
        defaults={
            'description': "Groupe pour les jeunes membres",
            'color': 'blue',
            'critere': critere_jeunes
        }
    )
    groupe_adultes, _ = Groupe.objects.get_or_create(
        nom="Groupe Adultes",
        defaults={
            'description': "Groupe pour les adultes",
            'color': 'green',
            'critere': critere_adultes
        }
    )
    groupe_chorale, _ = Groupe.objects.get_or_create(
        nom="Chorale",
        defaults={
            'description': "Groupe de chant",
            'color': 'purple',
            'critere': critere_adultes
        }
    )
    
    # Créer des étapes
    print("  - Création des étapes...")
    etape_accueil, _ = Etape.objects.get_or_create(
        libelle="Accueil",
        defaults={'description': "Étape d'accueil des nouveaux membres"}
    )
    etape_formation, _ = Etape.objects.get_or_create(
        libelle="Formation",
        defaults={'description': "Étape de formation"}
    )
    etape_integration, _ = Etape.objects.get_or_create(
        libelle="Intégration",
        defaults={'description': "Étape d'intégration complète"}
    )
    
    # Créer des tags
    print("  - Création des tags...")
    tag_actif, _ = Tag.objects.get_or_create(name="Actif")
    tag_volontaire, _ = Tag.objects.get_or_create(name="Volontaire")
    tag_leader, _ = Tag.objects.get_or_create(name="Leader")
    tag_musicien, _ = Tag.objects.get_or_create(name="Musicien")
    
    # Créer des membres
    print("  - Création des membres...")
    membres_data = [
        {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.dupont@test.com',
            'telephone': '0123456789',
            'genre': 'masculin',
            'date_naissance': date(1995, 5, 15),
            'categorie_age': cat_jeune,
            'statut': 'membre'
        },
        {
            'nom': 'Martin',
            'prenom': 'Marie',
            'email': 'marie.martin@test.com',
            'telephone': '0123456790',
            'genre': 'feminin',
            'date_naissance': date(1988, 8, 22),
            'categorie_age': cat_adulte,
            'statut': 'membre'
        },
        {
            'nom': 'Bernard',
            'prenom': 'Pierre',
            'email': 'pierre.bernard@test.com',
            'telephone': '0123456791',
            'genre': 'masculin',
            'date_naissance': date(1992, 3, 10),
            'categorie_age': cat_jeune,
            'statut': 'membre'
        },
        {
            'nom': 'Petit',
            'prenom': 'Sophie',
            'email': 'sophie.petit@test.com',
            'telephone': '0123456792',
            'genre': 'feminin',
            'date_naissance': date(1985, 12, 5),
            'categorie_age': cat_adulte,
            'statut': 'membre'
        },
        {
            'nom': 'Robert',
            'prenom': 'Luc',
            'email': 'luc.robert@test.com',
            'telephone': '0123456793',
            'genre': 'masculin',
            'date_naissance': date(1990, 7, 18),
            'categorie_age': cat_jeune,
            'statut': 'membre'
        }
    ]
    
    membres = []
    for data in membres_data:
        membre, created = Membre.objects.get_or_create(
            nom=data['nom'],
            prenom=data['prenom'],
            defaults=data
        )
        membres.append(membre)
        if created:
            print(f"    ✓ Créé: {membre.prenom} {membre.nom}")
    
    # Créer des regroupements
    print("  - Création des regroupements...")
    regroupements_data = [
        (membres[0], groupe_jeunes),      # Jean Dupont -> Groupe Jeunes
        (membres[1], groupe_adultes),     # Marie Martin -> Groupe Adultes
        (membres[1], groupe_chorale),     # Marie Martin -> Chorale
        (membres[2], groupe_jeunes),      # Pierre Bernard -> Groupe Jeunes
        (membres[3], groupe_adultes),     # Sophie Petit -> Groupe Adultes
        (membres[4], groupe_chorale),     # Luc Robert -> Chorale
    ]
    
    for membre, groupe in regroupements_data:
        regroupement, created = Regroupements.objects.get_or_create(
            membre=membre,
            groupe=groupe,
            defaults={'actif': True}
        )
        if created:
            print(f"    ✓ {membre.prenom} {membre.nom} -> {groupe.nom}")
    
    # Créer des intégrations (étapes)
    print("  - Création des intégrations...")
    integrations_data = [
        (membres[0], etape_accueil),      # Jean Dupont -> Accueil
        (membres[1], etape_formation),    # Marie Martin -> Formation
        (membres[1], etape_integration),  # Marie Martin -> Intégration
        (membres[2], etape_accueil),      # Pierre Bernard -> Accueil
        (membres[3], etape_integration),  # Sophie Petit -> Intégration
        (membres[4], etape_formation),    # Luc Robert -> Formation
    ]
    
    for membre, etape in integrations_data:
        integration, created = Integration.objects.get_or_create(
            membre=membre,
            etape=etape,
            defaults={'created_at': date.today()}
        )
        if created:
            print(f"    ✓ {membre.prenom} {membre.nom} -> {etape.libelle}")
    
    # Créer des étiquetages (tags)
    print("  - Création des étiquetages...")
    etiquetages_data = [
        (membres[0], tag_actif),          # Jean Dupont -> Actif
        (membres[1], tag_volontaire),     # Marie Martin -> Volontaire
        (membres[1], tag_leader),         # Marie Martin -> Leader
        (membres[2], tag_actif),          # Pierre Bernard -> Actif
        (membres[3], tag_volontaire),     # Sophie Petit -> Volontaire
        (membres[4], tag_musicien),       # Luc Robert -> Musicien
    ]
    
    for membre, tag in etiquetages_data:
        etiquetage, created = Etiquetage.objects.get_or_create(
            membre=membre,
            tag=tag
        )
        if created:
            print(f"    ✓ {membre.prenom} {membre.nom} -> {tag.name}")
    
    print("\n✅ Données de test créées avec succès!")
    
    # Afficher un résumé
    print("\n📊 RÉSUMÉ DES DONNÉES CRÉÉES:")
    print(f"  - Membres: {Membre.objects.count()}")
    print(f"  - Groupes: {Groupe.objects.count()}")
    print(f"  - Étapes: {Etape.objects.count()}")
    print(f"  - Tags: {Tag.objects.count()}")
    print(f"  - Regroupements: {Regroupements.objects.count()}")
    print(f"  - Intégrations: {Integration.objects.count()}")
    print(f"  - Étiquetages: {Etiquetage.objects.count()}")
    
    # Afficher les IDs pour les tests
    print("\n🔍 IDs POUR LES TESTS:")
    print(f"  - Groupes: {list(Groupe.objects.values_list('id', 'nom'))}")
    print(f"  - Étapes: {list(Etape.objects.values_list('id', 'libelle'))}")
    print(f"  - Tags: {list(Tag.objects.values_list('id', 'name'))}")
    
    print("\n🚀 Vous pouvez maintenant tester les endpoints avec ces données!")

def nettoyer_donnees_test():
    """Nettoie les données de test créées"""
    print("🧹 Nettoyage des données de test...")
    
    # Supprimer dans l'ordre pour éviter les erreurs de clés étrangères
    Etiquetage.objects.all().delete()
    Integration.objects.all().delete()
    Regroupements.objects.all().delete()
    Membre.objects.all().delete()
    Tag.objects.all().delete()
    Etape.objects.all().delete()
    Groupe.objects.all().delete()
    Critere.objects.all().delete()
    CategorieAge.objects.all().delete()
    
    print("✅ Données de test supprimées!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestion des données de test pour les endpoints de filtrage")
    parser.add_argument('--clean', action='store_true', help='Nettoyer les données de test existantes')
    parser.add_argument('--create', action='store_true', help='Créer de nouvelles données de test')
    
    args = parser.parse_args()
    
    if args.clean:
        nettoyer_donnees_test()
    elif args.create:
        creer_donnees_test()
    else:
        print("Usage:")
        print("  python creer_donnees_test.py --create  # Créer des données de test")
        print("  python creer_donnees_test.py --clean   # Nettoyer les données de test")
        print("  python creer_donnees_test.py --clean --create  # Nettoyer puis créer") 