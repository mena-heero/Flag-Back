# Generated by Django 4.1.3 on 2023-03-28 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0018_remove_mainmenuitem_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmediasettings',
            name='tiktok',
            field=models.URLField(blank=True, help_text='Tiktok URL', max_length=255, null=True),
        ),
    ]
