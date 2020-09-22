# Generated by Django 3.1.1 on 2020-09-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('is_extracted', models.CharField(max_length=1)),
                ('form_factor', models.FloatField()),
                ('aspect_ratio', models.FloatField()),
                ('rect', models.FloatField()),
                ('narrow_factor', models.FloatField()),
                ('prd', models.FloatField()),
                ('plw', models.FloatField()),
                ('idm', models.FloatField()),
                ('entropy', models.FloatField()),
                ('asm', models.FloatField()),
                ('contrast', models.FloatField()),
                ('correlation', models.FloatField()),
            ],
        ),
    ]
