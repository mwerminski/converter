import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Mp3
from ..serializers import FileSerializer, Mp3InfoSerializer, CoverImageSerializer, Mp3ResponseFileSerializer, FileResponseSerializer, ShortMp3InfoSerliazer


client = Client()

def 