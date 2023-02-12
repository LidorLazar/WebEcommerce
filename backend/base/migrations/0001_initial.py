# Generated by Django 4.1.5 on 2023-02-10 10:56

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, default='no-image.png', null=True, upload_to='images/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('paid', models.BooleanField(default=False)),
                ('create_order', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=200, null=True)),
                ('image', models.ImageField(default='no-image.png', upload_to='')),
                ('image2', models.ImageField(default='no-image.png', upload_to='')),
                ('image3', models.ImageField(default='no-image.png', upload_to='')),
                ('brand', models.CharField(max_length=100)),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'Soccer shoes'), (2, 'Ball')])),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('count_in_stock', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviwe',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('text_comment', models.TextField(blank=True, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.product')),
            ],
        ),
    ]
