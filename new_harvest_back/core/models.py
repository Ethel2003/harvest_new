from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Modèle de profil utilisateur qui étend le modèle User par défaut de Django."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('nom complet', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil utilisateur lorsqu'un nouvel utilisateur est créé."""
    if created:
        UserProfile.objects.create(user=instance, name=instance.username)


class CategorieAge(models.Model):
    libelle = models.CharField(max_length=255)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return self.libelle

class Membre(models.Model):
    GENRE_CHOICES = [
        ('masculin', 'Masculin'),
        ('feminin', 'Féminin'),
    ]
    
    SITUATION_CHOICES = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
    ]
    
    STATUT_CHOICES = [
        ('inscrit', 'Inscrit'),
        ('membre', 'Membre'),
    ]
    
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    nationalite = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, default='1')
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    situation_matrimoniale = models.CharField(max_length=20, choices=SITUATION_CHOICES, null=True, blank=True)
    categorie_age = models.ForeignKey(CategorieAge, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    conjoint = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='conjoints')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='inscrit')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        unique_together = ['nom', 'prenom']
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom and self.nom else f"Membre {self.id}"

class Departement(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    mission = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.nom

class Critere(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.libelle

class Groupe(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, default='1')
    critere = models.ForeignKey(Critere, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.nom or f"Groupe {self.id}"

class Etape(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.libelle

class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Degre(models.Model):
    description = models.CharField(max_length=255, null=True, blank=True)
    ratio = models.IntegerField()
    bg_color = models.CharField(max_length=255, unique=True)
    etape = models.ForeignKey(Etape, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description or f"Degré {self.id}"

class Appartenance(models.Model):
    degre = models.ForeignKey(Degre, on_delete=models.CASCADE)
    etape = models.ForeignKey(Etape, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.degre} - {self.etape}"

class Integration(models.Model):
    etape = models.ForeignKey(Etape, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    created_at = models.DateField()
    membership = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.membre} - {self.etape}"

class Etiquetage(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.membre} - {self.tag}"

class Enfant(models.Model):
    enfant = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='enfant_relation')
    pere = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='pere_relation', null=True, blank=True)
    mere = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='mere_relation', null=True, blank=True)
    
    def __str__(self):
        return f"Enfant: {self.enfant}"

class Attachement(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    attachable_id = models.IntegerField()
    attachable_type = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Formulaire(models.Model):
    nom_du_formulaire = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False)
    form_extend = models.BooleanField(null=True, blank=True)
    form_static = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.nom_du_formulaire

class Champ(models.Model):
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE)
    nom_du_champ = models.CharField(max_length=255, unique=True)
    type_de_champ = models.CharField(max_length=255)
    option = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.nom_du_champ

class CategorieMotifRdv(models.Model):
    libelleCategorie = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.libelleCategorie

class DisponibiliteRdv(models.Model):
    dateDispo = models.DateField()
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.membre} - {self.dateDispo}"

class RoleIntervenant(models.Model):
    libelle = models.CharField(max_length=255, default='')
    
    def __str__(self):
        return self.libelle

class Intervenant(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Evenement(models.Model):
    nom_evenement = models.CharField(max_length=255, null=True, blank=True)
    lieu = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    is_recurrent = models.BooleanField(default=False)
    recurence_data = models.JSONField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom_evenement or f"Événement {self.id}"

class EvenementAffectation(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    intervenant = models.ForeignKey(Intervenant, on_delete=models.CASCADE)
    role_intervenant = models.ForeignKey(RoleIntervenant, on_delete=models.CASCADE)
    donnees = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.intervenant} - {self.evenement}"

class Rdv(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    motif = models.TextField()
    categorie_motif = models.ForeignKey(CategorieMotifRdv, on_delete=models.CASCADE, null=True, blank=True)
    leader = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='rdvs_leader')
    date_rdv = models.DateField()
    heure_rdv = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"RDV: {self.prenom} {self.nom} - {self.date_rdv}"

class Defi(models.Model):
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description

class Victoire(models.Model):
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description

class FaitMarquant(models.Model):
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description

class Regroupements(models.Model):
    """
    Modèle pour gérer la relation many-to-many entre Membres et Groupes
    Un membre peut appartenir à un groupe et un groupe peut avoir plusieurs membres
    """
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='regroupements')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='regroupements')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)  # Pour marquer si l'appartenance est active
    
    class Meta:
        unique_together = ['membre', 'groupe']  # Un membre ne peut pas être dans le même groupe plusieurs fois
        verbose_name = "Regroupement"
        verbose_name_plural = "Regroupements"
    
    def __str__(self):
        return f"{self.membre} - {self.groupe}"
    
class Serviteurs(models.Model):
    """
    Modèle pour gérer la relation many-to-many entre Membres et Départements
    Un membre peut appartenir à un département et un département peut avoir plusieurs membres
    """
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='serviteurs')
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='serviteurs')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)  # Pour marquer si l'appartenance est active
    titre = models.CharField(max_length=255, null=True, blank=True)
    is_responsable = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['membre', 'departement']  # Un membre ne peut pas être dans le même département plusieurs fois
        verbose_name = "Serviteur"
        verbose_name_plural = "Serviteurs"
    
    def __str__(self):
        return f"{self.membre} - {self.departement}"
