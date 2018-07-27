# Generated by Django 2.0.7 on 2018-07-26 19:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_pizza_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='orders.Category')),
                ('size', models.ManyToManyField(null=True, related_name='size', to='orders.Size')),
            ],
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='category',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='size',
        ),
        migrations.DeleteModel(
            name='Pizza',
        ),
    ]
