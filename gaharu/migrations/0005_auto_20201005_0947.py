# Generated by Django 3.1.1 on 2020-10-05 02:47

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('gaharu', '0004_auto_20200908_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('filename', models.FileField(upload_to='models')),
                ('datalatih_ids', models.TextField(blank=True, null=True)),
                ('datauji_ids', models.TextField(blank=True, null=True)),
                ('accuracy', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelManagers(
            name='dataset',
            managers=[
                ('pdobjects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='dataset',
            name='kelas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]