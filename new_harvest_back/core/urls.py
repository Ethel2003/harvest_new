from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, LogoutView, VerifyTokenView, UserViewSet, UserProfileViewSet,
    MembreViewSet, CategorieAgeViewSet, DepartementViewSet, CritereViewSet,
    GroupeViewSet, RegroupementsViewSet, ServiteursViewSet, EtapeViewSet, TagViewSet, DegreViewSet, AppartenanceViewSet,
    IntegrationViewSet, EtiquetageViewSet, EnfantViewSet, AttachementViewSet,
    FormulaireViewSet, ChampViewSet, CategorieMotifRdvViewSet, DisponibiliteRdvViewSet,
    RoleIntervenantViewSet, IntervenantViewSet, EvenementViewSet, EvenementAffectationViewSet,
    RdvViewSet, DefiViewSet, VictoireViewSet, FaitMarquantViewSet, DashboardStatsView
)

router = DefaultRouter()

# Enregistrement des routes pour tous les modèles
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'membres', MembreViewSet, basename='membre')
router.register(r'categories-age', CategorieAgeViewSet, basename='categorie-age')
router.register(r'departements', DepartementViewSet, basename='departement')
router.register(r'criteres', CritereViewSet, basename='critere')
router.register(r'groupes', GroupeViewSet, basename='groupe')
router.register(r'regroupements', RegroupementsViewSet, basename='regroupement')
router.register(r'serviteurs', ServiteursViewSet, basename='serviteur')
router.register(r'etapes', EtapeViewSet, basename='etape')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'degres', DegreViewSet, basename='degre')
router.register(r'appartenances', AppartenanceViewSet, basename='appartenance')
router.register(r'integrations', IntegrationViewSet, basename='integration')
router.register(r'etiquetages', EtiquetageViewSet, basename='etiquetage')
router.register(r'enfants', EnfantViewSet, basename='enfant')
router.register(r'attachements', AttachementViewSet, basename='attachement')
router.register(r'formulaires', FormulaireViewSet, basename='formulaire')
router.register(r'champs', ChampViewSet, basename='champ')
router.register(r'categories-motif-rdv', CategorieMotifRdvViewSet, basename='categorie-motif-rdv')
router.register(r'disponibilites-rdv', DisponibiliteRdvViewSet, basename='disponibilite-rdv')
router.register(r'roles-intervenants', RoleIntervenantViewSet, basename='role-intervenant')
router.register(r'intervenants', IntervenantViewSet, basename='intervenant')
router.register(r'evenements', EvenementViewSet, basename='evenement')
router.register(r'evenement-affectations', EvenementAffectationViewSet, basename='evenement-affectation')
router.register(r'rdvs', RdvViewSet, basename='rdv')
router.register(r'defis', DefiViewSet, basename='defi')
router.register(r'victoires', VictoireViewSet, basename='victoire')
router.register(r'faits-marquants', FaitMarquantViewSet, basename='fait-marquant')

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('verify-token', VerifyTokenView.as_view(), name='verify-token'),
    path('statistics/dashboard', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
