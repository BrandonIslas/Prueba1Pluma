# Generated by Django 2.2 on 2021-06-15 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pluma', '0007_archivos'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrigenDestino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=10)),
                ('destino', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='archivos',
            name='archivo_cpg',
            field=models.FileField(blank=True, null=True, upload_to='corridas'),
        ),
        migrations.AlterField(
            model_name='archivos',
            name='archivo_prj',
            field=models.FileField(blank=True, null=True, upload_to='corridas'),
        ),
        migrations.AlterField(
            model_name='archivos',
            name='archivo_sdbf',
            field=models.FileField(blank=True, null=True, upload_to='corridas'),
        ),
        migrations.AlterField(
            model_name='archivos',
            name='archivo_shp',
            field=models.FileField(blank=True, null=True, upload_to='corridas'),
        ),
        migrations.AlterField(
            model_name='archivos',
            name='archivo_shx',
            field=models.FileField(blank=True, null=True, upload_to='corridas'),
        ),
    ]
