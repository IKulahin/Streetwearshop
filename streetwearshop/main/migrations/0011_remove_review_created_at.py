# Generated by Django 4.2.7 on 2024-01-09 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
    ]