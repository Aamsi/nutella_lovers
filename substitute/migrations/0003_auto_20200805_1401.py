# Generated by Django 3.0.8 on 2020-08-05 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0002_auto_20200803_1119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='nutri_score',
            new_name='nutriscore',
        ),
    ]
