# Generated by Django 4.1.3 on 2023-03-02 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_articledetailpage_body_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0005_alter_company_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'News'), (1, 'Articles'), (2, 'Company')], default=0, verbose_name='Rating on')),
                ('rating', models.FloatField(default=1, verbose_name='Rating')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('articles', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='home.articledetailpage', verbose_name='Articles')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='company.company', verbose_name='Company')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='home.newsdetailpage', verbose_name='News')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('-creation_time',),
            },
        ),
    ]
