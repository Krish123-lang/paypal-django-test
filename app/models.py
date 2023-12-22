from django.db import models

# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="images")

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title
