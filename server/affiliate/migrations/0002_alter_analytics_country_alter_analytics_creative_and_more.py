# Generated by Django 4.1.3 on 2023-07-31 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utility', '0024_globalsetting_address_en'),
        ('affiliate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analytics',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytics', to='utility.country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='analytics',
            name='creative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytics', to='affiliate.creative', verbose_name='Creative'),
        ),
        migrations.AlterField(
            model_name='analytics',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vat_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='100')),
                ('account_beneficiary', models.CharField(blank=True, max_length=150, null=True, verbose_name='Account beneficiary')),
                ('account_number', models.CharField(max_length=50, verbose_name='Account number')),
                ('bank_name', models.CharField(max_length=100, verbose_name='Bank name')),
                ('bank_branch', models.CharField(max_length=100, verbose_name='Bank branch')),
                ('bank_city', models.CharField(max_length=100, verbose_name='Bank city')),
                ('swift_code', models.CharField(max_length=50, verbose_name='Swift code')),
                ('iban_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='IBAN Number')),
                ('bank_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.country', verbose_name='Country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_detail', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Credit'), (1, 'Debit')], default=0, verbose_name='Balance type')),
                ('amount', models.FloatField(default=0, verbose_name='Amount')),
                ('analytics', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliate.analytics', verbose_name='Analytics')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
