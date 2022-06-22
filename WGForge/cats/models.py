from django.db import models


class CatColorsInfo(models.Model):
    color = models.TextField(unique=True, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cat_colors_info"


class Cats(models.Model):
    name = models.CharField(primary_key=True, max_length=-1)
    color = models.TextField(blank=True, null=True)
    tail_length = models.IntegerField(blank=True, null=True)
    whiskers_length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cats"


class CatsStat(models.Model):
    tail_length_mean = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True
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