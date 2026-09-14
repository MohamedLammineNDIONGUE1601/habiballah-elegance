import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from boutique.models import Categorie, Produit, ImageProduit
from pathlib import Path


class Command(BaseCommand):
    help = "Import product images and videos from media folder"

    def handle(self, *args, **options):
        media_folder = Path("media/produits")
        
        # Ensure Robes category exists
        categorie, _ = Categorie.objects.get_or_create(
            nom="Robes",
            defaults={
                "description": "Des robes modestes et raffinées, aux coupes intemporelles.",
                "ordre": 1
            }
        )
        
        self.stdout.write(f"✓ Catégorie: {categorie.nom}")
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png'}
        video_extensions = {'.mp4', '.avi', '.mov'}
        
        image_files = sorted([
            f for f in os.listdir(media_folder)
            if os.path.isfile(media_folder / f) and Path(f).suffix.lower() in image_extensions
        ])
        
        video_files = sorted([
            f for f in os.listdir(media_folder)
            if os.path.isfile(media_folder / f) and Path(f).suffix.lower() in video_extensions
        ])
        
        # Create products from images
        product_count = 0
        for idx, image_file in enumerate(image_files, 1):
            # Skip placeholder images
            if any(placeholder in image_file for placeholder in ['Abaya', 'Robe_', 'Hijab', 'Ceinture', 'Pochette']):
                continue
            
            nom_produit = f"Robe Élégance Tendance {idx}"
            
            # Check if product already exists
            if Produit.objects.filter(nom=nom_produit).exists():
                continue
            
            produit = Produit(
                nom=nom_produit,
                categorie=categorie,
                description=f"{nom_produit} — Une création exclusive Habiballah Élégance.",
                matiere="Tissu premium",
                prix=45000,
                stock=5,
                disponible=True,
                coup_de_coeur=idx <= 2,  # Mark first 2 as featured
            )
            
            # Set image from media folder
            image_path = media_folder / image_file
            with open(image_path, 'rb') as f:
                produit.image_principale.save(
                    image_file,
                    ContentFile(f.read()),
                    save=False
                )
            
            produit.save()
            product_count += 1
            self.stdout.write(f"  ✓ Produit créé: {nom_produit} (Image: {image_file})")
        
        # Add videos as gallery images
        video_count = 0
        for produit in Produit.objects.filter(categorie=categorie).order_by('date_ajout')[:len(image_files)]:
            for video_idx, video_file in enumerate(video_files):
                video_path = media_folder / video_file
                
                # Check if this video reference already exists
                if ImageProduit.objects.filter(produit=produit, image=f"produits/{video_file}").exists():
                    continue
                
                try:
                    with open(video_path, 'rb') as f:
                        image_produit = ImageProduit(
                            produit=produit,
                            ordre=video_idx + 1
                        )
                        image_produit.image.save(
                            video_file,
                            ContentFile(f.read()),
                            save=True
                        )
                        video_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠ Erreur vidéo {video_file}: {str(e)}")
                    )
                
                if video_idx >= 2:  # Limit to 3 videos per product
                    break
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Import terminé!"
                f"\n  • {product_count} produits créés"
                f"\n  • {video_count} vidéos ajoutées"
            )
        )
