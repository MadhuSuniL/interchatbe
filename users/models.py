import random
from django.contrib.auth.models import User
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile


class Profile(models.Model):
    user = models.OneToOneField(User, related_name = 'profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    bio = models.TextField(max_length=500, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True)

    def __str__(self):
        return self.name or self.user.username

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.username  # Set name to username if not provided
        
        if not self.profile_pic:
            self.generate_default_profile_pic()
        
        super().save(*args, **kwargs)


    def generate_default_profile_pic(self):
        # Define image size
        width, height = 200, 200

        # Generate a random background color
        background_color = (
            random.randint(0, 255),  # Red
            random.randint(0, 255),  # Green
            random.randint(0, 255)   # Blue
        )

        # Create a blank image with the background color
        image = Image.new('RGB', (width, height), color=background_color)
        draw = ImageDraw.Draw(image)

        # Define font and size
        font_size = 100  # Increased font size
        font = ImageFont.truetype("arial.ttf", font_size)

        # Calculate the size and position of the single letter
        text = self.user.username[0].upper()  # Take the first letter of the username
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)

        # Add the username text to the image
        text_color = (255, 255, 255)  # White
        draw.text(position, text, fill=text_color, font=font)

        # Save the image to a BytesIO object
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        # Save the image to the profile_pic field
        file_name = f'{self.user.username}_default.png'
        self.profile_pic.save(file_name, ContentFile(buffer.read()), save=False)
