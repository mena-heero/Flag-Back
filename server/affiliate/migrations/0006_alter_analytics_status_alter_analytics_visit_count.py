# Generated by Django 4.1.3 on 2023-08-06 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0005_alter_creative_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analytics',
            name='status',
            field=models.IntegerField(choices=[(0, 'Default'), (1, 'Answer'), (2, 'No Answer'), (3, 'Interested'), (4, 'Not Interested'), (5, 'Wrong Number')], default=0, verbose_name='User status'),
        ),
        migrations.AlterField(
            model_name='analytics',
            name='visit_count',
            field=models.IntegerField(default=0, verbose_name='Visit Count'),
        ),
    ]
