# Generated by Django 4.1.5 on 2023-02-15 20:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='create_order',
            new_name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='name',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='zip_code',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='base.product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
