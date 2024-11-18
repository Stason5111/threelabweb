# Generated by Django 4.2.7 on 2023-11-18 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_gender_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(blank=True, help_text='Вставьте изображение бренда', null=True, upload_to='brands/'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(help_text='Введите имя бренда', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(blank=True, help_text='Выберите бренд', null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.manufacturer'),
        ),
    ]
