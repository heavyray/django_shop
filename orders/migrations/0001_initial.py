# Generated by Django 4.0 on 2022-06-16 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=250, verbose_name='адрес')),
                ('postal_code', models.CharField(max_length=20, verbose_name='почтовый индекс')),
                ('city', models.CharField(max_length=100, verbose_name='город')),
                ('created', models.DateField(auto_now_add=True, verbose_name='создан')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='заказ')),
            ],
            options={
                'verbose_name': 'заказанный товар',
                'verbose_name_plural': 'заказанные товары',
            },
        ),
    ]
