# Generated by Django 4.2.1 on 2023-08-14 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house_project', '0005_house_is_rented'),
    ]

    operations = [
        migrations.CreateModel(
            name='House_guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_project.house')),
            ],
        ),
    ]
