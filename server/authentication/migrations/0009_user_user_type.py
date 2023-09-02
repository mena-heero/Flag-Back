# Generated by Django 4.1.3 on 2023-08-05 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_user_social_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(0, 'User'), (1, 'Affiliate')], default=0, verbose_name='Auth type'),
        ),
    ]
