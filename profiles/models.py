from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    pass


class BinanceKey(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=64)
    api_secret = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s' % self.name


class TelegramBotSettings(models.Model):
    name = models.CharField(max_length=64)
    token = models.CharField(max_length=64)
    chat = models.ManyToManyField('TelegramChatIds', blank=True)
    proxy = models.CharField(max_length=25, blank=True, null=True)
    def __str__(self):
        return '%s' % self.name


class TelegramChatIds(models.Model):
    name = models.CharField(max_length=128)
    chat_id = models.CharField(max_length=32)
    def __str__(self):
        return '%s' % self.name