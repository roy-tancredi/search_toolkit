# Generated by Django 3.1.5 on 2021-02-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query_builder', '0005_auto_20210204_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchsetting',
            name='setting_type',
            field=models.CharField(blank=True, max_length=64, verbose_name='typology of search settings'),
        ),
    ]
