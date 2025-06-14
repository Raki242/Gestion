from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# --- UTILISATEUR PERSONNALISÉ ---
class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrateur'),
        ('formateur', 'Formateur'),
        ('etudiant', 'Étudiant'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    code_formateur = models.CharField(max_length=10, unique=True, null=True, blank=True)
    code_parent = models.CharField(max_length=10, unique=True, null=True, blank=True)
    matricule = models.CharField(max_length=30, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# --- FILIÈRE / NIVEAU / OPTION ---
class Filiere(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Niveau(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Option(models.Model):
    nom = models.CharField(max_length=100)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom', 'filiere'], name='unique_option_par_filiere_et_niveau')
        ]
        verbose_name = "Option"
        verbose_name_plural = "Options"

    def __str__(self):
        filiere_nom = self.filiere.nom if self.filiere else "Filière inconnue"
        return f"{self.nom} - {filiere_nom}"


# --- ÉTUDIANT / PRÉINSCRIPTION ---
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'etudiant'})
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True)
    date_inscription = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username if self.user else 'Inconnu'} - {self.option.nom if self.option else 'Option ?'} - {self.niveau.nom if self.niveau else 'Niveau ?'}"


class Preinscription(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=50, default='en attente')

    def __str__(self):
        filiere_nom = self.option.filiere.nom if self.option and self.option.filiere else 'Filière ?'
        return f"{self.nom} - {self.email} - {filiere_nom} - {self.statut}"


# --- MATIÈRES / ENSEIGNEMENT ---
class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    coefficient = models.FloatField()
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} (Coef: {self.coefficient}) - {self.option.nom if self.option else 'Option ?'}"


class Enseignement(models.Model):
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'formateur'})
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.formateur.username if self.formateur else 'Formateur ?'} - {self.matiere.nom if self.matiere else 'Matière ?'}"


# --- NOTES ---
class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    valeur = models.FloatField()

    def __str__(self):
        return f"{self.etudiant.user.username if self.etudiant and self.etudiant.user else 'Étudiant ?'} - {self.matiere.nom if self.matiere else 'Matière ?'} - Note: {self.valeur}"

    def get_ponderee(self):
        return self.valeur * self.matiere.coefficient if self.matiere else 0


# --- EMARGEMENT ---
class Emargement(models.Model):
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'formateur'})
    date = models.DateField(default=timezone.now)
    heure_cours = models.FloatField()

    def __str__(self):
        return f"{self.formateur.username if self.formateur else 'Formateur ?'} - {self.date} - {self.heure_cours}h"


# --- ARTICLES ---
class Article(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titre} - par {self.auteur.username if self.auteur else 'Auteur ?'}"
