# Generated by Django 4.0 on 2022-06-16 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='статус')),
            ],
            options={
                'verbose_name': 'статусы',
                'verbose_name_plural': 'статусы',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0, verbose_name='баланс')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.status', verbose_name='статус')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d', verbose_name='фото товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('stock', models.PositiveIntegerField(verbose_name='остаток')),
                ('available', models.BooleanField(default=True, verbose_name='наличие')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='обновлено')),
                ('slug', models.SlugField(max_length=200)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.category')),
                ('in_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.shop', verbose_name='магазин')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ['id'],
                'index_together': {('id', 'slug')},
            },
        ),
    ]