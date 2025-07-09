from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Membre, CategorieAge, Departement, Critere, Groupe, Regroupements, Etape, Tag, Degre,
    Appartenance, Integration, Etiquetage, Enfant, Attachement, Formulaire,
    Champ, CategorieMotifRdv, DisponibiliteRdv, RoleIntervenant, Intervenant,
    Evenement, EvenementAffectation, Rdv, Defi, Victoire, FaitMarquant, Serviteurs
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='profile.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile', 'name']
        read_only_fields = ['id', 'profile']
    
    def create(self, validated_data):
        # Créer un nouvel utilisateur avec les données validées
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        # Mettre à jour un utilisateur existant
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'username', 'email', 'created_at', 'updated_at']

class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = '__all__'
    
    def validate(self, data):
        """
        Validation personnalisée pour la combinaison nom/prénom
        """
        nom = data.get('nom')
        prenom = data.get('prenom')
        
        if nom and prenom:
            # Vérifier si un membre avec cette combinaison nom/prénom existe déjà
            instance = getattr(self, 'instance', None)
            if instance:
                # Mise à jour : exclure l'instance actuelle
                if Membre.objects.filter(nom=nom, prenom=prenom).exclude(id=instance.id).exists():
                    raise serializers.ValidationError({
                        'nom': "Un membre avec cette combinaison nom/prénom existe déjà.",
                        'prenom': "Un membre avec cette combinaison nom/prénom existe déjà."
                    })
            else:
                # Création : vérifier si la combinaison existe déjà
                if Membre.objects.filter(nom=nom, prenom=prenom).exists():
                    raise serializers.ValidationError({
                        'nom': "Un membre avec cette combinaison nom/prénom existe déjà.",
                        'prenom': "Un membre avec cette combinaison nom/prénom existe déjà."
                    })
        
        return data

class CategorieAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieAge
        fields = '__all__'

class DepartementSerializer(serializers.ModelSerializer):
    # Champ calculé pour le nombre de serviteurs actifs
    nombre_serviteurs = serializers.SerializerMethodField()
    
    class Meta:
        model = Departement
        fields = '__all__'
    
    def get_nombre_serviteurs(self, obj):
        """
        Calcule le nombre de serviteurs actifs dans ce département
        """
        try:
            return obj.serviteurs.filter(actif=True).count()
        except Exception as e:
            print(f"Erreur lors du calcul du nombre de serviteurs pour le département {obj.id}: {e}")
            return 0

class CritereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critere
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    # Champ calculé pour le nombre de membres actifs
    nombre_membres = serializers.SerializerMethodField()
    
    class Meta:
        model = Groupe
        fields = '__all__'
    
    def get_nombre_membres(self, obj):
        """
        Calcule le nombre de membres actifs dans ce groupe
        """
        try:
            return obj.regroupements.count()
        except Exception as e:
            print(f"Erreur lors du calcul du nombre de membres pour le groupe {obj.id}: {e}")
            return 0
    
    def validate_nom(self, value):
        """
        Validation personnalisée pour le nom du groupe
        """
        if value:
            # Vérifier si un groupe avec ce nom existe déjà (sauf pour les mises à jour)
            instance = getattr(self, 'instance', None)
            if instance:
                # Mise à jour : exclure l'instance actuelle
                if Groupe.objects.filter(nom=value).exclude(id=instance.id).exists():
                    raise serializers.ValidationError("Un groupe avec ce nom existe déjà.")
            else:
                # Création : vérifier si le nom existe déjà
                if Groupe.objects.filter(nom=value).exists():
                    raise serializers.ValidationError("Un groupe avec ce nom existe déjà.")
        return value


class RegroupementsSerializer(serializers.ModelSerializer):
    membre_nom = serializers.CharField(source='membre.nom', read_only=True)
    membre_prenom = serializers.CharField(source='membre.prenom', read_only=True)
    groupe_nom = serializers.CharField(source='groupe.nom', read_only=True)
    
    class Meta:
        model = Regroupements
        fields = '__all__'

class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class DegreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degre
        fields = '__all__'

class AppartenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appartenance
        fields = '__all__'

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'

class EtiquetageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiquetage
        fields = '__all__'

class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfant
        fields = '__all__'

class AttachementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachement
        fields = '__all__'

class FormulaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulaire
        fields = '__all__'

class ChampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champ
        fields = '__all__'

class CategorieMotifRdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieMotifRdv
        fields = '__all__'

class DisponibiliteRdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibiliteRdv
        fields = '__all__'

class RoleIntervenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleIntervenant
        fields = '__all__'

class IntervenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervenant
        fields = '__all__'

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class EvenementAffectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvenementAffectation
        fields = '__all__'

class RdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rdv
        fields = '__all__'

class DefiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defi
        fields = '__all__'

class VictoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victoire
        fields = '__all__'

class FaitMarquantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaitMarquant
        fields = '__all__'

class ServiteursSerializer(serializers.ModelSerializer):
    membre_nom = serializers.CharField(source='membre.nom', read_only=True)
    membre_prenom = serializers.CharField(source='membre.prenom', read_only=True)
    departement_nom = serializers.CharField(source='departement.nom', read_only=True)
    
    class Meta:
        model = Serviteurs
        fields = '__all__'

