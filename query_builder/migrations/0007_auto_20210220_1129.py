# Generated by Django 3.1.5 on 2021-02-20 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query_builder', '0006_searchsetting_setting_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchsetting',
            old_name='setting_type',
            new_name='group',
        ),
    ]