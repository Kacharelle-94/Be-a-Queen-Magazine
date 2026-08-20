import json
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Article, Rubrique, Chronique,
    Newsletter, Contact, Commentaire, VisiteSite
)


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

def accueil(request):
    # Rubriques actives
    rubriques = Rubrique.objects.filter(active=True).order_by('ordre')

    # Articles en une (max 1 article principal)
    article_principal = Article.objects.filter(
        statut='publie',
        en_une=True
    ).order_by('-date_publication').first()

    # 4 derniers articles secondaires
    articles_secondaires = Article.objects.filter(
        statut='publie'
    ).exclude(
        id=article_principal.id if article_principal else 0
    ).order_by('-date_publication')[:4]

    # 3 dernières Chroniques de Reines
    chroniques = Chronique.objects.filter(
        statut='publie'
    ).order_by('-date_publication')[:3]

    context = {
        'rubriques'           : rubriques,
        'article_principal'   : article_principal,
        'articles_secondaires': articles_secondaires,
        'chroniques'          : chroniques,
    }
    return render(request, 'magazine/index.html', context)


# ============================================================
# PAGE RUBRIQUE
# ============================================================

def rubrique(request, slug):
    rub             = get_object_or_404(Rubrique, slug=slug, active=True)
    articles        = Article.objects.filter(
        rubrique=rub,
        statut='publie'
    ).order_by('-date_publication')
    toutes_rubriques = Rubrique.objects.filter(active=True).order_by('ordre')

    context = {
        'rubrique'        : rub,
        'articles'        : articles,
        'toutes_rubriques': toutes_rubriques,
    }
    return render(request, 'magazine/rubrique.html', context)


# ============================================================
# PAGE ARTICLE
# ============================================================

def article(request, slug):
    art = get_object_or_404(Article, slug=slug, statut='publie')

    # Incrémenter le compteur de vues
    art.vues += 1
    art.save(update_fields=['vues'])

    # Commentaires approuvés
    commentaires = art.commentaires.filter(approuve=True).order_by('date_creation')

    # Articles similaires (même rubrique)
    articles_similaires = Article.objects.filter(
        rubrique=art.rubrique,
        statut='publie'
    ).exclude(id=art.id).order_by('-date_publication')[:3]

    context = {
        'article'            : art,
        'commentaires'      : commentaires,
        'articles_similaires': articles_similaires,
    }
    return render(request, 'magazine/article.html', context)


# ============================================================
# PAGE CHRONIQUES DE REINES
# ============================================================

def chroniques(request):
    recits = Chronique.objects.filter(
        statut='publie'
    ).order_by('-date_publication')

    context = {'chroniques': recits}
    return render(request, 'magazine/chroniques.html', context)


# ============================================================
# PAGE À PROPOS
# ============================================================

def a_propos(request):
    return render(request, 'magazine/a_propos.html')


# ============================================================
# PAGE CONTACT
# ============================================================

def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            nom     = request.POST.get('nom', ''),
            email   = request.POST.get('email', ''),
            sujet   = request.POST.get('sujet', ''),
            type    = request.POST.get('type', 'autre'),
            message = request.POST.get('message', ''),
        )
        return render(request, 'magazine/contact.html', {'envoye': True})

    return render(request, 'magazine/contact.html')


# ============================================================
# NEWSLETTER (inscription)
# ============================================================

def newsletter(request):
    if request.method == 'POST':
        email  = request.POST.get('email', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        source = request.POST.get('source', 'accueil')

        if email:
            obj, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={
                    'prenom': prenom,
                    'source': source,
                    'actif' : True,
                }
            )

            sujet = "👑 Bienvenue dans la communauté des Reines !"
            message = f"""Bonjour {prenom if prenom else 'Reine'},

Merci de t'être abonnée à la newsletter de Be a Queen Magazine.

Nous sommes ravis de t'accueillir dans notre communauté de femmes fortes, inspirantes et ambitieuses.
Tu recevras bientôt nos chroniques exclusives, nos meilleurs articles et nos conseils directement dans ta boîte mail.

N'oublie pas : chaque femme porte une couronne qu'elle ne voit pas encore. Il est temps de porter la tienne.

À très vite,
Sandra Pamela Makoulo
Fondatrice de Be a Queen Magazine
"""
            try:
                send_mail(
                    sujet,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"============== ERREUR D'ENVOI D'EMAIL ==============\n{e}\n====================================================")

    return redirect('accueil')


# ============================================================
# COMMENTAIRE (ajout)
# ============================================================

def ajouter_commentaire(request, slug):
    art = get_object_or_404(Article, slug=slug, statut='publie')

    if request.method == 'POST':
        Commentaire.objects.create(
            article      = art,
            auteur_nom   = request.POST.get('nom', ''),
            auteur_email = request.POST.get('email', ''),
            contenu      = request.POST.get('contenu', ''),
            approuve     = False,
        )

    return redirect('article', slug=slug)


# ============================================================
# PRODUITS & BOUTIQUE
# ============================================================

def produits(request):
    """
    Affiche la liste des produits et services de la boutique.
    """
    return render(request, 'magazine/produits.html')


def produit_detail(request, slug):
    """
    Affiche les détails d'un produit ou service spécifique.
    """
    titre_produit = slug.replace('-', ' ').title()
    
    return render(request, 'magazine/produit_detail.html', {
        'titre': titre_produit,
        'slug': slug
    })


# ============================================================
# STATISTIQUES DE VISITES
# ============================================================

def statistiques(request):
    import json
    aujourd_hui = timezone.now().date()

    # --- Visites par jour (les 30 derniers jours) ---
    debut_mois = aujourd_hui - timedelta(days=29)
    visites_30j = VisiteSite.objects.filter(date__gte=debut_mois).order_by('date')

    visites_dict = {v.date: v.nombre_visites for v in visites_30j}

    labels_jours = []
    data_jours   = []
    for i in range(30):
        jour = debut_mois + timedelta(days=i)
        labels_jours.append(jour.strftime('%d/%m'))
        data_jours.append(visites_dict.get(jour, 0))

    # --- Visites par semaine (les 12 dernières semaines) ---
    labels_semaines = []
    data_semaines   = []
    for i in range(11, -1, -1):
        debut_sem = aujourd_hui - timedelta(weeks=i+1) + timedelta(days=1)
        fin_sem   = aujourd_hui - timedelta(weeks=i)
        visites_semaine = VisiteSite.objects.filter(date__gte=debut_sem, date__lte=fin_sem)
        total_semaine_val = visites_semaine.aggregate(t=Sum('nombre_visites'))['t'] or 0
        labels_semaines.append(f"Sem. {debut_sem.strftime('%d/%m')}")
        data_semaines.append(total_semaine_val)

    # --- Totaux ---
    total_global  = VisiteSite.objects.aggregate(t=Sum('nombre_visites'))['t'] or 0
    total_ce_mois = sum(data_jours)
    total_semaine = data_semaines[-1] if data_semaines else 0
    total_aujourd = visites_dict.get(aujourd_hui, 0)

    # --- Tableau des 14 derniers jours ---
    max_visites = max([visites_dict.get(aujourd_hui - timedelta(days=i), 0) for i in range(14)] or [1])
    derniers_jours = []
    for i in range(14):
        jour = aujourd_hui - timedelta(days=i)
        nb = visites_dict.get(jour, 0)
        pct = int((nb / max_visites) * 100) if max_visites > 0 else 0
        derniers_jours.append({
            'date'   : jour.strftime('%A %d %B %Y'),
            'visites': nb,
            'pct'    : pct,
        })

    context = {
        'labels_jours'   : json.dumps(labels_jours),
        'data_jours'     : json.dumps(data_jours),
        'labels_semaines': json.dumps(labels_semaines),
        'data_semaines'  : json.dumps(data_semaines),
        'total_global'   : total_global,
        'total_ce_mois'  : total_ce_mois,
        'total_semaine'  : total_semaine,
        'total_aujourd'  : total_aujourd,
        'derniers_jours' : derniers_jours,
    }
    return render(request, 'magazine/statistiques.html', context)