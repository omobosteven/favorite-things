# Generated by Django 2.2.2 on 2019-06-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190621_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritething',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
