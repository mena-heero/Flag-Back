# Generated by Django 4.1.3 on 2023-03-23 08:51

import company.models
import company.serializers
from django.db import migrations
import home.blocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_companydetail_recommendation_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('broker_survey_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250)), ('subtitle', wagtail.blocks.CharBlock(max_length=250)), ('image', home.blocks.ImageChooserBlock(rendition_rules={'original': 'original|jpegquality-60|format-webp'})), ('learn_more_button_text', wagtail.blocks.CharBlock(max_length=250)), ('learn_more_button_link', wagtail.blocks.CharBlock(max_length=250)), ('survey_button_text', wagtail.blocks.CharBlock(max_length=250)), ('survey_button_link', wagtail.blocks.CharBlock(max_length=250))])), ('companies', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250)), ('company', wagtail.blocks.ListBlock(home.blocks.CompanyListChooserBlock(page_type=['home.CompanyDetail'])))])), ('news', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250)), ('news', wagtail.blocks.ListBlock(home.blocks.NewsDetailPageChooserBlock(page_type=['home.NewsDetailPage'])))])), ('articles', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250)), ('articles', wagtail.blocks.ListBlock(home.blocks.ArticleDetailPageChooserBlock(page_type=['home.ArticleDetailPage'])))])), ('two_column_text_image_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250)), ('description', home.blocks.RichTextBlock()), ('link', wagtail.blocks.StructBlock([('link', wagtail.blocks.StreamBlock([('page', home.blocks.PageChooserBlock(max_num=1)), ('link', wagtail.blocks.URLBlock(max_num=1))])), ('label', wagtail.blocks.CharBlock())])), ('image', home.blocks.ImageChooserBlock(rendition_rules={'original': 'original|jpegquality-60|format-webp'}))])), ('currency_rate_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('tabs', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('stocks', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('stock', home.blocks.SnippetChooserBlock(serializer=company.serializers.StockSerializer, target_model=company.models.Stock))])))])))]))], blank=True, null=True, use_json_field=True),
        ),
    ]
