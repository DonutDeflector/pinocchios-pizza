# Generated by Django 2.0.7 on 2018-07-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20180726_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='size', to='orders.Size'),
        ),
    ]
