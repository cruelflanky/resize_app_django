from django.db import models

# Create your models here.
class Image(models.Model):

	name = models.CharField(verbose_name = 'Название', max_length=100)
	picture = models.ImageField()

	class Meta:
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'

	def __str__(self):
		return self.name