# Generated by Django 4.1.3 on 2023-01-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_product_image2_product_image3_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='no-image.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(default='no-image.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(default='no-image.png', upload_to=''),
        ),
    ]
