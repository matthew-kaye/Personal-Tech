from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Vendor(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=8192, blank=True)
    url = models.CharField(max_length=512, blank=True, null=True,)
    img_url = models.CharField(max_length=1024, blank=True, null=True,)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class HighScore(models.Model):
    name = models.CharField(max_length=64)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {str(self.score)}"

    class Meta:
        ordering = ("-score",)
