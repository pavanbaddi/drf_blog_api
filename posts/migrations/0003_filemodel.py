# Generated by Django 3.2.7 on 2022-03-21 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_postmodel_featured_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=255)),
                ('type_id', models.IntegerField()),
                ('path', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'files',
            },
        ),
    ]
