# Generated by Django 2.2 on 2021-06-13 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pluma', '0006_rutasindv'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_shp', models.FileField(upload_to='corridas/')),
                ('archivo_sdbf', models.FileField(upload_to='corridas/')),
                ('archivo_shx', models.FileField(upload_to='corridas/')),
                ('archivo_prj', models.FileField(upload_to='corridas/')),
                ('archivo_cpg', models.FileField(upload_to='corridas/')),
            ],
        ),
    ]
