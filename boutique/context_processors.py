from django.conf import settings
from .panier import Panier
from .models import Categorie


def contexte_global(request):
    return {
        "panier_global": Panier(request),
        "site_name": settings.SITE_NAME,
        "site_address": settings.SITE_ADDRESS,
        "site_phone": settings.SITE_PHONE,
        "site_email": settings.SITE_EMAIL,
        "menu_categories": Categorie.objects.all(),
    }
