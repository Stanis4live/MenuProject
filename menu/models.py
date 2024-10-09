from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='название')

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='название')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='родитель')
    url = models.CharField(max_length=200, blank=True, verbose_name='ссылка')
    named_url = models.CharField(max_length=200, blank=True, verbose_name='ссылка по имени')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='меню', related_name='items')

    class Meta:
        verbose_name = 'пункт меню'
        verbose_name_plural = 'пункты меню'

    def get_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        return self.name
