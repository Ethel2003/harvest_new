#!/usr/bin/env python3
"""
Script utilitaire pour obtenir les IDs existants dans la base de données
Utile pour configurer les scripts de test
"""

import os
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')

import django
django.setup()

from core.models import Membre, Etape, Tag, Integration, Etiquetage, Groupe

def afficher_membres():
    """Affiche tous les membres avec leurs IDs"""
    print("\n👥 MEMBRES DISPONIBLES:")
    print("-" * 50)
    
    membres = Membre.objects.all().order_by('id')
    if membres:
        for membre in membres:
            print(f"ID: {membre.id:3d} | {membre.prenom} {membre.nom} | {membre.email}")
    else:
        print("Aucun membre trouvé")
    
    return [m.id for m in membres]

def afficher_etapes():
    """Affiche toutes les étapes avec leurs IDs"""
    print("\n📋 ÉTAPES DISPONIBLES:")
    print("-" * 50)
    
    etapes = Etape.objects.all().order_by('id')
    if etapes:
        for etape in etapes:
            print(f"ID: {etape.id:3d} | {etape.libelle} | {etape.description}")
    else:
        print("Aucune étape trouvée")
    
    return [e.id for e in etapes]

def afficher_tags():
    """Affiche tous les tags avec leurs IDs"""
    print("\n🏷️ TAGS DISPONIBLES:")
    print("-" * 50)
    
    tags = Tag.objects.all().order_by('id')
    if tags:
        for tag in tags:
            print(f"ID: {tag.id:3d} | {tag.name}")
    else:
        print("Aucun tag trouvé")
    
    return [t.id for t in tags]

def afficher_groupes():
    """Affiche tous les groupes avec leurs IDs"""
    print("\n👥 GROUPES DISPONIBLES:")
    print("-" * 50)
    
    groupes = Groupe.objects.all().order_by('id')
    if groupes:
        for groupe in groupes:
            print(f"ID: {groupe.id:3d} | {groupe.nom} | {groupe.description}")
    else:
        print("Aucun groupe trouvé")
    
    return [g.id for g in groupes]

def afficher_integrations():
    """Affiche toutes les intégrations existantes"""
    print("\n🔗 INTÉGRATIONS EXISTANTES:")
    print("-" * 50)
    
    integrations = Integration.objects.all().order_by('id')
    if integrations:
        for integration in integrations:
            print(f"ID: {integration.id:3d} | Membre: {integration.membre.prenom} {integration.membre.nom} | Étape: {integration.etape.libelle} | Membership: {integration.membership}")
    else:
        print("Aucune intégration trouvée")
    
    return [i.id for i in integrations]

def afficher_etiquetages():
    """Affiche tous les étiquetages existants"""
    print("\n🏷️ ÉTIQUETAGES EXISTANTS:")
    print("-" * 50)
    
    etiquetages = Etiquetage.objects.all().order_by('id')
    if etiquetages:
        for etiquetage in etiquetages:
            print(f"ID: {etiquetage.id:3d} | Membre: {etiquetage.membre.prenom} {etiquetage.membre.nom} | Tag: {etiquetage.tag.name}")
    else:
        print("Aucun étiquetage trouvé")
    
    return [e.id for e in etiquetages]

def afficher_statistiques():
    """Affiche les statistiques de la base de données"""
    print("\n📊 STATISTIQUES DE LA BASE DE DONNÉES:")
    print("-" * 50)
    
    print(f"Membres: {Membre.objects.count()}")
    print(f"Étapes: {Etape.objects.count()}")
    print(f"Tags: {Tag.objects.count()}")
    print(f"Groupes: {Groupe.objects.count()}")
    print(f"Intégrations: {Integration.objects.count()}")
    print(f"Étiquetages: {Etiquetage.objects.count()}")

def generer_config_test():
    """Génère une configuration de test avec les IDs existants"""
    print("\n⚙️ CONFIGURATION POUR LES TESTS:")
    print("-" * 50)
    
    membres = Membre.objects.all()[:3]  # Prendre les 3 premiers
    etapes = Etape.objects.all()[:3]    # Prendre les 3 premiers
    tags = Tag.objects.all()[:3]        # Prendre les 3 premiers
    
    if membres and etapes and tags:
        print("Configuration recommandée pour les tests:")
        print(f"membre_id = {membres[0].id}  # {membres[0].prenom} {membres[0].nom}")
        print(f"etape_id = {etapes[0].id}    # {etapes[0].libelle}")
        print(f"tag_id = {tags[0].id}        # {tags[0].name}")
        
        print("\nConfiguration pour les tests multiples:")
        print(f"membres_ids = [{', '.join(str(m.id) for m in membres)}]")
        print(f"etapes_ids = [{', '.join(str(e.id) for e in etapes)}]")
        print(f"tags_ids = [{', '.join(str(t.id) for t in tags)}]")
    else:
        print("❌ Données insuffisantes pour générer une configuration")

def afficher_relations():
    """Affiche les relations existantes"""
    print("\n🔗 RELATIONS EXISTANTES:")
    print("-" * 50)
    
    # Membres avec intégrations
    membres_avec_integrations = Membre.objects.filter(integration__isnull=False).distinct()
    print(f"Membres avec intégrations: {membres_avec_integrations.count()}")
    for membre in membres_avec_integrations[:5]:  # Afficher les 5 premiers
        integrations = membre.integration_set.all()
        print(f"  - {membre.prenom} {membre.nom} (ID: {membre.id}): {integrations.count()} intégrations")
    
    # Membres avec étiquetages
    membres_avec_etiquetages = Membre.objects.filter(etiquetage__isnull=False).distinct()
    print(f"\nMembres avec étiquetages: {membres_avec_etiquetages.count()}")
    for membre in membres_avec_etiquetages[:5]:  # Afficher les 5 premiers
        etiquetages = membre.etiquetage_set.all()
        print(f"  - {membre.prenom} {membre.nom} (ID: {membre.id}): {etiquetages.count()} étiquetages")

def main():
    """Fonction principale"""
    print("🔍 OBTENIR LES IDs DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    try:
        # Afficher toutes les informations
        afficher_statistiques()
        afficher_membres()
        afficher_etapes()
        afficher_tags()
        afficher_groupes()
        afficher_integrations()
        afficher_etiquetages()
        afficher_relations()
        generer_config_test()
        
        print("\n✅ Affichage terminé!")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main() 