# Generated by Django 2.0.7 on 2018-07-26 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20180726_1934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['category', 'name']},
        ),
    ]
