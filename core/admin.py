from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    Filiere, Niveau, Option, Etudiant, Preinscription, Matiere,
    Enseignement, Note, Emargement, Article
)

User = get_user_model()


# Inlines
class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    raw_id_fields = ('matiere',)


class MatiereInline(admin.TabularInline):
    model = Matiere
    extra = 0


class EnseignementInline(admin.TabularInline):
    model = Enseignement
    extra = 0
    raw_id_fields = ('matiere',)


# Admins
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'matricule', 'code_formateur', 'code_parent', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'matricule', 'code_formateur', 'code_parent')

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj and obj.role == 'formateur':
            return inlines + [EnseignementInline(self.model, self.admin_site)]
        return inlines


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user', 'option','filiere','niveau', 'date_inscription')
    list_filter = ('option', 'niveau','filiere')
    search_fields = ('user__username', 'user__matricule')
    inlines = [NoteInline]


@admin.register(Preinscription)
class PreinscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'option', 'niveau', 'statut')
    list_filter = ('statut', 'option', 'niveau')
    search_fields = ('nom', 'email', 'telephone')


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'filiere')
    list_filter = ['filiere']
    search_fields = ('nom',)
    inlines = [MatiereInline]


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient', 'option')
    list_filter = ('option',)
    search_fields = ('nom',)


@admin.register(Enseignement)
class EnseignementAdmin(admin.ModelAdmin):
    list_display = ('formateur', 'matiere')
    list_filter = ('formateur', 'matiere')
    search_fields = ('formateur__username', 'matiere__nom')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'matiere', 'valeur')
    list_filter = ('matiere',)
    search_fields = ('etudiant__user__username', 'matiere__nom')


@admin.register(Emargement)
class EmargementAdmin(admin.ModelAdmin):
    list_display = ('formateur', 'date', 'heure_cours')
    list_filter = ('formateur', 'date')
    search_fields = ('formateur__username',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'titre', 'date_publication', 'approuve')
    list_filter = ('approuve', 'date_publication')
    search_fields = ('titre', 'auteur__username')
    readonly_fields = ('date_publication',)
