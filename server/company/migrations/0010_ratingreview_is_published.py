# Generated by Django 4.1.3 on 2023-04-07 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingreview',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Is published?'),
        ),
    ]
