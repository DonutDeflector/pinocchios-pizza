# Generated by Django 2.0.7 on 2018-07-29 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0039_remove_extra_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='categories',
            field=models.ManyToManyField(to='orders.Category'),
        ),
    ]
