# Generated by Django 2.0.7 on 2018-07-28 06:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_auto_20180728_0600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='sizes',
        ),
        migrations.AddField(
            model_name='price',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Item'),
        ),
        migrations.AddField(
            model_name='price',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='size', to='orders.Size'),
        ),
    ]
