from django.urls import path
from . import views

urlpatterns = [
    # Accueil
    path('', views.accueil, name='accueil'),

    # Rubriques
    path('rubrique/<slug:slug>/', views.rubrique, name='rubrique'),

    # Articles
    path('article/<slug:slug>/', views.article, name='article'),

    # Chroniques de Reines
    path('chroniques/', views.chroniques, name='chroniques'),

    # À propos
    path('a-propos/', views.a_propos, name='a_propos'),

    # Contact
    path('contact/', views.contact, name='contact'),

    # Newsletter
    path('newsletter/', views.newsletter, name='newsletter'),

    # Commentaire
    path('article/<slug:slug>/commenter/', views.ajouter_commentaire, name='commenter'),

    # Produits
    path('produits/', views.produits, name='produits'),
    path('produits/<slug:slug>/', views.produit_detail, name='produit_detail'),

    # Statistiques de visites (accès réservé à Sandra)
    path('statistiques/', views.statistiques, name='statistiques'),
    
]