# Generated by Django 4.2.7 on 2023-11-18 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='gender',
            name='slug',
            field=models.SlugField(default='18.11.2023', help_text='Сокращение для ссылки', max_length=150),
            preserve_default=False,
        ),
    ]
