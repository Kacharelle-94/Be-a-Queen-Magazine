from django.contrib import admin
from .models import (
    Utilisateur, Rubrique, Tag, Article, ArticleTag,
    Chronique, Newsletter, Commentaire, Contact, Media,
    Notification, Favori, Statistique, Partenaire, CampagneNewsletter,
    VisiteSite
)

# ============================================================
# CONFIGURATION TABLE 1 : UTILISATEURS
# ============================================================
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'role', 'date_inscription', 'actif', 'is_admin')
    list_filter = ('role', 'actif', 'is_admin')
    search_fields = ('nom', 'email')
    ordering = ('-date_inscription',)


# ============================================================
# CONFIGURATION TABLE 2 : RUBRIQUES
# ============================================================
@admin.register(Rubrique)
class RubriqueAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'nom', 'slug', 'ordre', 'active')
    list_editable = ('ordre', 'active')  # Permet de modifier l'ordre directement depuis la liste
    prepopulated_fields = {'slug': ('nom',)}  # Génère le slug automatiquement à l'écriture du nom
    search_fields = ('nom',)


# ============================================================
# CONFIGURATION TABLE 4 : TAGS
# ============================================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)


# ============================================================
# CONFIGURATION TABLE 3 : ARTICLES
# ============================================================
class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'rubrique', 'auteure', 'statut', 'en_une', 'date_publication', 'vues')
    list_filter = ('statut', 'en_une', 'rubrique', 'date_publication')
    list_editable = ('statut', 'en_une')
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'  # Ajoute une barre de navigation par date (année/mois)
    inlines = [ArticleTagInline]  # Permet d'associer des tags directement depuis la page de l'article


# ============================================================
# CONFIGURATION TABLE 5 : RELATION ARTICLES ↔ TAGS
# ============================================================
@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag')
    search_fields = ('article__titre', 'tag__nom')


# ============================================================
# CONFIGURATION TABLE 6 : CHRONIQUES
# ============================================================
@admin.register(Chronique)
class ChroniqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteure', 'anonyme', 'statut', 'date_publication', 'vues')
    list_filter = ('statut', 'anonyme', 'date_publication')
    list_editable = ('statut',)
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}


# ============================================================
# CONFIGURATION TABLE 7 : NEWSLETTER
# ============================================================
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'prenom', 'source', 'date_inscription', 'actif')
    list_filter = ('actif', 'source', 'date_inscription')
    search_fields = ('email', 'prenom')


# ============================================================
# CONFIGURATION TABLE 8 : COMMENTAIRES
# ============================================================
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur_nom', 'article', 'approuve', 'date_creation')
    list_filter = ('approuve', 'date_creation')
    list_editable = ('approuve',)  # Valider ou rejeter un commentaire en un clic !
    search_fields = ('auteur_nom', 'auteur_email', 'contenu')


# ============================================================
# CONFIGURATION TABLE 9 : CONTACTS
# ============================================================
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sujet', 'type', 'lu', 'date_envoi')
    list_filter = ('lu', 'type', 'date_envoi')
    list_editable = ('lu',)
    search_fields = ('nom', 'email', 'sujet', 'message')


# ============================================================
# CONFIGURATION TABLE 10 : MÉDIATHÈQUE
# ============================================================
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'taille', 'article', 'date_upload')
    list_filter = ('type', 'date_upload')
    search_fields = ('nom',)


# ============================================================
# CONFIGURATION TABLE 11 : NOTIFICATIONS
# ============================================================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type', 'lu', 'date_creation')
    list_filter = ('lu', 'type', 'date_creation')
    list_editable = ('lu',)
    search_fields = ('message', 'utilisateur__nom')


# ============================================================
# CONFIGURATION TABLE 12 : FAVORIS
# ============================================================
@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'article', 'date_ajout')
    search_fields = ('utilisateur__nom', 'article__titre')


# ============================================================
# CONFIGURATION TABLE 13 : STATISTIQUES
# ============================================================
@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ('article', 'appareil', 'pays', 'adresse_ip', 'date_visite')
    list_filter = ('appareil', 'pays', 'date_visite')
    search_fields = ('article__titre', 'adresse_ip')


# ============================================================
# CONFIGURATION TABLE 14 : PARTENAIRES
# ============================================================
@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_web', 'actif', 'date_debut', 'date_fin')
    list_filter = ('actif',)
    list_editable = ('actif',)
    search_fields = ('nom', 'description')


# ============================================================
# CONFIGURATION TABLE 15 : CAMPAGNES NEWSLETTER
# ============================================================
@admin.register(CampagneNewsletter)
class CampagneNewsletterAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut', 'date_envoi', 'nombre_destinataires', 'taux_ouverture')
    list_filter = ('statut', 'date_envoi')
    search_fields = ('titre', 'contenu')


# ============================================================
# CONFIGURATION TABLE 16 : VISITES DU SITE
# ============================================================
@admin.register(VisiteSite)
class VisiteSiteAdmin(admin.ModelAdmin):
    list_display = ('date', 'nombre_visites')
    ordering = ('-date',)