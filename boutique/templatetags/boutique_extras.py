from django import template

register = template.Library()


@register.filter(name="fcfa")
def fcfa(valeur):
    """Formate un nombre en FCFA avec des espaces comme séparateurs de milliers."""
    try:
        valeur = int(valeur)
    except (TypeError, ValueError):
        return valeur
    return f"{valeur:,}".replace(",", " ") + " FCFA"
