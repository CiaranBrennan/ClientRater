# Generated by Django 2.2.7 on 2020-03-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0004_auto_20200305_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(verbose_name='Rating'),
        ),
    ]