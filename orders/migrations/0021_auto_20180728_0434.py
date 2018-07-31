# Generated by Django 2.0.7 on 2018-07-28 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_category_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.AddField(
            model_name='item',
            name='sizes',
            field=models.ManyToManyField(related_name='size', to='orders.Size'),
        ),
        migrations.AlterField(
            model_name='category',
            name='items',
            field=models.ManyToManyField(null=True, related_name='item', to='orders.Item'),
        ),
    ]
