# Generated by Django 4.2.7 on 2024-01-04 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_material_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_images/default.jpg', upload_to='product_images/'),
        ),
    ]
