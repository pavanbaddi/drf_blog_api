# Generated by Django 3.2.7 on 2022-03-25 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_remove_commentmodel_basemodel_ptr'),
        ('posts', '0004_basemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BaseModel',
        ),
    ]
