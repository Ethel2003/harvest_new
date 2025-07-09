#!/usr/bin/env python3
"""
Script de migration des données existantes vers le nouveau modèle Regroupements
Migre les relations existantes entre Membres et Groupes via les modèles Degre et Integration
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
django.setup()

from core.models import Membre, Groupe, Regroupements, Degre, Integration


def migrate_degre_to_regroupements():
    """
    Migre les données de la table Degre vers Regroupements
    """
    print("🔄 Migration des données Degre vers Regroupements...")
    
    try:
        # Récupérer tous les degrés existants
        degres = Degre.objects.all()
        print(f"📊 {degres.count()} degrés trouvés")
        
        regroupements_crees = 0
        regroupements_existants = 0
        
        for degre in degres:
            # Vérifier si un regroupement existe déjà
            regroupement_existant = Regroupements.objects.filter(
                membre=degre.membre,
                groupe=degre.groupe
            ).first()
            
            if regroupement_existant:
                print(f"  ⚠️  Regroupement existant pour Membre {degre.membre.id} - Groupe {degre.groupe.id}")
                regroupements_existants += 1
                continue
            
            # Créer un nouveau regroupement
            regroupement = Regroupements.objects.create(
                membre=degre.membre,
                groupe=degre.groupe,
                date_inscription=degre.created_at or datetime.now(),
                actif=True
            )
            
            print(f"  ✅ Créé: Membre {degre.membre.nom} {degre.membre.prenom} -> Groupe {degre.groupe.nom}")
            regroupements_crees += 1
        
        print(f"📈 Migration terminée:")
        print(f"  - Regroupements créés: {regroupements_crees}")
        print(f"  - Regroupements existants: {regroupements_existants}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration Degre: {e}")
        return False


def migrate_integration_to_regroupements():
    """
    Migre les données de la table Integration vers Regroupements
    """
    print("\n🔄 Migration des données Integration vers Regroupements...")
    
    try:
        # Récupérer toutes les intégrations existantes
        integrations = Integration.objects.all()
        print(f"📊 {integrations.count()} intégrations trouvées")
        
        regroupements_crees = 0
        regroupements_existants = 0
        
        for integration in integrations:
            # Vérifier si un regroupement existe déjà
            regroupement_existant = Regroupements.objects.filter(
                membre=integration.membre,
                groupe=integration.groupe
            ).first()
            
            if regroupement_existant:
                print(f"  ⚠️  Regroupement existant pour Membre {integration.membre.id} - Groupe {integration.groupe.id}")
                regroupements_existants += 1
                continue
            
            # Créer un nouveau regroupement
            regroupement = Regroupements.objects.create(
                membre=integration.membre,
                groupe=integration.groupe,
                date_inscription=integration.created_at or datetime.now(),
                actif=True
            )
            
            print(f"  ✅ Créé: Membre {integration.membre.nom} {integration.membre.prenom} -> Groupe {integration.groupe.nom}")
            regroupements_crees += 1
        
        print(f"📈 Migration terminée:")
        print(f"  - Regroupements créés: {regroupements_crees}")
        print(f"  - Regroupements existants: {regroupements_existants}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration Integration: {e}")
        return False


def verify_migration():
    """
    Vérifie que la migration s'est bien passée
    """
    print("\n🔍 Vérification de la migration...")
    
    try:
        # Compter les regroupements
        total_regroupements = Regroupements.objects.count()
        regroupements_actifs = Regroupements.objects.filter(actif=True).count()
        
        print(f"📊 Statistiques des regroupements:")
        print(f"  - Total: {total_regroupements}")
        print(f"  - Actifs: {regroupements_actifs}")
        
        # Vérifier les groupes avec des membres
        groupes_avec_membres = Groupe.objects.filter(regroupements__actif=True).distinct().count()
        total_groupes = Groupe.objects.count()
        
        print(f"📊 Statistiques des groupes:")
        print(f"  - Total groupes: {total_groupes}")
        print(f"  - Groupes avec membres: {groupes_avec_membres}")
        
        # Afficher quelques exemples
        print(f"\n📋 Exemples de regroupements:")
        regroupements_exemples = Regroupements.objects.select_related('membre', 'groupe')[:5]
        
        for reg in regroupements_exemples:
            print(f"  - {reg.membre.nom} {reg.membre.prenom} -> {reg.groupe.nom} (Actif: {reg.actif})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False


def generate_statistics():
    """
    Génère des statistiques détaillées après la migration
    """
    print("\n📈 Génération des statistiques détaillées...")
    
    try:
        from django.db.models import Count, Q
        
        # Statistiques par groupe
        groupes_stats = Groupe.objects.annotate(
            nombre_membres=Count('regroupements', filter=Q(regroupements__actif=True))
        ).values('id', 'nom', 'nombre_membres').order_by('-nombre_membres')
        
        print(f"📊 Membres par groupe:")
        for groupe in groupes_stats:
            print(f"  - {groupe['nom']}: {groupe['nombre_membres']} membres")
        
        # Statistiques globales
        total_membres = Membre.objects.count()
        membres_avec_groupes = Membre.objects.filter(regroupements__actif=True).distinct().count()
        
        print(f"\n📊 Statistiques globales:")
        print(f"  - Total membres: {total_membres}")
        print(f"  - Membres dans des groupes: {membres_avec_groupes}")
        print(f"  - Pourcentage: {(membres_avec_groupes/total_membres*100):.1f}%" if total_membres > 0 else "  - Pourcentage: 0%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des statistiques: {e}")
        return False


def run_migration():
    """
    Exécute la migration complète
    """
    print("🚀 DÉBUT DE LA MIGRATION DES DONNÉES")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Migration des degrés
    if not migrate_degre_to_regroupements():
        print("❌ Échec de la migration des degrés")
        return False
    
    # Migration des intégrations
    if not migrate_integration_to_regroupements():
        print("❌ Échec de la migration des intégrations")
        return False
    
    # Vérification
    if not verify_migration():
        print("❌ Échec de la vérification")
        return False
    
    # Statistiques
    if not generate_statistics():
        print("❌ Échec de la génération des statistiques")
        return False
    
    print("\n" + "="*60)
    print("✅ MIGRATION TERMINÉE AVEC SUCCÈS")
    print("="*60)
    print("📊 Le modèle Regroupements est maintenant opérationnel")
    print("🔗 Toutes les relations existantes ont été migrées")
    print("📈 Les statistiques de groupes incluent le nombre de membres")
    print("🎯 Vous pouvez maintenant utiliser les nouvelles fonctionnalités")
    
    return True


if __name__ == "__main__":
    # Demander confirmation
    print("⚠️  ATTENTION: Ce script va migrer les données existantes vers le nouveau modèle Regroupements")
    print("📋 Cela va créer des enregistrements dans la table Regroupements basés sur:")
    print("   - Les relations existantes dans la table Degre")
    print("   - Les relations existantes dans la table Integration")
    
    confirmation = input("\n❓ Voulez-vous continuer? (oui/non): ").lower().strip()
    
    if confirmation in ['oui', 'o', 'yes', 'y']:
        run_migration()
    else:
        print("❌ Migration annulée") 