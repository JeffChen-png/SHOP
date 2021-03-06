# Generated by Django 3.1.7 on 2021-05-24 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='brand/%Y/%m/%d')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='category/%Y/%m/%d')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_tag', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Хэш-тег',
                'verbose_name_plural': 'Хэш-теги',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='type/%Y/%m/%d')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='product/%Y/%m/%d')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, db_index=True)),
                ('composition', models.CharField(blank=True, db_index=True, max_length=200)),
                ('stock', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('slug', models.SlugField(max_length=200)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SHOP.brand')),
                ('category', models.ManyToManyField(to='SHOP.Category')),
                ('hash_tag', models.ManyToManyField(blank=True, db_index=True, null=True, related_name='tags', to='SHOP.HashTag')),
                ('type', models.ManyToManyField(to='SHOP.Type')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ('name', 'created', 'updated', 'stock', 'price'),
                'index_together': {('id', 'slug')},
            },
        ),
    ]
