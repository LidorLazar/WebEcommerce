# Generated by Django 4.1.5 on 2023-02-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='no-image.png', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='reviwe',
            name='text_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
