# Generated by Django 4.1.3 on 2023-02-28 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('-creation_time',)},
        ),
    ]
