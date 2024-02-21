from django.db import models

class Price(models.Model):
    lesson_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.lesson_price)

    class Meta:
        verbose_name = 'Lesson Price'
        verbose_name_plural = 'Lesson Price'
