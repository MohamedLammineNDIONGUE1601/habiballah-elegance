import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from boutique.models import Categorie, Produit

CATEGORIES = [
    ("Abayas", "Des abayas fluides et élégantes, pour toutes les occasions."),
    ("Robes", "Des robes modestes et raffinées, aux coupes intemporelles."),
    ("Hijabs & Voiles", "Une sélection de tissus doux et soyeux."),
    ("Accessoires", "Bijoux discrets, ceintures et pochettes assortis."),
]

PRODUITS = [
    ("Abaya Noor perle brodée", "Abayas", 45000, None, "Crêpe de soie", True),
    ("Abaya Zahra col brodé or", "Abayas", 52000, 46000, "Nida premium", True),
    ("Robe Amira plissée", "Robes", 38000, None, "Mousseline doublée", True),
    ("Robe Sofia manches longues", "Robes", 33000, None, "Coton lourd", False),
    ("Hijab soie Médina", "Hijabs & Voiles", 8500, None, "Soie de Médine", True),
    ("Hijab jersey premium", "Hijabs & Voiles", 6000, 5000, "Jersey extensible", False),
    ("Ceinture dorée fine", "Accessoires", 7000, None, "Cuir synthétique", False),
    ("Pochette brodée Chérifs", "Accessoires", 12500, None, "Velours brodé", True),
]


def image_placeholder(nom, couleur_fond=(20, 17, 22)):
    img = Image.new("RGB", (800, 1000), couleur_fond)
    draw = ImageDraw.Draw(img)
    # cadre doré
    draw.rectangle([20, 20, 779, 979], outline=(201, 162, 75), width=3)
    draw.rectangle([34, 34, 765, 965], outline=(139, 108, 46), width=1)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    texte = "HABIBALLAH\nÉLÉGANCE"
    draw.multiline_text((400, 460), texte, fill=(201, 162, 75), anchor="mm", align="center", font=font, spacing=12)
    draw.text((400, 540), nom, fill=(168, 158, 140), anchor="mm", font=font)
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=88)
    return ContentFile(buffer.getvalue(), name=f"{nom}.jpg")


def run():
    cat_objs = {}
    for i, (nom, desc) in enumerate(CATEGORIES):
        cat, _ = Categorie.objects.get_or_create(nom=nom, defaults={"description": desc, "ordre": i})
        cat_objs[nom] = cat
    print(f"Catégories : {Categorie.objects.count()}")

    for nom, cat_nom, prix, promo, matiere, coeur in PRODUITS:
        if Produit.objects.filter(nom=nom).exists():
            continue
        p = Produit(
            nom=nom,
            categorie=cat_objs[cat_nom],
            description=f"{nom} — une pièce {cat_nom.lower()} pensée pour l'élégance et le confort au quotidien.",
            matiere=matiere,
            prix=prix,
            prix_promo=promo,
            stock=12,
            disponible=True,
            coup_de_coeur=coeur,
        )
        p.image_principale.save(f"{nom}.jpg", image_placeholder(nom), save=False)
        p.save()
    print(f"Produits : {Produit.objects.count()}")


if __name__ == "__main__":
    run()
