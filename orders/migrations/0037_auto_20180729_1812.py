# Generated by Django 2.0.7 on 2018-07-29 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_auto_20180729_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extra',
            name='category',
        ),
        migrations.AddField(
            model_name='extra',
            name='category',
            field=models.ManyToManyField(to='orders.Category'),
        ),
    ]
