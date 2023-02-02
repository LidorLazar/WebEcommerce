# Generated by Django 4.1.5 on 2023-01-18 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, null=True)),
                ('brand', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('rating', models.DecimalField(decimal_places=2, max_digits=7)),
                ('num_reviews', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('count_in_stock', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
