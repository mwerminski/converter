from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

class Mp3(models.Model):
    owner = models.CharField(max_length=200)
    file_name = models.TextField(null=True)
    file_type = models.TextField(null=True)
    data_file = models.FileField(null=True, blank=False)
    #mp3 tag
    header = models.CharField(max_length=3)
    title = models.CharField(max_length=30)
    artist = models.CharField(max_length=30)
    album = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    comment = models.CharField(max_length=28)
    zero_byte = models.CharField(max_length=1)
    track = models.CharField(max_length=1)
    genre = models.CharField(max_length=1)
    #image cover
    cover = models.ImageField()
