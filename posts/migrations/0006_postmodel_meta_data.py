# Generated by Django 3.2.7 on 2022-03-27 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_delete_basemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='meta_data',
            field=models.JSONField(null=True),
        ),
    ]
