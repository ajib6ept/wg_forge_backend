from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CatColorsInfo(models.Model):
    color = models.TextField(primary_key=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "cat_colors_info"


class Cats(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    color = models.TextField(blank=True, null=True)
    tail_length = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(100), MinValueValidator(1)],
    )
    whiskers_length = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(100), MinValueValidator(1)],
    )

    class Meta:
        managed = False
        db_table = "cats"


class CatsStat(models.Model):
    tail_length_mean = models.DecimalField(
        max_digits=65535, decimal_places=65535, primary_key=True
    )
    tail_length_median = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    tail_length_mode = models.TextField(blank=True, null=True)
    whiskers_length_mean = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    whiskers_length_median = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    whiskers_length_mode = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cats_stat"
