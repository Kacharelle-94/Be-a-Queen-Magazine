from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# ============================================================
# TABLE 1 : UTILISATEURS / ADMINS
# ============================================================

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom, password=None):
        if not email:
            raise ValueError("L'email est obligatoire")
        utilisateur = self.model(email=self.normalize_email(email), nom=nom)
        utilisateur.set_password(password)
        utilisateur.save(using=self._db)
        return utilisateur

    def create_superuser(self, email, nom, password=None):
        utilisateur = self.create_user(email, nom, password)
        utilisateur.role = 'admin'
        utilisateur.is_admin = True
        utilisateur.save(using=self._db)
        return utilisateur


class Utilisateur(AbstractBaseUser):
    ROLES = [
        ('admin',    'Administratrice'),
        ('auteure',  'Auteure'),
        ('editrice', 'Éditrice'),
    ]

    nom               = models.CharField(max_length=150, verbose_name="Nom complet")
    email             = models.EmailField(max_length=191, unique=True, verbose_name="Email")
    role              = models.CharField(max_length=20, choices=ROLES, default='auteure', verbose_name="Rôle")
    photo             = models.ImageField(upload_to='profils/', blank=True, null=True, verbose_name="Photo de profil")
    bio               = models.TextField(blank=True, null=True, verbose_name="Biographie")
    date_inscription  = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")
    actif             = models.BooleanField(default=True, verbose_name="Compte actif")
    is_admin          = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nom']

    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.nom} ({self.role})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name        = "Utilisatrice"
        verbose_name_plural = "Utilisatrices"
        db_table            = "utilisateurs"


# ============================================================
# TABLE 2 : RUBRIQUES
# ============================================================

class Rubrique(models.Model):
    nom         = models.CharField(max_length=100, verbose_name="Nom")
    slug        = models.SlugField(max_length=100, unique=True, verbose_name="Slug URL")
    emoji       = models.CharField(max_length=10, blank=True, verbose_name="Emoji")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre       = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    active      = models.BooleanField(default=True, verbose_name="Rubrique active")

    def __str__(self):
        return f"{self.emoji} {self.nom}"

    class Meta:
        ordering            = ['ordre']
        verbose_name        = "Rubrique"
        verbose_name_plural = "Rubriques"
        db_table            = "rubriques"


# ============================================================
# TABLE 4 : TAGS
# ============================================================

class Tag(models.Model):
    nom  = models.CharField(max_length=80, unique=True, verbose_name="Nom du tag")
    slug = models.SlugField(max_length=80, unique=True, verbose_name="Slug URL")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name        = "Tag"
        verbose_name_plural = "Tags"
        db_table            = "tags"


# ============================================================
# TABLE 3 : ARTICLES
# (après Tag car articles utilise tags via ManyToMany)
# ============================================================

class Article(models.Model):
    STATUTS = [
        ('brouillon', 'Brouillon'),
        ('publie',    'Publié'),
        ('archive',   'Archivé'),
    ]

    titre              = models.CharField(max_length=191, verbose_name="Titre")
    slug               = models.SlugField(max_length=191, unique=True, verbose_name="Slug URL")
    extrait            = models.TextField(blank=True, verbose_name="Extrait / Résumé")
    contenu            = models.TextField(verbose_name="Contenu complet")
    image_principale   = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Image de couverture")
    rubrique           = models.ForeignKey(Rubrique, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name="Rubrique")
    auteure            = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name="Auteure")
    tags               = models.ManyToManyField(Tag, through='ArticleTag', blank=True, verbose_name="Tags")
    statut             = models.CharField(max_length=20, choices=STATUTS, default='brouillon', verbose_name="Statut")
    en_une             = models.BooleanField(default=False, verbose_name="Afficher en une")
    date_publication   = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    date_modification  = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    vues               = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")
    temps_lecture      = models.PositiveIntegerField(default=5, verbose_name="Temps de lecture (min)")

    def __str__(self):
        return self.titre

    class Meta:
        ordering            = ['-date_publication']
        verbose_name        = "Article"
        verbose_name_plural = "Articles"
        db_table            = "articles"


# ============================================================
# TABLE 5 : ARTICLES ↔ TAGS (table de liaison)
# ============================================================

class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    tag     = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")

    def __str__(self):
        return f"{self.article.titre} — {self.tag.nom}"

    class Meta:
        unique_together     = ('article', 'tag')
        verbose_name        = "Tag d'article"
        verbose_name_plural = "Tags d'articles"
        db_table            = "articles_tags"


# ============================================================
# TABLE 6 : CHRONIQUES DE REINES
# ============================================================

class Chronique(models.Model):
    STATUTS = [
        ('brouillon', 'Brouillon'),
        ('publie',    'Publié'),
        ('archive',   'Archivé'),
    ]

    titre            = models.CharField(max_length=191, verbose_name="Titre du récit")
    slug             = models.SlugField(max_length=191, unique=True, verbose_name="Slug URL")
    contenu          = models.TextField(verbose_name="Contenu du récit")
    auteure          = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='chroniques', verbose_name="Auteure")
    anonyme          = models.BooleanField(default=False, verbose_name="Récit anonyme")
    image            = models.ImageField(upload_to='chroniques/', blank=True, null=True, verbose_name="Image d'illustration")
    statut           = models.CharField(max_length=20, choices=STATUTS, default='brouillon', verbose_name="Statut")
    date_publication = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    vues             = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")

    def __str__(self):
        return self.titre

    class Meta:
        ordering            = ['-date_publication']
        verbose_name        = "Chronique de Reine"
        verbose_name_plural = "Chroniques de Reines"
        db_table            = "chroniques"


# ============================================================
# TABLE 7 : NEWSLETTER
# ============================================================

class Newsletter(models.Model):
    SOURCES = [
        ('accueil',  'Page d\'accueil'),
        ('popup',    'Popup'),
        ('article',  'Article'),
        ('footer',   'Footer'),
        ('autre',    'Autre'),
    ]

    email               = models.EmailField(max_length=191, unique=True, verbose_name="Adresse email")
    prenom              = models.CharField(max_length=80, blank=True, verbose_name="Prénom")
    actif               = models.BooleanField(default=True, verbose_name="Abonnement actif")
    date_inscription    = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")
    date_desinscription = models.DateTimeField(blank=True, null=True, verbose_name="Date de désabonnement")
    source              = models.CharField(max_length=20, choices=SOURCES, default='accueil', verbose_name="Source d'inscription")

    def __str__(self):
        return self.email

    class Meta:
        ordering            = ['-date_inscription']
        verbose_name        = "Abonnée Newsletter"
        verbose_name_plural = "Abonnées Newsletter"
        db_table            = "newsletter"


# ============================================================
# TABLE 8 : COMMENTAIRES
# ============================================================

class Commentaire(models.Model):
    article       = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires', verbose_name="Article")
    auteur_nom    = models.CharField(max_length=100, verbose_name="Nom")
    auteur_email  = models.EmailField(verbose_name="Email (non affiché)")
    contenu       = models.TextField(verbose_name="Commentaire")
    approuve      = models.BooleanField(default=False, verbose_name="Approuvé")
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date")

    def __str__(self):
        return f"{self.auteur_nom} sur « {self.article.titre} »"

    class Meta:
        ordering            = ['-date_creation']
        verbose_name        = "Commentaire"
        verbose_name_plural = "Commentaires"
        db_table            = "commentaires"


# ============================================================
# TABLE 9 : MESSAGES DE CONTACT
# ============================================================

class Contact(models.Model):
    TYPES = [
        ('partenariat', 'Partenariat'),
        ('presse',      'Presse'),
        ('recrutement', 'Recrutement'),
        ('temoignage',  'Témoignage / Chronique'),
        ('autre',       'Autre'),
    ]

    nom        = models.CharField(max_length=150, verbose_name="Nom")
    email      = models.EmailField(verbose_name="Email")
    sujet      = models.CharField(max_length=191, verbose_name="Sujet")
    type       = models.CharField(max_length=20, choices=TYPES, default='autre', verbose_name="Type de demande")
    message    = models.TextField(verbose_name="Message")
    lu         = models.BooleanField(default=False, verbose_name="Lu")
    date_envoi = models.DateTimeField(default=timezone.now, verbose_name="Date d'envoi")

    def __str__(self):
        return f"{self.nom} — {self.sujet}"

    class Meta:
        ordering            = ['-date_envoi']
        verbose_name        = "Message de contact"
        verbose_name_plural = "Messages de contact"
        db_table            = "contacts"


# ============================================================
# TABLE 10 : MÉDIATHÈQUE
# ============================================================

class Media(models.Model):
    TYPES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
        ('pdf',   'PDF'),
    ]

    nom          = models.CharField(max_length=191, verbose_name="Nom du fichier")
    url          = models.FileField(upload_to='mediatheque/', verbose_name="Fichier")
    type         = models.CharField(max_length=10, choices=TYPES, default='image', verbose_name="Type")
    taille       = models.PositiveIntegerField(default=0, verbose_name="Taille (Ko)")
    article      = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, related_name='medias', verbose_name="Article associé")
    date_upload  = models.DateTimeField(default=timezone.now, verbose_name="Date d'upload")

    def __str__(self):
        return self.nom

    class Meta:
        ordering            = ['-date_upload']
        verbose_name        = "Média"
        verbose_name_plural = "Médiathèque"
        db_table            = "medias"


# ============================================================
# TABLE 11 : NOTIFICATIONS
# ============================================================

class Notification(models.Model):
    TYPES = [
        ('nouveau_commentaire', 'Nouveau commentaire'),
        ('nouveau_contact',     'Nouveau message de contact'),
        ('nouvel_abonne',       'Nouvelle abonnée newsletter'),
        ('nouvel_article',      'Nouvel article publié'),
    ]

    utilisateur   = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications', verbose_name="Destinataire")
    message       = models.TextField(verbose_name="Message")
    type          = models.CharField(max_length=30, choices=TYPES, verbose_name="Type")
    lu            = models.BooleanField(default=False, verbose_name="Lu")
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date")

    def __str__(self):
        return f"{self.type} — {self.utilisateur.nom}"

    class Meta:
        ordering            = ['-date_creation']
        verbose_name        = "Notification"
        verbose_name_plural = "Notifications"
        db_table            = "notifications"


# ============================================================
# TABLE 12 : ARTICLES FAVORIS
# ============================================================

class Favori(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='favoris', verbose_name="Utilisatrice")
    article     = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favoris', verbose_name="Article")
    date_ajout  = models.DateTimeField(default=timezone.now, verbose_name="Date d'ajout")

    def __str__(self):
        return f"{self.utilisateur.nom} ❤ {self.article.titre}"

    class Meta:
        unique_together     = ('utilisateur', 'article')
        ordering            = ['-date_ajout']
        verbose_name        = "Favori"
        verbose_name_plural = "Favoris"
        db_table            = "favoris"


# ============================================================
# TABLE 13 : STATISTIQUES DE VISITES
# ============================================================

class Statistique(models.Model):
    APPAREILS = [
        ('mobile',   'Mobile'),
        ('desktop',  'Ordinateur'),
        ('tablette', 'Tablette'),
    ]

    article     = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='statistiques', verbose_name="Article")
    adresse_ip  = models.GenericIPAddressField(blank=True, null=True, verbose_name="Adresse IP")
    pays        = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    appareil    = models.CharField(max_length=10, choices=APPAREILS, blank=True, verbose_name="Appareil")
    date_visite = models.DateTimeField(default=timezone.now, verbose_name="Date de visite")

    def __str__(self):
        return f"Visite — {self.article.titre} — {self.date_visite.strftime('%d/%m/%Y')}"

    class Meta:
        ordering            = ['-date_visite']
        verbose_name        = "Statistique"
        verbose_name_plural = "Statistiques"
        db_table            = "statistiques"


# ============================================================
# TABLE 14 : PARTENAIRES
# ============================================================

class Partenaire(models.Model):
    nom         = models.CharField(max_length=150, verbose_name="Nom du partenaire")
    logo        = models.ImageField(upload_to='partenaires/', blank=True, null=True, verbose_name="Logo")
    site_web    = models.URLField(blank=True, verbose_name="Site web")
    description = models.TextField(blank=True, verbose_name="Description")
    actif       = models.BooleanField(default=True, verbose_name="Partenariat actif")
    date_debut  = models.DateField(blank=True, null=True, verbose_name="Début du partenariat")
    date_fin    = models.DateField(blank=True, null=True, verbose_name="Fin du partenariat")

    def __str__(self):
        return self.nom

    class Meta:
        ordering            = ['nom']
        verbose_name        = "Partenaire"
        verbose_name_plural = "Partenaires"
        db_table            = "partenaires"


# ============================================================
# TABLE 15 : CAMPAGNES NEWSLETTER
# ============================================================

class CampagneNewsletter(models.Model):
    STATUTS = [
        ('brouillon', 'Brouillon'),
        ('envoyee',   'Envoyée'),
        ('planifiee', 'Planifiée'),
    ]

    titre                = models.CharField(max_length=191, verbose_name="Titre de la campagne")
    contenu              = models.TextField(verbose_name="Corps de l'email")
    statut               = models.CharField(max_length=20, choices=STATUTS, default='brouillon', verbose_name="Statut")
    date_envoi           = models.DateTimeField(blank=True, null=True, verbose_name="Date d'envoi")
    nombre_destinataires = models.PositiveIntegerField(default=0, verbose_name="Nombre de destinataires")
    taux_ouverture       = models.FloatField(default=0.0, verbose_name="Taux d'ouverture (%)")

    def __str__(self):
        return self.titre

    class Meta:
        ordering            = ['-date_envoi']
        verbose_name        = "Campagne Newsletter"
        verbose_name_plural = "Campagnes Newsletter"
        db_table            = "campagnes_newsletter"

# ============================================================
# TABLE 16 : VISITES DU SITE GLOBALES
# ============================================================

class VisiteSite(models.Model):
    date = models.DateField(default=timezone.now, unique=True, verbose_name="Date")
    nombre_visites = models.PositiveIntegerField(default=0, verbose_name="Nombre de visites")

    def __str__(self):
        return f"Visites le {self.date} : {self.nombre_visites}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Visite du site"
        verbose_name_plural = "Visites du site"
        db_table = "visites_site"