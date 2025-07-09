# Importations nécessaires pour les vues Django REST Framework
from django.shortcuts import render, get_object_or_404  # Fonctions de raccourci Django
from django.db.models import Q  # Pour les requêtes complexes
from django.contrib.auth import authenticate  # Pour l'authentification
from django.contrib.auth.models import User  # Modèle utilisateur par défaut
from django.http import JsonResponse, Http404  # Pour retourner des réponses JSON
from django.views.decorators.csrf import csrf_exempt  # Pour désactiver la protection CSRF
from django.utils.decorators import method_decorator  # Pour appliquer des décorateurs aux méthodes
from rest_framework.views import APIView  # Vue API de base
from rest_framework.response import Response  # Pour retourner des réponses REST
from rest_framework import status, permissions, viewsets, filters  # Composants REST framework
from rest_framework.authtoken.models import Token  # Modèle de token d'authentification
from rest_framework.decorators import action  # Décorateur pour actions personnalisées
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny  # Permissions
from .models import (
    UserProfile, Membre, CategorieAge, Departement, Critere, Groupe, Regroupements, Etape, Tag, Degre,
    Appartenance, Integration, Etiquetage, Enfant, Attachement, Formulaire,
    Champ, CategorieMotifRdv, DisponibiliteRdv, RoleIntervenant, Intervenant,
    Evenement, EvenementAffectation, Rdv, Defi, Victoire, FaitMarquant, Serviteurs
)
from .serializers import (
    UserSerializer, UserProfileSerializer, MembreSerializer, CategorieAgeSerializer, DepartementSerializer,
    CritereSerializer, GroupeSerializer, RegroupementsSerializer, EtapeSerializer, TagSerializer, DegreSerializer,
    AppartenanceSerializer, IntegrationSerializer, EtiquetageSerializer, EnfantSerializer,
    AttachementSerializer, FormulaireSerializer, ChampSerializer, CategorieMotifRdvSerializer,
    DisponibiliteRdvSerializer, RoleIntervenantSerializer, IntervenantSerializer, EvenementSerializer,
    EvenementAffectationSerializer, RdvSerializer, DefiSerializer, VictoireSerializer, FaitMarquantSerializer, ServiteursSerializer
)
from django.utils import timezone
from django.db import IntegrityError

class BaseViewSet(viewsets.ModelViewSet):
    """
    Classe de base pour tous les ViewSets qui fournit les opérations CRUD communes à tous les modèles.
    Cette classe hérite de ModelViewSet qui inclut déjà les méthodes list, create, retrieve, update,
    partial_update et destroy. Nous les redéfinissons ici pour personnaliser les réponses.    
    """
    # Configuration des filtres pour la recherche et le tri
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['__all__']  # Permet de rechercher dans tous les champs par défaut
    ordering_fields = ['__all__']  # Permet de trier sur tous les champs par défaut
    
    def list(self, request, *args, **kwargs):
        """
        Récupère la liste de tous les objets du modèle avec pagination.
        Correspond à GET /api/{model}/
        """
        # Filtrer le queryset selon les paramètres de recherche et de tri
        queryset = self.filter_queryset(self.get_queryset())
        
        # Paginer les résultats si nécessaire
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        # Si pas de pagination, renvoyer tous les résultats
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Crée un nouvel objet du modèle.
        Correspond à POST /api/{model}/
        """
        # Valider les données reçues
        serializer = self.get_serializer(data=request.data.get('data', {}))
        serializer.is_valid(raise_exception=True)  # Lève une exception si les données sont invalides
        
        # Créer l'objet en base de données
        self.perform_create(serializer)
        
        # Préparer les en-têtes de la réponse
        headers = self.get_success_headers(serializer.data)
        
        # Renvoyer une réponse avec un message de succès et les données de l'objet créé
        return Response({
            "message": "Nouveau élément créé avec succès !", 
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """
        Met à jour un objet existant du modèle.
        Correspond à PUT /api/{model}/{id}/
        """
        # Déterminer si c'est une mise à jour partielle (PATCH) ou complète (PUT)
        partial = kwargs.pop('partial', False)
        
        # Récupérer l'instance à mettre à jour
        instance = self.get_object()
        
        # Valider les données reçues
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)  # Lève une exception si les données sont invalides
        
        # Mettre à jour l'objet en base de données
        self.perform_update(serializer)
        
        # Renvoyer une réponse avec un message de succès et les données de l'objet mis à jour
        return Response({
            "message": "Modification effectuée avec succès !", 
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        Supprime un objet existant du modèle.
        Correspond à DELETE /api/{model}/{id}/
        """
        # Récupérer l'instance à supprimer
        instance = self.get_object()
        
        # Supprimer l'objet de la base de données
        self.perform_destroy(instance)
        
        # Renvoyer une réponse avec un message de succès
        return Response({
            "message": "Suppression effectuée avec succès !"
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def store_multiple(self, request):
        """
        Crée plusieurs objets du modèle en une seule requête.
        Correspond à POST /api/{model}/store_multiple/
        
        Cette méthode est utile pour créer plusieurs objets en une seule requête,
        par exemple lors de l'import de données en masse.
        """
        # Valider les données reçues (liste d'objets)
        serializer = self.get_serializer(data=request.data, many=True)
        
        if serializer.is_valid():
            # Créer les objets en base de données
            serializer.save()
            return Response({'message': 'Enregistrement effectué avec succès !'}, status=status.HTTP_201_CREATED)
            
        # Renvoyer les erreurs de validation si les données sont invalides
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def destroy_multiple(self, request):
        """
        Supprime plusieurs objets du modèle en une seule requête.
        Correspond à POST /api/{model}/destroy_multiple/
        
        Cette méthode est utile pour supprimer plusieurs objets en une seule requête,
        par exemple lors de la suppression en masse.
        """
        # Récupérer les identifiants des objets à supprimer
        ids = request.data.get('ids', [])
        
        # Vérifier que des identifiants ont été fournis
        if not ids:
            return Response({'error': 'Aucun identifiant fourni'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Supprimer les objets de la base de données
        self.get_queryset().filter(id__in=ids).delete()
        
        # Renvoyer une réponse avec un message de succès
        return Response({'message': 'Suppression des éléments sélectionnés effectuée avec succès !'})

class MembreViewSet(BaseViewSet):
    """
    ViewSet pour le modèle Membre.
    Fournit les opérations CRUD standard et des méthodes personnalisées pour gérer
    les relations spécifiques aux membres (tags, étapes, conjoints, enfants, etc.)
    """
    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    ordering_fields = ['nom', 'prenom', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """
        Surcharge de get_queryset pour supporter les filtres par groupes, étapes et tags
        """
        queryset = super().get_queryset()
        
        # Récupération des paramètres de filtrage
        groupes = self.request.query_params.getlist('groupes[]')
        etapes = self.request.query_params.getlist('etapes[]')
        tags = self.request.query_params.getlist('tags[]')
        
        # Filtrage par groupes (via le modèle Regroupements)
        if groupes:
            queryset = queryset.filter(regroupements__groupe_id__in=groupes, regroupements__actif=True).distinct()
        
        # Filtrage par étapes (via le modèle Integration)
        if etapes:
            queryset = queryset.filter(integration__etape_id__in=etapes).distinct()
        
        # Filtrage par tags (via le modèle Etiquetage)
        if tags:
            queryset = queryset.filter(etiquetage__tag_id__in=tags).distinct()
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Création d'un membre avec gestion des erreurs d'unicité
        """
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique_together' in str(e) or 'UNIQUE constraint' in str(e):
                return Response({
                    'success': False,
                    'error': 'Un membre avec cette combinaison nom/prénom existe déjà.',
                    'details': 'La combinaison nom et prénom doit être unique.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Erreur lors de la création du membre.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Mise à jour d'un membre avec gestion des erreurs d'unicité
        """
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique_together' in str(e) or 'UNIQUE constraint' in str(e):
                return Response({
                    'success': False,
                    'error': 'Un membre avec cette combinaison nom/prénom existe déjà.',
                    'details': 'La combinaison nom et prénom doit être unique.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Erreur lors de la mise à jour du membre.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Retourne les statistiques complètes des membres
        Route: GET /api/membres/statistiques/
        """
        try:
            from django.db.models import Count, Q
            
            # Total exact de membres
            total_membres = Membre.objects.count()
            
            # Répartition par genre
            repartition_genre = {}
            for choix in Membre.GENRE_CHOICES:
                count = Membre.objects.filter(genre=choix[0]).count()
                if count > 0:
                    repartition_genre[choix[1]] = count
            
            # Répartition par statut
            repartition_statut = {}
            for choix in Membre.STATUT_CHOICES:
                count = Membre.objects.filter(statut=choix[0]).count()
                if count > 0:
                    repartition_statut[choix[1]] = count
            
            # Répartition par situation matrimoniale
            repartition_situation = {}
            for choix in Membre.SITUATION_CHOICES:
                count = Membre.objects.filter(situation_matrimoniale=choix[0]).count()
                if count > 0:
                    repartition_situation[choix[1]] = count
            
            # Membres par tag (via Etiquetage)
            membres_par_tag = []
            try:
                tag_stats = Tag.objects.annotate(
                    nombre_membres=Count('etiquetage__membre', distinct=True)
                ).filter(nombre_membres__gt=0).values('name', 'nombre_membres')
                
                for tag in tag_stats:
                    membres_par_tag.append({
                        'tag': tag['name'],
                        'nombre': tag['nombre_membres']
                    })
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques par tag: {e}")
            
            # Membres par département (via Serviteurs)
            membres_par_departement = []
            try:
                dept_stats = Departement.objects.annotate(
                    nombre_membres=Count('serviteurs__membre', filter=Q(serviteurs__actif=True), distinct=True)
                ).filter(nombre_membres__gt=0).values('nom', 'nombre_membres')
                
                for dept in dept_stats:
                    membres_par_departement.append({
                        'departement': dept['nom'],
                        'nombre': dept['nombre_membres']
                    })
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques par département: {e}")
            
            # Membres par groupe (via Regroupements)
            membres_par_groupe = []
            try:
                groupe_stats = Groupe.objects.annotate(
                    nombre_membres=Count('regroupements__membre', filter=Q(regroupements__actif=True), distinct=True)
                ).filter(nombre_membres__gt=0).values('nom', 'nombre_membres')
                
                for groupe in groupe_stats:
                    membres_par_groupe.append({
                        'groupe': groupe['nom'],
                        'nombre': groupe['nombre_membres']
                    })
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques par groupe: {e}")
            
            # Statistiques par âge (si date_naissance disponible)
            repartition_age = {}
            try:
                membres_avec_age = Membre.objects.filter(date_naissance__isnull=False).count()
                if membres_avec_age > 0:
                    from datetime import date
                    today = date.today()
                    
                    # Calculer les âges et les catégoriser
                    moins_18 = 0
                    age_18_25 = 0
                    age_26_35 = 0
                    age_36_50 = 0
                    plus_50 = 0
                    
                    for membre in Membre.objects.filter(date_naissance__isnull=False):
                        age = today.year - membre.date_naissance.year - ((today.month, today.day) < (membre.date_naissance.month, membre.date_naissance.day))
                        
                        if age < 18:
                            moins_18 += 1
                        elif age <= 25:
                            age_18_25 += 1
                        elif age <= 35:
                            age_26_35 += 1
                        elif age <= 50:
                            age_36_50 += 1
                        else:
                            plus_50 += 1
                    
                    repartition_age = {
                        'moins_18': moins_18,
                        '18_25': age_18_25,
                        '26_35': age_26_35,
                        '36_50': age_36_50,
                        'plus_50': plus_50,
                        'total_avec_age': membres_avec_age
                    }
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques par âge: {e}")
            
            # Statistiques globales
            statistiques_globales = {
                'total_membres': total_membres,
                'membres_avec_email': Membre.objects.filter(email__isnull=False, email__gt='').count(),
                'membres_avec_telephone': Membre.objects.filter(telephone__isnull=False, telephone__gt='').count(),
                'membres_avec_date_naissance': Membre.objects.filter(date_naissance__isnull=False).count(),
                'membres_avec_conjoint': Membre.objects.filter(conjoint__isnull=False).count(),
                'membres_avec_enfants': Membre.objects.filter(enfant_relation__isnull=False).distinct().count(),
                'nouveaux_membres': Membre.objects.filter(created_at__isnull=False).count(),
            }
            
            return Response({
                'success': True,
                'data': {
                    'statistiques_globales': statistiques_globales,
                    'repartition_genre': repartition_genre,
                    'repartition_statut': repartition_statut,
                    'repartition_situation': repartition_situation,
                    'repartition_age': repartition_age,
                    'membres_par_tag': membres_par_tag,
                    'membres_par_departement': membres_par_departement,
                    'membres_par_groupe': membres_par_groupe
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul des statistiques: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def taged_multiple(self, request):
        """
        Ajoute plusieurs tags à plusieurs membres en une seule requête.
        Correspond à POST /api/membres/taged_multiple/
        
        Nouveau format de payload attendu :
        {
            "tags_ids": [id1, id2, id3],
            "membre_ids": [membre1, membre2, membre3]
        }
        
        Ancien format supporté pour compatibilité :
        {
            "tag_ids": [id1, id2, id3],
            "membre_ids": [membre1, membre2, membre3]
        }
        """
        try:
            # Récupérer les identifiants des tags et des membres depuis la requête
            # Support du nouveau format (tags_ids) et de l'ancien format (tag_ids) pour compatibilité
            print('request.data', request.data)
            
            # Vérifier si les données sont encapsulées dans un objet 'data' ou directement
            if request.data and isinstance(request.data, dict):
                if 'data' in request.data:
                    # Format encapsulé: {"data": {"tags_ids": [...], "membre_ids": [...]}}
                    data = request.data.get('data', {})
                    tags_ids = data.get('tags_ids', [])
                    tag_ids = data.get('tag_ids', [])
                    membre_ids = data.get('membre_ids', [])
                else:
                    # Format direct: {"tags_ids": [...], "membre_ids": [...]}
                    tags_ids = request.data.get('tags_ids', [])
                    tag_ids = request.data.get('tag_ids', [])
                    membre_ids = request.data.get('membre_ids', [])
            else:
                tags_ids = []
                tag_ids = []
                membre_ids = []
            
            # Utiliser le nouveau format en priorité, sinon l'ancien
            final_tag_ids = tags_ids if tags_ids else tag_ids
            
            # Vérifier que les identifiants ont été fournis
            if not final_tag_ids or not membre_ids:
                return Response({
                    'success': False,
                    'error': 'Les identifiants des tags (tags_ids) et des membres (membre_ids) sont requis'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier que les listes ne sont pas vides
            if not isinstance(final_tag_ids, list) or not isinstance(membre_ids, list):
                return Response({
                    'success': False,
                    'error': 'tags_ids et membre_ids doivent être des listes'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if len(final_tag_ids) == 0 or len(membre_ids) == 0:
                return Response({
                    'success': False,
                    'error': 'Les listes tags_ids et membre_ids ne peuvent pas être vides'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier l'existence des tags et membres
            from django.db.models import Q
            
            # Vérifier que tous les tags existent
            tags_existants = Tag.objects.filter(id__in=final_tag_ids)
            if len(tags_existants) != len(final_tag_ids):
                tags_trouves = list(tags_existants.values_list('id', flat=True))
                tags_manquants = [tid for tid in final_tag_ids if tid not in tags_trouves]
                return Response({
                    'success': False,
                    'error': f'Tags non trouvés: {tags_manquants}'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Vérifier que tous les membres existent
            membres_existants = Membre.objects.filter(id__in=membre_ids)
            if len(membres_existants) != len(membre_ids):
                membres_trouves = list(membres_existants.values_list('id', flat=True))
                membres_manquants = [mid for mid in membre_ids if mid not in membres_trouves]
                return Response({
                    'success': False,
                    'error': f'Membres non trouvés: {membres_manquants}'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Supprimer les étiquetages existants pour éviter les doublons
            etiquetages_supprimes = Etiquetage.objects.filter(
                membre_id__in=membre_ids, 
                tag_id__in=final_tag_ids
            ).delete()
            
            # Créer les nouveaux étiquetages (relation many-to-many entre Membre et Tag)
            etiquetages = []
            for membre_id in membre_ids:
                for tag_id in final_tag_ids:
                    etiquetages.append(Etiquetage(membre_id=membre_id, tag_id=tag_id))
            
            # Insérer tous les étiquetages en une seule requête SQL (optimisation)
            etiquetages_crees = Etiquetage.objects.bulk_create(etiquetages)
            
            # Récupérer les informations des tags et membres pour la réponse
            tags_info = list(tags_existants.values('id', 'name'))
            membres_info = list(membres_existants.values('id', 'nom', 'prenom'))
            
            # Renvoyer une réponse détaillée avec un message de succès
            return Response({
                'success': True,
                'message': f'Association de {len(final_tag_ids)} tags à {len(membre_ids)} membres effectuée avec succès !',
                'data': {
                    'etiquetages_crees': len(etiquetages_crees),
                    'etiquetages_supprimes': etiquetages_supprimes[0] if etiquetages_supprimes else 0,
                    'tags_associes': tags_info,
                    'membres_associes': membres_info,
                    'total_associations': len(final_tag_ids) * len(membre_ids)
                },
                'payload_recu': {
                    'tags_ids': final_tag_ids,
                    'membre_ids': membre_ids,
                    'format_utilise': 'nouveau' if tags_ids else 'ancien'
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de l\'association des tags: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def untaged_multiple(self, request, pk=None):
        """
        Supprime plusieurs tags d'un membre spécifique.
        Correspond à POST /api/membres/{id}/untaged_multiple/
        
        Paramètres attendus dans le corps de la requête :
        - tag_ids : liste des identifiants des tags à supprimer
        
        Le paramètre pk (id du membre) est fourni dans l'URL.
        """
        # Récupérer les identifiants des tags depuis la requête
        tag_ids = request.data.get('tag_ids', [])
        
        # Vérifier que les identifiants des tags ont été fournis
        if not tag_ids:
            return Response({'error': 'Les identifiants des tags sont requis'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Supprimer les étiquetages correspondants
        Etiquetage.objects.filter(membre_id=pk, tag_id__in=tag_ids).delete()
        
        # Renvoyer une réponse avec un message de succès
        return Response({'message': 'Suppression des tags effectuée avec succès !'})
    
    @action(detail=False, methods=['post'])
    def store_multiple_etapes(self, request):
        """
        Associe une étape à plusieurs membres en une seule requête.
        Correspond à POST /api/membres/store_multiple_etapes/
        
        Paramètres attendus dans le corps de la requête :
        - etape_id : identifiant de l'étape à associer
        - membre_ids : liste des identifiants des membres à associer
        
        Cette méthode permet d'associer une étape spécifique à plusieurs membres
        en créant les enregistrements dans la table Integration.
        """
        try:
            # Vérifier si les données sont encapsulées dans un objet 'data' ou directement
            if request.data and isinstance(request.data, dict):
                if 'data' in request.data:
                    # Format encapsulé: {"data": {"etape_id": 1, "membre_ids": [...]}}
                    data = request.data.get('data', {})
                    etape_id = data.get('etape_id')
                    membre_ids = data.get('membre_ids', [])
                else:
                    # Format direct: {"etape_id": 1, "membre_ids": [...]}
                    etape_id = request.data.get('etape_id')
                    membre_ids = request.data.get('membre_ids', [])
            else:
                etape_id = None
                membre_ids = []
            
            # Vérifier que les paramètres ont été fournis
            if not etape_id:
                return Response({
                    'success': False,
                    'error': 'L\'identifiant de l\'étape (etape_id) est requis'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not membre_ids:
                return Response({
                    'success': False,
                    'error': 'La liste des identifiants des membres (membre_ids) est requise'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier que membre_ids est une liste
            if not isinstance(membre_ids, list):
                return Response({
                    'success': False,
                    'error': 'membre_ids doit être une liste'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if len(membre_ids) == 0:
                return Response({
                    'success': False,
                    'error': 'La liste membre_ids ne peut pas être vide'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier l'existence de l'étape
            from django.shortcuts import get_object_or_404
            try:
                etape = Etape.objects.get(id=etape_id)
            except Etape.DoesNotExist:
                return Response({
                    'success': False,
                    'error': f'Étape avec l\'ID {etape_id} non trouvée'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Vérifier l'existence des membres
            membres_existants = Membre.objects.filter(id__in=membre_ids)
            if len(membres_existants) != len(membre_ids):
                membres_trouves = list(membres_existants.values_list('id', flat=True))
                membres_manquants = [mid for mid in membre_ids if mid not in membres_trouves]
                return Response({
                    'success': False,
                    'error': f'Membres non trouvés: {membres_manquants}'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Supprimer les intégrations existantes pour éviter les doublons
            integrations_supprimees = Integration.objects.filter(
                membre_id__in=membre_ids,
                etape_id=etape_id
            ).delete()
            
            # Créer les nouvelles intégrations
            integrations = []
            for membre_id in membre_ids:
                integrations.append(Integration(
                    etape_id=etape_id,
                    membre_id=membre_id,
                    created_at=timezone.now()
                ))
            
            # Insérer toutes les intégrations en une seule requête SQL (optimisation)
            integrations_crees = Integration.objects.bulk_create(integrations)
            
            # Récupérer les informations des membres pour la réponse
            membres_info = list(membres_existants.values('id', 'nom', 'prenom'))
            
            # Renvoyer une réponse détaillée
            return Response({
                'success': True,
                'message': f'Étape "{etape.libelle}" associée à {len(membre_ids)} membres avec succès !',
                'data': {
                    'integrations_crees': len(integrations_crees),
                    'integrations_supprimees': integrations_supprimees[0] if integrations_supprimees else 0,
                    'etape_associee': {
                        'id': etape.id,
                        'libelle': etape.libelle,
                        'description': etape.description
                    },
                    'membres_associes': membres_info,
                    'total_associations': len(membre_ids)
                },
                'payload_recu': {
                    'etape_id': etape_id,
                    'membre_ids': membre_ids
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de l\'association de l\'étape: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['delete'])
    def delete_etape(self, request, pk=None, etape_id=None):
        """
        Supprime une étape spécifique d'un membre.
        Correspond à DELETE /api/membres/{id}/delete_etape/{etape_id}/
        
        Le paramètre pk (id du membre) et etape_id sont fournis dans l'URL.
        Cette méthode permet de retirer une étape du parcours d'intégration d'un membre.
        """
        # Vérifier que l'identifiant de l'étape a été fourni
        if not etape_id:
            return Response({'error': 'L\'identifiant de l\'étape est requis'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Supprimer l'intégration correspondante
        Integration.objects.filter(membre_id=pk, etape_id=etape_id).delete()
        
        # Renvoyer une réponse avec un message de succès
        return Response({'message': 'Suppression effectuée avec succès !'})
    
    @action(detail=False, methods=['get'])
    def nouveaux_par_date(self, request):
        """
        Retourne le nombre de nouveaux membres par date de création
        Route: GET /api/membres/nouveaux_par_date/
        
        Paramètres de requête optionnels :
        - start_date: Date de début (YYYY-MM-DD)
        - end_date: Date de fin (YYYY-MM-DD)
        - format: 'daily' (par jour) ou 'monthly' (par mois)
        """
        try:
            from django.db.models import Count
            from django.db.models.functions import TruncDate, TruncMonth
            from datetime import datetime, timedelta
            
            # Récupérer les paramètres de requête
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            format_type = request.query_params.get('period', 'daily')
            
            # Construire le queryset de base
            queryset = Membre.objects.filter(created_at__isnull=False)
            
            # Appliquer les filtres de date si fournis
            if start_date:
                try:
                    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(created_at__gte=start_datetime)
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Format de date de début invalide. Utilisez YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if end_date:
                try:
                    end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                    queryset = queryset.filter(created_at__lt=end_datetime)
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Format de date de fin invalide. Utilisez YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Grouper par date selon le format demandé
            if format_type == 'monthly':
                # Grouper par mois
                stats = queryset.annotate(
                    month=TruncMonth('created_at')
                ).values('month').annotate(
                    count=Count('id')
                ).order_by('month')
                
                result = []
                for stat in stats:
                    result.append({
                        'date': stat['month'].strftime('%Y-%m'),
                        'count': stat['count']
                    })
            else:
                # Grouper par jour (par défaut)
                stats = queryset.annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    count=Count('id')
                ).order_by('date')
                
                result = []
                for stat in stats:
                    result.append({
                        'date': stat['date'].strftime('%Y-%m-%d'),
                        'count': stat['count']
                    })
            
            # Calculer les statistiques globales
            total_nouveaux = sum(item['count'] for item in result)
            moyenne_quotidienne = total_nouveaux / len(result) if result else 0
            
            return Response({
                'success': True,
                'data': {
                    'nouveaux_par_date': result,
                    'statistiques': {
                        'total_nouveaux': total_nouveaux,
                        'moyenne_quotidienne': round(moyenne_quotidienne, 2),
                        'periode': {
                            'start_date': start_date,
                            'end_date': end_date,
                            'format': format_type
                        }
                    }
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul des nouveaux membres par date: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='evolution-membres')
    def evolution_membres(self, request):
        """
        Retourne l'évolution du nombre total de membres par date de création
        Route: GET /api/membres/evolution_membres/
        
        Retourne un format spécifique pour les graphiques :
        [
            { date: '30 Jun', value: 0 },
            { date: 'Jul \'25', value: 1 },
            { date: '02 Jul', value: 2 },
            ...
        ]
        
        Paramètres de requête optionnels :
        - start_date: Date de début (YYYY-MM-DD)
        - end_date: Date de fin (YYYY-MM-DD)
        - period: 'daily' (par jour) ou 'monthly' (par mois)
        """
        try:
            from django.db.models import Count
            from django.db.models.functions import TruncDate, TruncMonth
            from datetime import datetime, timedelta
            
            # Récupérer les paramètres de requête
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            format_type = request.query_params.get('period', 'daily')
            
            # Construire le queryset de base
            queryset = Membre.objects.filter(created_at__isnull=False)
            
            # Appliquer les filtres de date si fournis
            if start_date:
                try:
                    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(created_at__gte=start_datetime)
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Format de date de début invalide. Utilisez YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if end_date:
                try:
                    end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                    queryset = queryset.filter(created_at__lt=end_datetime)
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Format de date de fin invalide. Utilisez YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Récupérer tous les membres triés par date de création
            membres_par_date = queryset.order_by('created_at').values('created_at')
            
            # Créer un dictionnaire pour stocker le nombre cumulatif par date
            evolution_data = {}
            count_cumulatif = 0
            
            for membre in membres_par_date:
                created_at = membre['created_at']
                
                if format_type == 'monthly':
                    # Format pour les mois
                    date_key = created_at.strftime('%b \'%y')  # 'Jul \'25'
                else:
                    # Format pour les jours
                    date_key = created_at.strftime('%d %b')  # '30 Jun', '02 Jul'
                
                count_cumulatif += 1
                evolution_data[date_key] = count_cumulatif
            
            # Convertir en liste et trier par ordre chronologique
            result = []
            for date_key, value in evolution_data.items():
                result.append({
                    'date': date_key,
                    'value': value
                })
            
            # Trier par valeur (nombre cumulatif) pour maintenir l'ordre chronologique
            result.sort(key=lambda x: x['value'])
            
            return Response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul de l\'évolution des membres: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def par_groupes(self, request):
        """
        Filtre les membres par groupes spécifiques.
        Route: GET /api/membres/par_groupes/?groupes[]=1&groupes[]=2
        
        Paramètres de requête :
        - groupes[]: Liste des IDs des groupes (peut être multiple)
        """
        try:
            groupes = request.query_params.getlist('groupes[]')
            
            if not groupes:
                return Response({
                    'success': False,
                    'error': 'Aucun groupe spécifié. Utilisez le paramètre groupes[]'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Filtrer les membres par groupes actifs
            queryset = Membre.objects.filter(
                regroupements__groupe_id__in=groupes,
                regroupements__actif=True
            ).distinct()
            
            # Appliquer la pagination et la sérialisation
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'filtres_appliques': {
                    'groupes': groupes,
                    'nombre_membres': queryset.count()
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du filtrage par groupes: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def par_etapes(self, request):
        """
        Filtre les membres par étapes spécifiques.
        Route: GET /api/membres/par_etapes/?etapes[]=1&etapes[]=2
        
        Paramètres de requête :
        - etapes[]: Liste des IDs des étapes (peut être multiple)
        """
        try:
            etapes = request.query_params.getlist('etapes[]')
            
            if not etapes:
                return Response({
                    'success': False,
                    'error': 'Aucune étape spécifiée. Utilisez le paramètre etapes[]'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Filtrer les membres par étapes
            queryset = Membre.objects.filter(
                integration__etape_id__in=etapes
            ).distinct()
            
            # Appliquer la pagination et la sérialisation
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'filtres_appliques': {
                    'etapes': etapes,
                    'nombre_membres': queryset.count()
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du filtrage par étapes: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def par_tags(self, request):
        """
        Filtre les membres par tags spécifiques.
        Route: GET /api/membres/par_tags/?tags[]=1&tags[]=2
        
        Paramètres de requête :
        - tags[]: Liste des IDs des tags (peut être multiple)
        """
        try:
            tags = request.query_params.getlist('tags[]')
            
            if not tags:
                return Response({
                    'success': False,
                    'error': 'Aucun tag spécifié. Utilisez le paramètre tags[]'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Filtrer les membres par tags
            queryset = Membre.objects.filter(
                etiquetage__tag_id__in=tags
            ).distinct()
            
            # Appliquer la pagination et la sérialisation
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'filtres_appliques': {
                    'tags': tags,
                    'nombre_membres': queryset.count()
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du filtrage par tags: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def filtres_combines(self, request):
        """
        Filtre les membres par une combinaison de groupes, étapes et tags.
        Route: GET /api/membres/filtres_combines/?groupes[]=1&etapes[]=1&tags[]=1
        
        Paramètres de requête :
        - groupes[]: Liste des IDs des groupes (optionnel)
        - etapes[]: Liste des IDs des étapes (optionnel)
        - tags[]: Liste des IDs des tags (optionnel)
        """
        try:
            groupes = request.query_params.getlist('groupes[]')
            etapes = request.query_params.getlist('etapes[]')
            tags = request.query_params.getlist('tags[]')
            
            # Vérifier qu'au moins un filtre est appliqué
            if not groupes and not etapes and not tags:
                return Response({
                    'success': False,
                    'error': 'Aucun filtre spécifié. Utilisez au moins un des paramètres: groupes[], etapes[], tags[]'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Construire le queryset de base
            queryset = Membre.objects.all()
            
            # Appliquer les filtres
            if groupes:
                queryset = queryset.filter(
                    regroupements__groupe_id__in=groupes,
                    regroupements__actif=True
                )
            
            if etapes:
                queryset = queryset.filter(integration__etape_id__in=etapes)
            
            if tags:
                queryset = queryset.filter(etiquetage__tag_id__in=tags)
            
            # Appliquer distinct pour éviter les doublons
            queryset = queryset.distinct()
            
            # Appliquer la pagination et la sérialisation
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'filtres_appliques': {
                    'groupes': groupes,
                    'etapes': etapes,
                    'tags': tags,
                    'nombre_membres': queryset.count()
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du filtrage combiné: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def tous_les_membres(self, request):
        """
        Récupère l'intégralité des membres sans pagination
        Route: GET /api/membres/tous_les_membres/
        
        Paramètres de requête optionnels :
        - search: Recherche dans nom, prénom, email, téléphone
        - ordering: Tri (nom, prenom, created_at, updated_at, -nom, -prenom, etc.)
        - groupes[]: Filtrage par groupes
        - etapes[]: Filtrage par étapes
        - tags[]: Filtrage par tags
        - avec_relations: true/false pour inclure les relations (groupes, étapes, tags)
        """
        try:
            # Utiliser le queryset optimisé avec les filtres
            queryset = self.get_queryset()
            
            # Appliquer la recherche si spécifiée
            search_term = request.query_params.get('search', '')
            if search_term:
                queryset = queryset.filter(
                    Q(nom__icontains=search_term) |
                    Q(prenom__icontains=search_term) |
                    Q(email__icontains=search_term) |
                    Q(telephone__icontains=search_term)
                )
            
            # Appliquer le tri
            ordering = request.query_params.get('ordering', 'nom')
            if ordering in ['nom', 'prenom', 'created_at', 'updated_at', '-nom', '-prenom', '-created_at', '-updated_at']:
                queryset = queryset.order_by(ordering)
            
            # Option pour inclure les relations
            avec_relations = request.query_params.get('avec_relations', 'false').lower() == 'true'
            
            if avec_relations:
                # Précharger les relations pour optimiser les performances
                queryset = queryset.prefetch_related(
                    'regroupements__groupe',
                    'integration__etape',
                    'etiquetage__tag',
                    'serviteurs__departement',
                    'enfants_relation',
                    'conjoints'
                ).select_related('categorie_age', 'conjoint')
                
                # Sérialiser avec les données supplémentaires
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
                
                # Ajouter les relations à chaque membre
                for i, membre in enumerate(queryset):
                    # Groupes
                    groupes = []
                    for regroupement in membre.regroupements.filter(actif=True):
                        groupes.append({
                            'id': regroupement.groupe.id,
                            'nom': regroupement.groupe.nom,
                            'date_inscription': regroupement.date_inscription
                        })
                    data[i]['groupes'] = groupes
                    
                    # Étapes
                    etapes = []
                    for integration in membre.integration.all():
                        etapes.append({
                            'id': integration.etape.id,
                            'libelle': integration.etape.libelle,
                            'created_at': integration.created_at,
                            'membership': integration.membership
                        })
                    data[i]['etapes'] = etapes
                    
                    # Tags
                    tags = []
                    for etiquetage in membre.etiquetage.all():
                        tags.append({
                            'id': etiquetage.tag.id,
                            'name': etiquetage.tag.name
                        })
                    data[i]['tags'] = tags
                    
                    # Départements
                    departements = []
                    for serviteur in membre.serviteurs.filter(actif=True):
                        departements.append({
                            'id': serviteur.departement.id,
                            'nom': serviteur.departement.nom,
                            'date_inscription': serviteur.date_inscription
                        })
                    data[i]['departements'] = departements
                    
                    # Enfants
                    enfants = []
                    for enfant_relation in membre.enfant_relation.all():
                        enfants.append({
                            'id': enfant_relation.enfant.id,
                            'nom': enfant_relation.enfant.nom,
                            'prenom': enfant_relation.enfant.prenom
                        })
                    data[i]['enfants'] = enfants
                    
                    # Conjoint
                    if membre.conjoint:
                        data[i]['conjoint'] = {
                            'id': membre.conjoint.id,
                            'nom': membre.conjoint.nom,
                            'prenom': membre.conjoint.prenom
                        }
                    else:
                        data[i]['conjoint'] = None
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            
            return Response({
                'success': True,
                'data': data,
                'total': len(data),
                'filtres_appliques': {
                    'search': search_term,
                    'ordering': ordering,
                    'groupes': request.query_params.getlist('groupes[]'),
                    'etapes': request.query_params.getlist('etapes[]'),
                    'tags': request.query_params.getlist('tags[]'),
                    'avec_relations': avec_relations
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération des membres: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def membres_simples(self, request):
        """
        Récupère une liste simplifiée des membres (nom, prénom, id) sans pagination
        Route: GET /api/membres/membres_simples/
        
        Paramètres de requête optionnels :
        - search: Recherche dans nom et prénom
        - ordering: Tri (nom, prenom, -nom, -prenom)
        - groupes[]: Filtrage par groupes
        - etapes[]: Filtrage par étapes
        - tags[]: Filtrage par tags
        """
        try:
            queryset = self.get_queryset()
            
            # Appliquer la recherche si spécifiée
            search_term = request.query_params.get('search', '')
            if search_term:
                queryset = queryset.filter(
                    Q(nom__icontains=search_term) |
                    Q(prenom__icontains=search_term)
                )
            
            # Appliquer le tri
            ordering = request.query_params.get('ordering', 'nom')
            if ordering in ['nom', 'prenom', '-nom', '-prenom']:
                queryset = queryset.order_by(ordering)
            
            # Sélectionner seulement les champs nécessaires
            queryset = queryset.only('id', 'nom', 'prenom', 'email')
            
            # Créer une liste simplifiée
            membres_simples = []
            for membre in queryset:
                membres_simples.append({
                    'id': membre.id,
                    'nom': membre.nom,
                    'prenom': membre.prenom,
                    'telephone': membre.telephone,
                    'email': membre.email,
                    'nom_complet': f"{membre.prenom or ''} {membre.nom or ''}".strip()
                })
            
            return Response({
                'success': True,
                'data': membres_simples,
                'total': len(membres_simples),
                'filtres_appliques': {
                    'search': search_term,
                    'ordering': ordering,
                    'groupes': request.query_params.getlist('groupes[]'),
                    'etapes': request.query_params.getlist('etapes[]'),
                    'tags': request.query_params.getlist('tags[]')
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération des membres simples: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def membre_avec_relations(self, request, pk=None):
        """
        Récupère un membre avec ses relations: tags, étape, groupe, département
        Route: GET /api/membres/{id}/membre_avec_relations/
        """
        try:
            membre = self.get_object()
            
            # Récupérer les tags du membre
            tags = []
            try:
                etiquetages = Etiquetage.objects.filter(membre=membre).select_related('tag')
                tags = [
                    {
                        'id': etiquetage.tag.id,
                        'name': etiquetage.tag.name,
                    }
                    for etiquetage in etiquetages
                ]
            except Exception as e:
                print(f"Erreur lors de la récupération des tags: {e}")
            
            # Récupérer l'étape actuelle du membre
            etape_actuelle = None
            try:
                integration = Integration.objects.filter(membre=membre).select_related('etape').order_by('-created_at').first()
                if integration:
                    etape_actuelle = {
                        'id': integration.etape.id,
                        'libelle': integration.etape.libelle,
                        'description': integration.etape.description,
                        'date_association': integration.created_at
                    }
            except Exception as e:
                print(f"Erreur lors de la récupération de l'étape: {e}")
            
            # Récupérer le groupe d'appartenance du membre
            groupe_actuel = None
            try:
                regroupement = Regroupements.objects.filter(membre=membre, actif=True).select_related('groupe').first()
                if regroupement:
                    groupe_actuel = {
                        'id': regroupement.groupe.id,
                        'nom': regroupement.groupe.nom,
                        'description': regroupement.groupe.description,
                        'date_inscription': regroupement.date_inscription,
                        'date_sortie': regroupement.date_sortie
                    }
            except Exception as e:
                print(f"Erreur lors de la récupération du groupe: {e}")
            
            # Récupérer le département d'appartenance du membre
            departement_actuel = None
            try:
                serviteur = Serviteurs.objects.filter(membre=membre, actif=True).select_related('departement').first()
                if serviteur:
                    departement_actuel = {
                        'id': serviteur.departement.id,
                        'nom': serviteur.departement.nom,
                        'mission': serviteur.departement.mission,
                        'color': serviteur.departement.color,
                        'date_inscription': serviteur.date_inscription,
                        'date_sortie': serviteur.date_sortie
                    }
            except Exception as e:
                print(f"Erreur lors de la récupération du département: {e}")
            
            # Récupérer les informations de base du membre
            membre_data = {
                'id': membre.id,
                'nom': membre.nom,
                'prenom': membre.prenom,
                'email': membre.email,
                'telephone': membre.telephone,
                'adresse': membre.adresse,
                'ville': membre.ville,
                'profession': membre.profession,
                'nationalite': membre.nationalite,
                'genre': membre.genre,
                'date_naissance': membre.date_naissance,
                'situation_matrimoniale': membre.situation_matrimoniale,
                'statut': membre.statut,
                'color': membre.color,
                'created_at': membre.created_at,
                'updated_at': membre.updated_at
            }
            
            # Construire la réponse complète
            response_data = {
                'success': True,
                'data': {
                    'membre': membre_data,
                    'relations': {
                        'tags': tags,
                        'etape_actuelle': etape_actuelle,
                        'groupe_actuel': groupe_actuel,
                        'departement_actuel': departement_actuel
                    },
                    'statistiques': {
                        'nombre_tags': len(tags),
                        'a_une_etape': etape_actuelle is not None,
                        'a_un_groupe': groupe_actuel is not None,
                        'a_un_departement': departement_actuel is not None
                    }
                }
            }
            
            return Response(response_data)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération du membre avec ses relations: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'errors': ['Email and password are required.']}, status=422)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'errors': ['Utilisateur non trouvé']}, status=422)
        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is not None:
            token, created = Token.objects.get_or_create(user=user)
            # Récupérer le profil utilisateur pour obtenir le nom
            try:
                profile = user.profile
                name = profile.name
            except:
                name = user.username
            return Response({'data': {'user': {'id': user.id, 'username': user.username, 'email': user.email, 'name': name}, 'token': token.key}}, status=200)
        else:
            return Response({'errors': ["Erreur d'authentification"]}, status=422)


class UserViewSet(BaseViewSet):
    """
    ViewSet pour le modèle User.
    Fournit les opérations CRUD standard pour gérer les utilisateurs.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email', 'date_joined']
    
    def get_permissions(self):
        """
        Définit les permissions en fonction de l'action.
        - create (inscription): accessible à tous
        - retrieve, update, destroy: accessible uniquement à l'utilisateur concerné ou à un admin
        - list: accessible uniquement aux admins
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        """
        Récupère un utilisateur spécifique.
        Un utilisateur ne peut voir que son propre profil, sauf s'il est admin.
        """
        instance = self.get_object()
        if request.user.is_staff or request.user.id == instance.id:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Vous n\'êtes pas autorisé à voir ce profil.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Retourne les statistiques complètes des utilisateurs
        Route: GET /api/users/statistiques/
        """
        try:
            from django.db.models import Count
            from django.contrib.auth.models import Group
            
            # Total exact d'utilisateurs
            total_users = User.objects.count()
            
            # Utilisateurs actifs (qui se sont connectés récemment)
            users_actifs = User.objects.filter(is_active=True).count()
            users_inactifs = User.objects.filter(is_active=False).count()
            
            # Nouveaux utilisateurs (créés ce mois)
            from datetime import datetime, timedelta
            from django.utils import timezone
            
            now = timezone.now()
            debut_mois = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            nouveaux_users = User.objects.filter(date_joined__gte=debut_mois).count()
            
            # Répartition par groupes/roles
            repartition_roles = {}
            try:
                # Compter les utilisateurs par groupe
                for group in Group.objects.all():
                    count = group.user_set.count()
                    if count > 0:
                        repartition_roles[group.name] = count
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques par rôle: {e}")
            
            # Répartition par date de création (par mois)
            repartition_date_creation = {}
            try:
                from django.db.models.functions import TruncMonth
                
                # Grouper par mois de création
                users_par_mois = User.objects.annotate(
                    mois_creation=TruncMonth('date_joined')
                ).values('mois_creation').annotate(
                    count=Count('id')
                ).order_by('mois_creation')
                
                for stat in users_par_mois:
                    mois = stat['mois_creation'].strftime('%Y-%m')
                    repartition_date_creation[mois] = stat['count']
            except Exception as e:
                print(f"Erreur lors du calcul des statistiques par date: {e}")
            
            # Statistiques globales
            statistiques_globales = {
                'total_users': total_users,
                'users_actifs': users_actifs,
                'users_inactifs': users_inactifs,
                'nouveaux_users': nouveaux_users,
            }
            
            return Response({
                'success': True,
                'data': {
                    'statistiques_globales': statistiques_globales,
                    'repartition_roles': repartition_roles,
                    'repartition_date_creation': repartition_date_creation
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul des statistiques: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileViewSet(BaseViewSet):
    """ViewSet pour les opérations CRUD sur le modèle UserProfile."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_permissions(self):
        """Définit les permissions en fonction de l'action.
        
        - retrieve, update: l'utilisateur lui-même ou un admin
        - list, create, destroy: admin uniquement
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated]
        else:  # list, create, destroy et autres actions
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_object(self):
        """Surcharge pour vérifier que l'utilisateur ne peut accéder qu'à son propre profil."""
        obj = super().get_object()
        if not self.request.user.is_staff and obj.user.id != self.request.user.id:
            self.permission_denied(self.request, message="Vous n'avez pas la permission d'accéder à ce profil.")
        return obj

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'message': 'You have been successfully logged out!'}, status=200)

class VerifyTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'user': {'id': user.id, 'email': user.email, 'name': user.username}, 'token': request.auth.key}, status=200)


class CategorieAgeViewSet(BaseViewSet):
    queryset = CategorieAge.objects.all()
    serializer_class = CategorieAgeSerializer
    search_fields = ['libelle']
    ordering_fields = ['min_age', 'max_age']


class DepartementViewSet(BaseViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    search_fields = ['nom', 'mission']
    ordering_fields = ['nom', 'created_at', 'updated_at']
    
    def create(self, request, *args, **kwargs):
        """
        Création d'un département avec gestion des erreurs d'unicité
        """
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique' in str(e) or 'UNIQUE constraint' in str(e):
                return Response({
                    'success': False,
                    'error': 'Un département avec ce nom existe déjà.',
                    'details': 'Le nom du département doit être unique.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Erreur lors de la création du département.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Mise à jour d'un département avec gestion des erreurs d'unicité
        """
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique' in str(e) or 'UNIQUE constraint' in str(e):
                return Response({
                    'success': False,
                    'error': 'Un département avec ce nom existe déjà.',
                    'details': 'Le nom du département doit être unique.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Erreur lors de la mise à jour du département.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations nécessaires
        pour le calcul du nombre de serviteurs
        """
        queryset = Departement.objects.all()
        
        # Précharger les relations pour optimiser les performances
        queryset = queryset.prefetch_related(
            'serviteurs__membre'
        ).distinct()
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Retourne les statistiques des départements avec le nombre de serviteurs
        Route: GET /api/departements/statistiques/
        """
        try:
            from django.db.models import Count, Q
            
            # Calculer les statistiques pour chaque département
            departements_stats = []
            
            for departement in self.get_queryset():
                # Compter les serviteurs actifs via la relation Serviteurs
                nombre_serviteurs = departement.serviteurs.filter(actif=True).count()
                
                departements_stats.append({
                    'id': departement.id,
                    'nom': departement.nom,
                    'mission': departement.mission,
                    'color': departement.color,
                    'membres_count': nombre_serviteurs,
                    'created_at': departement.created_at,
                    'updated_at': departement.updated_at
                })
            
            # Calculer les statistiques globales
            total_departements = len(departements_stats)
            total_serviteurs = sum(stat['membres_count'] for stat in departements_stats)
            departement_plus_populaire = max(departements_stats, key=lambda x: x['membres_count']) if departements_stats else None
            
            return Response({
                'success': True,
                'data': {
                    'departements': departements_stats,
                    'statistiques_globales': {
                        'total_departements': total_departements,
                        'total_serviteurs': total_serviteurs,
                        'moyenne_serviteurs_par_departement': total_serviteurs / total_departements if total_departements > 0 else 0,
                        'departement_plus_populaire': departement_plus_populaire
                    }
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul des statistiques: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiteursViewSet(BaseViewSet):
    """
    ViewSet pour gérer les serviteurs (relation many-to-many entre Membres et Départements)
    """
    queryset = Serviteurs.objects.all()
    serializer_class = ServiteursSerializer
    search_fields = ['membre__nom', 'membre__prenom', 'departement__nom']
    ordering_fields = ['date_inscription', 'date_sortie', 'membre__nom', 'departement__nom']
    
    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations
        """
        return Serviteurs.objects.select_related('membre', 'departement').all()
    
    @action(detail=False, methods=['get'])
    def actifs(self, request):
        """
        Retourne seulement les serviteurs actifs
        Route: GET /api/serviteurs/actifs/
        """
        try:
            serviteurs = self.get_queryset().filter(actif=True)
            serializer = self.get_serializer(serviteurs, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération des serviteurs actifs: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def ajouter_membre_departement(self, request):
        """
        Associe plusieurs membres à un département en une seule requête.
        Route: POST /api/serviteurs/ajouter_membre_departement/
        
        Paramètres attendus dans le corps de la requête :
        - departement_id : identifiant du département
        - membre_ids : liste des identifiants des membres à associer
        
        Cette méthode permet d'associer plusieurs membres à un département
        en créant les enregistrements dans la table Serviteurs.
        """
        try:
            # Vérifier si les données sont encapsulées dans un objet 'data' ou directement
            if request.data and isinstance(request.data, dict):
                if 'data' in request.data:
                    # Format encapsulé: {"data": {"departement_id": 1, "membre_ids": [...]}}
                    data = request.data.get('data', {})
                    departement_id = data.get('departement_id')
                    membre_ids = data.get('membre_ids', [])
                else:
                    # Format direct: {"departement_id": 1, "membre_ids": [...]}
                    departement_id = request.data.get('departement_id')
                    membre_ids = request.data.get('membre_ids', [])
            else:
                departement_id = None
                membre_ids = []
            
            # Vérifier que les paramètres ont été fournis
            if not departement_id:
                return Response({
                    'success': False,
                    'error': 'L\'identifiant du département (departement_id) est requis'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not membre_ids:
                return Response({
                    'success': False,
                    'error': 'La liste des identifiants des membres (membre_ids) est requise'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier que membre_ids est une liste
            if not isinstance(membre_ids, list):
                return Response({
                    'success': False,
                    'error': 'membre_ids doit être une liste'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if len(membre_ids) == 0:
                return Response({
                    'success': False,
                    'error': 'La liste membre_ids ne peut pas être vide'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérifier l'existence du département
            from django.shortcuts import get_object_or_404
            try:
                departement = Departement.objects.get(id=departement_id)
            except Departement.DoesNotExist:
                return Response({
                    'success': False,
                    'error': f'Département avec l\'ID {departement_id} non trouvé'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Vérifier l'existence des membres
            membres_existants = Membre.objects.filter(id__in=membre_ids)
            if len(membres_existants) != len(membre_ids):
                membres_trouves = list(membres_existants.values_list('id', flat=True))
                membres_manquants = [mid for mid in membre_ids if mid not in membres_trouves]
                return Response({
                    'success': False,
                    'error': f'Membres non trouvés: {membres_manquants}'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Supprimer les serviteurs existants pour éviter les doublons
            serviteurs_supprimes = Serviteurs.objects.filter(
                membre_id__in=membre_ids,
                departement_id=departement_id
            ).delete()
            
            # Créer les nouveaux serviteurs
            serviteurs = []
            for membre_id in membre_ids:
                serviteurs.append(Serviteurs(
                    departement_id=departement_id,
                    membre_id=membre_id,
                    actif=True,
                    date_inscription=timezone.now()
                ))
            
            # Insérer tous les serviteurs en une seule requête SQL (optimisation)
            serviteurs_crees = Serviteurs.objects.bulk_create(serviteurs)
            
            # Récupérer les informations des membres pour la réponse
            membres_info = list(membres_existants.values('id', 'nom', 'prenom'))
            
            # Renvoyer une réponse détaillée
            return Response({
                'success': True,
                'message': f'{len(membre_ids)} membres associés au département "{departement.nom}" avec succès !',
                'data': {
                    'serviteurs_crees': len(serviteurs_crees),
                    'serviteurs_supprimes': serviteurs_supprimes[0] if serviteurs_supprimes else 0,
                    'departement_associe': {
                        'id': departement.id,
                        'nom': departement.nom,
                        'mission': departement.mission,
                        'color': departement.color
                    },
                    'membres_associes': membres_info,
                    'total_associations': len(membre_ids)
                },
                'payload_recu': {
                    'departement_id': departement_id,
                    'membre_ids': membre_ids
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de l\'association des membres au département: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CritereViewSet(BaseViewSet):
    queryset = Critere.objects.all()
    serializer_class = CritereSerializer
    search_fields = ['libelle', 'description']
    ordering_fields = ['libelle']


class GroupeViewSet(BaseViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'created_at', 'updated_at']
    
    def create(self, request, *args, **kwargs):
        """
        Création d'un groupe avec gestion des erreurs d'unicité
        """
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique' in str(e) or 'UNIQUE constraint' in str(e):
                return Response({
                    'success': False,
                    'error': 'Un groupe avec ce nom existe déjà.',
                    'details': 'Le nom du groupe doit être unique.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Erreur lors de la création du groupe.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Mise à jour d'un groupe avec gestion des erreurs d'unicité
        """
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique' in str(e) or 'UNIQUE constraint' in str(e):
                return Response({
                    'success': False,
                    'error': 'Un groupe avec ce nom existe déjà.',
                    'details': 'Le nom du groupe doit être unique.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Erreur lors de la mise à jour du groupe.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations nécessaires
        pour le calcul du nombre de membres
        """
        queryset = Groupe.objects.all()
        
        # Précharger les relations pour optimiser les performances
        queryset = queryset.prefetch_related(
            'regroupements__membre'
        ).distinct()
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Retourne les statistiques des groupes avec le nombre de membres
        Route: GET /api/groupes/statistiques/
        """
        try:
            from django.db.models import Count, Q
            
            # Calculer les statistiques pour chaque groupe
            groupes_stats = []
            
            for groupe in self.get_queryset():
                # Compter les membres actifs via la relation Regroupements
                nombre_membres = groupe.regroupements.count()
                
                groupes_stats.append({
                    'id': groupe.id,
                    'nom': groupe.nom,
                    'description': groupe.description,
                    'color': groupe.color,
                    'membres_count': nombre_membres,
                    'created_at': groupe.created_at,
                    'updated_at': groupe.updated_at
                })
            
            # Calculer les statistiques globales
            total_groupes = len(groupes_stats)
            total_membres = sum(stat['membres_count'] for stat in groupes_stats)
            groupe_plus_populaire = max(groupes_stats, key=lambda x: x['membres_count']) if groupes_stats else None
            
            return Response({
                'success': True,
                'data': {
                    'groupes': groupes_stats,
                    'statistiques_globales': {
                        'total_groupes': total_groupes,
                        'total_membres': total_membres,
                        'moyenne_membres_par_groupe': total_membres / total_groupes if total_groupes > 0 else 0,
                        'groupe_plus_populaire': groupe_plus_populaire
                    }
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul des statistiques: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def insert_membre(self, request, pk=None):
        """
        Ajouter des membres à un groupe
        Route: POST /api/groupes/{id}/insert_membre/
        """
        data = request.data.get('data', {})
        membre_ids = data.get('membre_ids', [])
        
        if not membre_ids:
            return Response({'error': 'Les identifiants des membres sont requis'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            groupe = self.get_object()
            regroupements_crees = []
            
            for membre_id in membre_ids:
                # Vérifier si le membre existe
                try:
                    membre = Membre.objects.get(id=membre_id)
                except Membre.DoesNotExist:
                    continue
                
                # Créer ou mettre à jour le regroupement
                regroupement, created = Regroupements.objects.get_or_create(
                    membre=membre,
                    groupe=groupe,
                    defaults={'actif': True}
                )
                
                if not created and not regroupement.actif:
                    # Réactiver le regroupement existant
                    regroupement.actif = True
                    regroupement.date_sortie = None
                    regroupement.save()
                
                regroupements_crees.append(regroupement)
            
            return Response({
                'success': True,
                'message': f'{len(regroupements_crees)} membres ajoutés au groupe {groupe.nom} avec succès',
                'data': {
                    'groupe_id': groupe.id,
                    'groupe_nom': groupe.nom,
                    'membres_ajoutes': len(regroupements_crees)
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de l\'ajout des membres: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def remove_membre(self, request, pk=None):
        """
        Retirer des membres d'un groupe
        Route: POST /api/groupes/{id}/remove_membre/
        """
        membre_ids = request.data.get('membre_ids', [])
        
        if not membre_ids:
            return Response({'error': 'Les identifiants des membres sont requis'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            groupe = self.get_object()
            regroupements_supprimes = 0
            
            for membre_id in membre_ids:
                # Marquer le regroupement comme inactif
                regroupements = Regroupements.objects.filter(
                    membre_id=membre_id,
                    groupe=groupe,
                    actif=True
                )
                
                for regroupement in regroupements:
                    regroupement.actif = False
                    regroupement.date_sortie = timezone.now()
                    regroupement.save()
                    regroupements_supprimes += 1
            
            return Response({
                'success': True,
                'message': f'{regroupements_supprimes} membres retirés du groupe avec succès',
                'data': {
                    'groupe_id': groupe.id,
                    'groupe_nom': groupe.nom,
                    'membres_retires': regroupements_supprimes
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du retrait des membres: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegroupementsViewSet(BaseViewSet):
    """
    ViewSet pour gérer les regroupements (relation many-to-many entre Membres et Groupes)
    """
    queryset = Regroupements.objects.all()
    serializer_class = RegroupementsSerializer
    search_fields = ['membre__nom', 'membre__prenom', 'groupe__nom']
    ordering_fields = ['date_inscription', 'date_sortie', 'membre__nom', 'groupe__nom']
    
    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations
        """
        return Regroupements.objects.select_related('membre', 'groupe').all()
    
    @action(detail=False, methods=['get'])
    def actifs(self, request):
        """
        Retourne seulement les regroupements actifs
        Route: GET /api/regroupements/actifs/
        """
        try:
            regroupements = self.get_queryset().filter(actif=True)
            serializer = self.get_serializer(regroupements, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération des regroupements actifs: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def ajouter_membre_groupe(self, request):
        """
        Ajouter un membre à un groupe
        Route: POST /api/regroupements/ajouter_membre_groupe/
        """
        membre_id = request.data.get('membre_id')
        groupe_id = request.data.get('groupe_id')
        
        if not membre_id or not groupe_id:
            return Response({
                'success': False,
                'error': 'Les identifiants du membre et du groupe sont requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            membre = Membre.objects.get(id=membre_id)
            groupe = Groupe.objects.get(id=groupe_id)
            
            # Créer ou réactiver le regroupement
            regroupement, created = Regroupements.objects.get_or_create(
                membre=membre,
                groupe=groupe,
                defaults={'actif': True}
            )
            
            if not created and not regroupement.actif:
                regroupement.actif = True
                regroupement.date_sortie = None
                regroupement.save()
            
            serializer = self.get_serializer(regroupement)
            
            return Response({
                'success': True,
                'message': 'Membre ajouté au groupe avec succès',
                'data': serializer.data
            })
            
        except Membre.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Membre non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        except Groupe.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Groupe non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de l\'ajout: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EtapeViewSet(BaseViewSet):
    queryset = Etape.objects.all()
    serializer_class = EtapeSerializer
    search_fields = ['libelle', 'description']
    ordering_fields = ['libelle']


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ['name']
    ordering_fields = ['name']
    
    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations si nécessaire
        """
        return Tag.objects.all()
    
    @action(detail=False, methods=['get'])
    def tous_les_tags(self, request):
        """
        Récupère la totalité des tags sans pagination
        Route: GET /api/tags/tous_les_tags/
        
        Paramètres de requête optionnels :
        - search: Recherche dans le nom des tags
        - ordering: Tri (name, -name)
        - avec_membres: true/false pour inclure le nombre de membres par tag
        """
        try:
            queryset = self.get_queryset()
            
            # Appliquer la recherche si spécifiée
            search_term = request.query_params.get('search', '')
            if search_term:
                queryset = queryset.filter(name__icontains=search_term)
            
            # Appliquer le tri
            ordering = request.query_params.get('ordering', 'name')
            if ordering in ['name', '-name']:
                queryset = queryset.order_by(ordering)
            
            # Option pour inclure le nombre de membres par tag
            avec_membres = request.query_params.get('avec_membres', 'false').lower() == 'true'
            
            if avec_membres:
                from django.db.models import Count
                queryset = queryset.annotate(
                    nombre_membres=Count('etiquetage__membre', distinct=True)
                )
                
                # Sérialiser avec les données supplémentaires
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
                
                # Ajouter le nombre de membres à chaque tag
                for i, tag in enumerate(queryset):
                    data[i]['nombre_membres'] = tag.nombre_membres
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            
            return Response({
                'success': True,
                'data': data,
                'total': len(data),
                'filtres_appliques': {
                    'search': search_term,
                    'ordering': ordering,
                    'avec_membres': avec_membres
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération des tags: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Retourne les statistiques des tags
        Route: GET /api/tags/statistiques/
        """
        try:
            from django.db.models import Count
            
            # Total des tags
            total_tags = Tag.objects.count()
            
            # Tags les plus utilisés (avec le plus de membres)
            tags_populaires = Tag.objects.annotate(
                nombre_membres=Count('etiquetage__membre', distinct=True)
            ).filter(nombre_membres__gt=0).order_by('-nombre_membres')[:10]
            
            # Tags non utilisés
            tags_non_utilises = Tag.objects.annotate(
                nombre_membres=Count('etiquetage__membre', distinct=True)
            ).filter(nombre_membres=0).count()
            
            # Répartition par nombre de membres
            repartition = {
                '0_membre': tags_non_utilises,
                '1_5_membres': Tag.objects.annotate(
                    nombre_membres=Count('etiquetage__membre', distinct=True)
                ).filter(nombre_membres__range=(1, 5)).count(),
                '6_10_membres': Tag.objects.annotate(
                    nombre_membres=Count('etiquetage__membre', distinct=True)
                ).filter(nombre_membres__range=(6, 10)).count(),
                'plus_de_10_membres': Tag.objects.annotate(
                    nombre_membres=Count('etiquetage__membre', distinct=True)
                ).filter(nombre_membres__gt=10).count()
            }
            
            return Response({
                'success': True,
                'data': {
                    'total_tags': total_tags,
                    'tags_populaires': [
                        {
                            'id': tag.id,
                            'name': tag.name,
                            'nombre_membres': tag.nombre_membres
                        } for tag in tags_populaires
                    ],
                    'tags_non_utilises': tags_non_utilises,
                    'repartition': repartition
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du calcul des statistiques: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def avec_membres(self, request):
        """
        Récupère tous les tags avec le nombre de membres associés
        Route: GET /api/tags/avec_membres/
        
        Paramètres de requête optionnels :
        - min_membres: Nombre minimum de membres (filtre)
        - max_membres: Nombre maximum de membres (filtre)
        - ordering: Tri (nombre_membres, -nombre_membres, name, -name)
        """
        try:
            from django.db.models import Count
            
            queryset = Tag.objects.annotate(
                nombre_membres=Count('etiquetage__membre', distinct=True)
            )
            
            # Filtres par nombre de membres
            min_membres = request.query_params.get('min_membres')
            if min_membres and min_membres.isdigit():
                queryset = queryset.filter(nombre_membres__gte=int(min_membres))
            
            max_membres = request.query_params.get('max_membres')
            if max_membres and max_membres.isdigit():
                queryset = queryset.filter(nombre_membres__lte=int(max_membres))
            
            # Tri
            ordering = request.query_params.get('ordering', 'nombre_membres')
            if ordering in ['nombre_membres', '-nombre_membres', 'name', '-name']:
                queryset = queryset.order_by(ordering)
            
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            
            # Ajouter le nombre de membres à chaque tag
            for i, tag in enumerate(queryset):
                data[i]['nombre_membres'] = tag.nombre_membres
            
            return Response({
                'success': True,
                'data': data,
                'total': len(data),
                'filtres_appliques': {
                    'min_membres': min_membres,
                    'max_membres': max_membres,
                    'ordering': ordering
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la récupération des tags avec membres: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def creer_multiple(self, request):
        """
        Crée plusieurs tags en une seule requête
        Route: POST /api/tags/creer_multiple/
        
        Paramètres attendus dans le corps de la requête :
        - tags: Liste des noms de tags à créer
        """
        try:
            tags_data = request.data.get('tags', [])
            
            if not tags_data or not isinstance(tags_data, list):
                return Response({
                    'success': False,
                    'error': 'Le paramètre "tags" doit être une liste non vide'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Créer les tags
            tags_crees = []
            tags_existants = []
            
            for tag_name in tags_data:
                if not tag_name or not isinstance(tag_name, str):
                    continue
                
                tag_name = tag_name.strip()
                if not tag_name:
                    continue
                
                # Vérifier si le tag existe déjà
                tag, created = Tag.objects.get_or_create(name=tag_name)
                
                if created:
                    tags_crees.append(tag)
                else:
                    tags_existants.append(tag)
            
            # Sérialiser les tags créés
            serializer = self.get_serializer(tags_crees, many=True)
            
            return Response({
                'success': True,
                'message': f'{len(tags_crees)} tags créés avec succès',
                'data': {
                    'tags_crees': serializer.data,
                    'tags_existants': len(tags_existants),
                    'total_traites': len(tags_data)
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors de la création multiple: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DegreViewSet(BaseViewSet):
    queryset = Degre.objects.all()
    serializer_class = DegreSerializer
    search_fields = ['description']
    ordering_fields = ['ratio']


class AppartenanceViewSet(BaseViewSet):
    queryset = Appartenance.objects.all()
    serializer_class = AppartenanceSerializer


class IntegrationViewSet(BaseViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    ordering_fields = ['created_at']


class EtiquetageViewSet(BaseViewSet):
    queryset = Etiquetage.objects.all()
    serializer_class = EtiquetageSerializer


class EnfantViewSet(BaseViewSet):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer


class AttachementViewSet(BaseViewSet):
    queryset = Attachement.objects.all()
    serializer_class = AttachementSerializer
    search_fields = ['name', 'extension']
    ordering_fields = ['uploaded_at']


class FormulaireViewSet(BaseViewSet):
    queryset = Formulaire.objects.all()
    serializer_class = FormulaireSerializer
    search_fields = ['nom_du_formulaire']
    ordering_fields = ['created_at', 'updated_at']


class ChampViewSet(BaseViewSet):
    queryset = Champ.objects.all()
    serializer_class = ChampSerializer
    search_fields = ['nom_du_champ', 'type_de_champ']


class CategorieMotifRdvViewSet(BaseViewSet):
    queryset = CategorieMotifRdv.objects.all()
    serializer_class = CategorieMotifRdvSerializer
    search_fields = ['libelleCategorie']
    ordering_fields = ['created_at', 'updated_at']


class DisponibiliteRdvViewSet(BaseViewSet):
    queryset = DisponibiliteRdv.objects.all()
    serializer_class = DisponibiliteRdvSerializer
    ordering_fields = ['dateDispo', 'created_at', 'updated_at']


class RoleIntervenantViewSet(BaseViewSet):
    queryset = RoleIntervenant.objects.all()
    serializer_class = RoleIntervenantSerializer


class IntervenantViewSet(BaseViewSet):
    queryset = Intervenant.objects.all()
    serializer_class = IntervenantSerializer
    search_fields = ['nom', 'prenom']
    ordering_fields = ['nom', 'prenom']


class EvenementViewSet(BaseViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    search_fields = ['nom_evenement', 'lieu']
    ordering_fields = ['date', 'created_at', 'updated_at']


class EvenementAffectationViewSet(BaseViewSet):
    queryset = EvenementAffectation.objects.all()
    serializer_class = EvenementAffectationSerializer


class RdvViewSet(BaseViewSet):
    queryset = Rdv.objects.all()
    serializer_class = RdvSerializer
    search_fields = ['nom', 'prenom', 'motif']
    ordering_fields = ['date_rdv', 'heure_rdv', 'created_at', 'updated_at']


class DefiViewSet(BaseViewSet):
    queryset = Defi.objects.all()
    serializer_class = DefiSerializer
    search_fields = ['description']


class VictoireViewSet(BaseViewSet):
    queryset = Victoire.objects.all()
    serializer_class = VictoireSerializer
    search_fields = ['description']


class FaitMarquantViewSet(BaseViewSet):
    queryset = FaitMarquant.objects.all()
    serializer_class = FaitMarquantSerializer
    search_fields = ['description']


class DashboardStatsView(APIView):
    """
    Vue pour récupérer les statistiques du tableau de bord.
    Retourne le nombre d'utilisateurs, groupes, départements et membres.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Récupère les statistiques du tableau de bord.
        
        Returns:
            Response: JSON avec les statistiques au format:
            {
                "departments": number,
                "groups": number,
                "users": number,
                "members": number
            }
        """
        try:
            # Compter les départements
            departments_count = Departement.objects.count()
            
            # Compter les groupes
            groups_count = Groupe.objects.count()
            
            # Compter les utilisateurs (User de Django)
            users_count = User.objects.count()
            
            # Compter les membres
            members_count = Membre.objects.count()
            
            # Préparer la réponse au format demandé
            stats = {
                "departments": departments_count,
                "groups": groups_count,
                "users": users_count,
                "members": members_count
            }
            
            return Response(stats, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Erreur lors de la récupération des statistiques: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)