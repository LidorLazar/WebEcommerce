# Generated by Django 4.1.5 on 2023-02-07 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='no-image.png', null=True, upload_to='static/images/'),
        ),
    ]
