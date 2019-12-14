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
    header = models.CharField(max_length=3, blank = True)
    title = models.CharField(max_length=30, blank = True)
    artist = models.CharField(max_length=30, blank = True)
    album = models.CharField(max_length=30, blank = True)
    year = models.CharField(max_length=4, blank = True)
    comment = models.CharField(max_length=28, blank = True)
    zero_byte = models.CharField(max_length=1, blank = True)
    track = models.CharField(max_length=1, blank = True)
    genre = models.CharField(max_length=1, blank = True)
    #image cover
    cover = models.ImageField(blank = True)
