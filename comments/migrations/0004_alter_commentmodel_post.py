# Generated by Django 3.2.7 on 2022-03-25 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_delete_basemodel'),
        ('comments', '0003_commentmodel_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.postmodel'),
        ),
    ]
