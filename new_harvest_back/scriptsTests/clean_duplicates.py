#!/usr/bin/env python3
"""
Script pour nettoyer les doublons avant d'appliquer les contraintes d'unicité
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harvest_api.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from core.models import Membre, Groupe
from django.db.models import Count


def clean_duplicate_groupes():
    """
    Nettoie les doublons de groupes en gardant le plus récent
    """
    print("🧹 Nettoyage des doublons de groupes...")
    
    try:
        # Trouver les groupes avec des noms dupliqués
        groupes_duplicates = Groupe.objects.values('nom').annotate(
            count=Count('id')
        ).filter(count__gt=1, nom__isnull=False)
        
        print(f"📊 {len(groupes_duplicates)} noms de groupes dupliqués trouvés")
        
        for duplicate in groupes_duplicates:
            nom = duplicate['nom']
            groupes = Groupe.objects.filter(nom=nom).order_by('-created_at')
            
            # Garder le premier (le plus récent) et supprimer les autres
            groupe_to_keep = groupes.first()
            groupes_to_delete = groupes[1:]
            
            print(f"  🔄 Groupe '{nom}':")
            print(f"    - Gardé: ID {groupe_to_keep.id} (créé le {groupe_to_keep.created_at})")
            
            for groupe in groupes_to_delete:
                print(f"    - Supprimé: ID {groupe.id} (créé le {groupe.created_at})")
                groupe.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage des groupes: {e}")
        return False


def clean_duplicate_membres():
    """
    Nettoie les doublons de membres en gardant le plus récent
    """
    print("\n🧹 Nettoyage des doublons de membres...")
    
    try:
        # Trouver les membres avec des combinaisons nom/prénom dupliquées
        membres_duplicates = Membre.objects.values('nom', 'prenom').annotate(
            count=Count('id')
        ).filter(count__gt=1, nom__isnull=False, prenom__isnull=False)
        
        print(f"📊 {len(membres_duplicates)} combinaisons nom/prénom dupliquées trouvées")
        
        for duplicate in membres_duplicates:
            nom = duplicate['nom']
            prenom = duplicate['prenom']
            membres = Membre.objects.filter(nom=nom, prenom=prenom).order_by('-created_at')
            
            # Garder le premier (le plus récent) et supprimer les autres
            membre_to_keep = membres.first()
            membres_to_delete = membres[1:]
            
            print(f"  🔄 Membre '{prenom} {nom}':")
            print(f"    - Gardé: ID {membre_to_keep.id} (créé le {membre_to_keep.created_at})")
            
            for membre in membres_to_delete:
                print(f"    - Supprimé: ID {membre.id} (créé le {membre.created_at})")
                membre.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage des membres: {e}")
        return False


def verify_cleanup():
    """
    Vérifie que le nettoyage s'est bien passé
    """
    print("\n🔍 Vérification du nettoyage...")
    
    try:
        # Vérifier les groupes
        groupes_duplicates = Groupe.objects.values('nom').annotate(
            count=Count('id')
        ).filter(count__gt=1, nom__isnull=False)
        
        if groupes_duplicates.exists():
            print(f"⚠️  {len(groupes_duplicates)} groupes dupliqués restent")
            for duplicate in groupes_duplicates:
                print(f"  - Nom: {duplicate['nom']}")
        else:
            print("✅ Aucun groupe dupliqué restant")
        
        # Vérifier les membres
        membres_duplicates = Membre.objects.values('nom', 'prenom').annotate(
            count=Count('id')
        ).filter(count__gt=1, nom__isnull=False, prenom__isnull=False)
        
        if membres_duplicates.exists():
            print(f"⚠️  {len(membres_duplicates)} membres dupliqués restent")
            for duplicate in membres_duplicates:
                print(f"  - {duplicate['prenom']} {duplicate['nom']}")
        else:
            print("✅ Aucun membre dupliqué restant")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False


def run_cleanup():
    """
    Exécute le nettoyage complet
    """
    print("🚀 DÉBUT DU NETTOYAGE DES DOUBLONS")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Nettoyage des groupes
    if not clean_duplicate_groupes():
        print("❌ Échec du nettoyage des groupes")
        return False
    
    # Nettoyage des membres
    if not clean_duplicate_membres():
        print("❌ Échec du nettoyage des membres")
        return False
    
    # Vérification
    if not verify_cleanup():
        print("❌ Échec de la vérification")
        return False
    
    print("\n" + "="*60)
    print("✅ NETTOYAGE TERMINÉ AVEC SUCCÈS")
    print("="*60)
    print("🧹 Tous les doublons ont été supprimés")
    print("📊 Les données sont maintenant prêtes pour les contraintes d'unicité")
    print("🎯 Vous pouvez maintenant appliquer les migrations")
    
    return True


if __name__ == "__main__":
    # Demander confirmation
    print("⚠️  ATTENTION: Ce script va supprimer les doublons de groupes et de membres")
    print("📋 Cela va:")
    print("   - Supprimer les groupes avec des noms dupliqués (garde le plus récent)")
    print("   - Supprimer les membres avec des combinaisons nom/prénom dupliquées (garde le plus récent)")
    
    confirmation = input("\n❓ Voulez-vous continuer? (oui/non): ").lower().strip()
    
    if confirmation in ['oui', 'o', 'yes', 'y']:
        run_cleanup()
    else:
        print("❌ Nettoyage annulé") 