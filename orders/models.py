from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Size(models.Model):
    name = models.CharField(max_length=32)
    price = models.PositiveIntegerField

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category", null=True)
    size = models.ForeignKey(Size, related_name="size",
                             on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name}"


class Topping(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class AddOn(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
