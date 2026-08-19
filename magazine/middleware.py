from django.utils.timezone import now
from magazine.models import VisiteSite

class VisiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ignorer les requetes admin, static, media
        if not request.path.startswith('/admin/') and \
           not request.path.startswith('/media/') and \
           not request.path.startswith('/static/'):

            # Compter uniquement une visite par session par jour
            if not request.session.get('has_visited_today'):
                request.session['has_visited_today'] = True
                aujourd_hui = now().date()
                visite, created = VisiteSite.objects.get_or_create(date=aujourd_hui)
                visite.nombre_visites += 1
                visite.save(update_fields=['nombre_visites'])

        response = self.get_response(request)
        return response
