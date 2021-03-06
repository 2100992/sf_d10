# Generated by Django 3.0.3 on 2020-02-06 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Производитель')),
                ('slug', models.SlugField(default='_', max_length=150, unique=True)),
                ('descriptions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Модель')),
                ('slug', models.SlugField(default='_', max_length=150, unique=True)),
                ('descriptions', models.TextField(blank=True, null=True)),
                ('start_production', models.SmallIntegerField(blank=True, null=True)),
                ('end_producrion', models.SmallIntegerField(blank=True, null=True)),
                ('car_maker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='car_models', to='app.CarMaker')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('year', models.SmallIntegerField(verbose_name='Год выпуска')),
                ('gearbox', models.SmallIntegerField(choices=[(0, 'отсутствует'), (1, 'механика'), (2, 'автомат'), (3, 'робот')], verbose_name='КПП')),
                ('descriptions', models.TextField()),
                ('car_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cars', to='app.CarModel')),
            ],
        ),
    ]
