# Generated by Django 3.0.8 on 2020-10-11 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0008_auto_20200825_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='thumbnail',
            field=models.TextField(null=True),
        ),
    ]