# Generated by Django 4.2.1 on 2023-08-16 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house_project', '0007_house_guest_alter_house_house_host_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rented_houses', to=settings.AUTH_USER_MODEL),
        ),
    ]
