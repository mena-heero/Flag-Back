# Generated by Django 4.1.3 on 2023-02-27 12:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wagtailcore', '0078_referenceindex'),
        ('home', '0005_alter_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('hero_title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Hero title')),
                ('hero_description', wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Hero description')),
                ('list_title', models.CharField(blank=True, max_length=250, null=True, verbose_name='List title')),
                ('og_keywords', models.CharField(blank=True, max_length=550, null=True, verbose_name='Og keywords')),
                ('og_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
