# Generated by Django 2.0.6 on 2018-06-14 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='categories',
            field=models.ManyToManyField(related_name='publications', to='publications.Category'),
        ),
    ]
