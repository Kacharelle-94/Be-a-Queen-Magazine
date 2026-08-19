from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def seed_data(apps, schema_editor):
    # Get models
    Utilisateur = apps.get_model('magazine', 'Utilisateur')
    Rubrique = apps.get_model('magazine', 'Rubrique')
    Article = apps.get_model('magazine', 'Article')
    Chronique = apps.get_model('magazine', 'Chronique')
    
    # Create default user
    admin_user = Utilisateur.objects.create(
        nom="Sandra Pamela",
        email="admin@beaqueen.com",
        password=make_password("AdminQueen2026"),
        role="admin",
        is_admin=True,
        actif=True
    )
    
    # Create default rubriques
    sante = Rubrique.objects.create(
        nom="Santé & Bien-être",
        slug="sante-bien-etre",
        emoji="💫",
        description="Corps, esprit et équilibre. Des conseils pratiques et des routines pour te sentir bien dans ta peau.",
        ordre=1,
        active=True
    )
    
    healthy = Rubrique.objects.create(
        nom="Healthy People",
        slug="healthy-people",
        emoji="🌿",
        description="Des femmes inspirantes qui adoptent un mode de vie sain et équilibré. Leurs histoires, leurs habitudes.",
        ordre=2,
        active=True
    )
    
    entrepreneuriat = Rubrique.objects.create(
        nom="Entrepreneuriat",
        slug="entrepreneuriat",
        emoji="💼",
        description="Stratégies, conseils business et retours d'expérience pour créer et développer ton activité.",
        ordre=3,
        active=True
    )
    
    succes = Rubrique.objects.create(
        nom="Femmes de Succès",
        slug="femmes-de-succes",
        emoji="👑",
        description="Les parcours de femmes africaines qui brillent dans leurs domaines et ouvrent la voie.",
        ordre=4,
        active=True
    )
    
    actualites = Rubrique.objects.create(
        nom="Actualités",
        slug="actualites",
        emoji="📰",
        description="Un regard engagé sur l'actualité qui concerne les femmes et les sociétés africaines.",
        ordre=5,
        active=True
    )
    
    # Create articles
    # 1. Featured Article (Femmes de Succès)
    Article.objects.create(
        titre="Comment ces femmes africaines ont bâti leur empire sans attendre la permission de personne",
        slug="comment-ces-femmes-africaines-ont-bati-leur-empire",
        extrait="Elles ont défié les clichés, bravé les pressions sociales et construit des parcours qui inspirent une génération entière. Rencontre avec des reines qui ont choisi de briller.",
        contenu="""Bâtir un empire n'est jamais chose aisée. Pour les femmes africaines, les défis sont souvent doublés de barrières systémiques, culturelles et financières. Pourtant, sur tout le continent, une révolution silencieuse est en marche. Des femmes audacieuses tracent leur propre chemin, bâtissent des entreprises florissantes et redéfinissent le leadership au féminin.

De Lagos à Nairobi, de Dakar à Johannesburg, ces entrepreneures prouvent que la persévérance et la vision sont des leviers indestructibles. Elles n'attendent plus qu'on leur donne une place à la table : elles construisent leur propre table.

Le premier secret de leur réussite réside dans l'éducation et l'entraide. En créant des réseaux solides et en s'appuyant sur le mentorat, elles transmettent les clés du succès aux générations futures.

Le second pilier est l'innovation locale. En répondant à des problématiques spécifiques de leurs communautés (services financiers mobiles, agriculture durable, e-commerce adapté), elles se positionnent sur des marchés à forte valeur ajoutée.

Ce parcours inspirant nous montre que chaque femme est capable de créer sa propre réussite. N'attendez plus la permission : osez, planifiez, et bâtissez votre empire dès aujourd'hui.""",
        rubrique=succes,
        auteure=admin_user,
        statut="publie",
        en_une=True,
        date_publication=timezone.now(),
        temps_lecture=6
    )
    
    # 2. Secondary Article (Santé & Bien-être)
    Article.objects.create(
        titre="5 routines matinales pour démarrer ta journée avec puissance",
        slug="5-routines-matinales-demarrer-journee-puissance",
        extrait="Corps et esprit alignés dès le réveil.",
        contenu="""La manière dont vous commencez votre matinée détermine la trajectoire de toute votre journée. Adopter des habitudes saines dès le réveil permet de réduire le stress, d'accroître votre concentration et de booster votre énergie vitale. Voici 5 routines à intégrer dans votre quotidien :

1. L'éveil corporel doux : Prenez 5 minutes pour vous étirer. Réveillez vos articulations et respirez profondément pour oxygéner votre cerveau.
2. L'hydratation : Buvez un grand verre d'eau tempérée, éventuellement avec un filet de citron, pour relancer votre système digestif.
3. La méditation ou gratitude : Installez-vous au calme et formulez trois choses pour lesquelles vous êtes reconnaissante aujourd'hui.
4. L'écriture libre : Posez vos pensées ou vos objectifs sur papier pour désencombrer votre esprit.
5. Un petit-déjeuner nutritif : Privilégiez des aliments riches en fibres et en protéines pour une énergie stable tout au long de la matinée.

Essayez ces étapes pendant 21 jours et observez le changement dans votre attitude et votre productivité !""",
        rubrique=sante,
        auteure=admin_user,
        statut="publie",
        en_une=False,
        date_publication=timezone.now(),
        temps_lecture=4
    )
    
    # 3. Secondary Article (Entrepreneuriat)
    Article.objects.create(
        titre="Lancer son business en ligne depuis l'Afrique : guide complet",
        slug="lancer-son-business-en-ligne-depuis-afrique",
        extrait="Les stratégies qui fonctionnent vraiment.",
        contenu="""L'économie numérique en Afrique connaît une croissance sans précédent. Grâce à internet, il est désormais possible de toucher une clientèle locale et internationale sans disposer de capitaux de départ astronomiques. Voici les étapes clés pour lancer votre business en ligne :

1. Valider son idée : Identifiez un problème réel dans votre communauté et proposez une solution simple. Testez votre concept auprès de votre entourage ou sur les réseaux sociaux.
2. Choisir son canal : Vous n'avez pas nécessairement besoin d'un site web complexe au début. Les réseaux sociaux comme Instagram, WhatsApp Business et TikTok sont d'excellentes vitrines de départ.
3. Configurer les moyens de paiement : Intégrez des solutions de paiement mobile (Mobile Money), très populaires sur le continent, en plus des cartes bancaires.
4. Structurer sa logistique : Le service client et la rapidité de livraison sont vos meilleurs atouts de fidélisation. Associez-vous avec des livreurs locaux fiables.

La persévérance est la clé. Le digital demande du temps pour construire une relation de confiance avec vos abonnés.""",
        rubrique=entrepreneuriat,
        auteure=admin_user,
        statut="publie",
        en_une=False,
        date_publication=timezone.now(),
        temps_lecture=8
    )
    
    # 4. Secondary Article (Healthy People)
    Article.objects.create(
        titre="Aïcha, 32 ans, a transformé sa vie en adoptant 3 habitudes simples",
        slug="aicha-transforme-vie-3-habitudes-simples",
        extrait="Son histoire et ses secrets de bien-être.",
        contenu="""À 32 ans, Aïcha cumulait une carrière stressante dans la finance et une fatigue chronique qui l'empêchait de profiter de sa vie de famille. C'est à la suite d'un bilan de santé alarmant qu'elle a décidé de tout changer. Pas à pas, sans régime drastique ni routine insurmontable, elle a instauré 3 habitudes simples :

1. La marche quotidienne : 30 minutes de marche active à l'air libre chaque jour après le déjeuner. Cela a considérablement amélioré sa digestion et son sommeil.
2. La déconnexion numérique : Éteindre tous les écrans (téléphone, ordinateur, télévision) une heure avant le coucher pour lire ou méditer.
3. L'alimentation intuitive : Remplacer les plats industriels rapides par des produits frais locaux, en écoutant sa faim réelle plutôt que son stress.

"Je me sens plus vivante et plus sereine que jamais", confie Aïcha. Son témoignage montre que le bien-être n'est pas une destination lointaine, mais un choix quotidien.""",
        rubrique=healthy,
        auteure=admin_user,
        statut="publie",
        en_une=False,
        date_publication=timezone.now(),
        temps_lecture=5
    )
    
    # 5. Secondary Article (Actualités)
    Article.objects.create(
        titre="Les femmes africaines et la tech : une révolution silencieuse",
        slug="femmes-africaines-tech-revolution-silencieuse",
        extrait="Chiffres, témoignages et perspectives.",
        contenu="""Longtemps sous-représentées dans les filières scientifiques et techniques, les femmes africaines sont en train de prendre d'assaut le secteur de la technologie. À travers des bootcamps de codage, des incubateurs dédiés et des initiatives universitaires, une nouvelle génération de codeuses, de data scientists et de fondatrices de start-ups émerge.

Cette montée en puissance est essentielle pour le développement économique du continent. En effet, en apportant leur vision propre, ces professionnelles développent des solutions technologiques qui répondent directement aux besoins des femmes (santé maternelle, micro-crédits, éducation).

Des organisations engagées soutiennent ce mouvement en proposant des bourses d'études et des programmes de mentorat. L'avenir de la tech en Afrique sera féminin et résolument novateur.""",
        rubrique=actualites,
        auteure=admin_user,
        statut="publie",
        en_une=False,
        date_publication=timezone.now(),
        temps_lecture=5
    )
    
    # Create chroniques
    Chronique.objects.create(
        titre="La nuit où j'ai décidé de me choisir moi",
        slug="la-nuit-decide-me-choisir-moi",
        contenu="""Pendant des années, j'ai vécu pour plaire aux autres. J'étais la fille parfaite, la fiancée idéale, l'employée modèle. Je cochais toutes les cases d'une vie réussie selon les critères de ma famille et de la société. Mais chaque soir, en rentrant chez moi, je ressentais un vide immense.

C'est lors d'une nuit de décembre, alors que le silence enveloppait la ville, que j'ai fondu en larmes. Je me suis regardée dans le miroir et je ne me suis pas reconnue. J'avais sacrifié mes rêves, mes passions et ma paix intérieure pour acheter l'approbation d'autrui.

Cette nuit-là, j'ai pris la décision la plus effrayante et la plus libératrice de mon existence : j'ai décidé de me choisir moi. J'ai rompu des relations toxiques, j'ai quitté mon emploi stable pour me lancer dans ma passion de l'écriture et j'ai commencé à dire 'non'. Le chemin de la reconstruction a été long et semé d'embûches, mais aujourd'hui, je porte ma couronne fièrement. Je ne vis plus dans l'ombre des attentes des autres.""",
        auteure=admin_user,
        anonyme=False,
        statut="publie",
        date_publication=timezone.now()
    )
    
    Chronique.objects.create(
        titre="Mon silence était ma prison",
        slug="mon-silence-etait-ma-prison",
        contenu="""On m'a toujours appris qu'une femme sage doit savoir se taire. Garder le silence face à l'injustice, face aux mots blessants, face aux abus légers du quotidien. 'C'est la tradition, c'est pour préserver la paix du foyer', me disait-on. Alors, j'ai tu ma voix. J'ai avalé mes colères et étouffé mes larmes.

Mais ce silence est devenu ma prison. Il me rongeait de l'intérieur, détruisant ma confiance en moi et ma joie de vivre. Je me sentais spectatrice de ma propre vie, enfermée dans une cellule dont j'avais moi-même accepté de porter la clé sans jamais oser tourner la serrure.

Jusqu'au jour où j'ai compris que mon silence ne protégeait pas la paix, il protégeait le confort de ceux qui m'oppressaient. J'ai commencé à parler. D'abord doucement, d'une voix tremblante, puis avec assurance. Parler a été ma thérapie. Briser le silence, c'est abattre les murs de sa prison. Aujourd'hui, je parle pour que d'autres reines sachent que leur voix a de la valeur.""",
        auteure=admin_user,
        anonyme=True,
        statut="publie",
        date_publication=timezone.now()
    )
    
    Chronique.objects.create(
        titre="Je suis revenue de loin pour devenir moi",
        slug="je-suis-revenue-de-loin-devenir-moi",
        contenu="""La vie a cette capacité de vous mettre à terre quand vous vous y attendez le moins. Divorce difficile, faillite de ma première boutique, rejet de mes proches... En l'espace de six mois, j'ai perdu tout ce qui définissait ma sécurité matérielle et émotionnelle. J'ai touché le fond.

Beaucoup pensaient que je ne m'en relèverais pas. Et pour être honnête, j'ai failli abandonner. Mais dans les moments les plus sombres, une petite étincelle de résilience refuse de s'éteindre. J'ai compris que ma valeur ne dépendait pas de mes possessions ni de mon statut marital.

Je suis revenue de loin. J'ai reconstruit ma vie brique par brique, avec plus de sagesse, de force et de gratitude. Chaque cicatrice sur mon âme est aujourd'hui un témoin de ma victoire. Je ne suis plus la victime des circonstances, je suis la créatrice de mon destin.""",
        auteure=admin_user,
        anonyme=False,
        statut="publie",
        date_publication=timezone.now()
    )

class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
