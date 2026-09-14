# Habiballah Élégance — Boutique en ligne

Site e-commerce Django pour la boutique **Habiballah Élégance**
(Médina Gounass, Matam / Sénégal — chez la maison des Chérifs).

## Stack
- Django 6 (Python)
- HTML / CSS (thème noir & or fait main, sans framework CSS)
- JavaScript vanilla (menu mobile, quantités, galerie)
- SQLite (base par défaut, changeable en PostgreSQL/MySQL)

## Fonctionnalités
- Catalogue avec catégories, recherche et tri par prix
- Fiche produit (galerie, description, matière, prix promo)
- Panier basé sur la session (aucune inscription requise)
- Commande "à la livraison" (nom, téléphone, adresse) → confirmation
- Formulaire de contact
- Interface d'administration en français pour gérer produits, catégories, commandes et messages

## Démarrage rapide

```bash
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Le site : http://127.0.0.1:8000/
L'administration : http://127.0.0.1:8000/admin/

## Ajouter des produits
1. Aller sur `/admin/`
2. Créer des **Catégories** (Abayas, Hijabs, Robes, etc.)
3. Créer des **Produits** : nom, catégorie, prix, image, stock, disponibilité
4. Cocher "Coup de cœur" pour mettre un produit en avant sur l'accueil

## Personnaliser les coordonnées
Modifier `config/settings.py` :
```python
SITE_ADDRESS = "Médina Gounass, Matam / Sénégal — chez la maison des Chérifs"
SITE_PHONE = "..."
SITE_EMAIL = "..."
```

## Compte administrateur créé pour la démo
- Utilisateur : `admin`
- Mot de passe : `Habiballah2026!`
⚠️ À changer immédiatement après le premier déploiement.

## Avant la mise en production
- Changer `SECRET_KEY` et mettre `DEBUG = False` dans `config/settings.py`
- Définir `ALLOWED_HOSTS`
- Configurer l'envoi d'e-mails (notifications de commande) si souhaité
- Brancher un vrai moyen de paiement (Wave, Orange Money, etc.) si besoin, sinon la commande reste en "paiement à la livraison"
