# Generated by Django 4.1.3 on 2023-06-03 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0048_contactuspage_hero_subtitle_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articledetailpage',
            name='title_en',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='companydetail',
            name='recommendation_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Recommendation text en'),
        ),
        migrations.AddField(
            model_name='companydetail',
            name='short_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Short description en'),
        ),
        migrations.AddField(
            model_name='companydetail',
            name='title_en',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='companyfinderrating',
            name='title_en',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
