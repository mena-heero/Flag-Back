# Generated by Django 4.1.3 on 2023-03-03 00:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0006_ratingreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingreview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
