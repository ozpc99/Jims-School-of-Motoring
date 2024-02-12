from django.db import models

class Price(models.Model):
    lesson_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Lesson Price: {self.lesson_price}"

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    class Meta:
        verbose_name = 'Lesson Price'
        verbose_name_plural = 'Lesson Price'