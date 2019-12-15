from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from mp3converter import urls
from converter.models import Mp3
from converter.serializers import FileSerializer, Mp3InfoSerializer, CoverImageSerializer, Mp3ResponseFileSerializer, FileResponseSerializer, ShortMp3InfoSerliazer
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadhandler import MemoryFileUploadHandler
import io


class ModelTestCase(APITestCase):

    def setUp(self):
        Mp3.objects.create(
            file_name = "example",
            file_type = "wav",
            title = "bad bad",
            artist = "ble ble",
            album = "ble bad ble",
            year = "1410",
            comment = "bleeeeeeeeeeeeeee",
            track =  "1",
            genre = "rap"
        )

    def test_values(self):
        converted_file = Mp3.objects.get(id=1)
        f_name = converted_file._meta.get_field('file_name').verbose_name
        self.assertEquals(f_name, "file name")
        f_type = converted_file._meta.get_field('file_type').verbose_name
        self.assertEquals(f_type, "file type")
        title = converted_file._meta.get_field('title').verbose_name
        self.assertEquals(title, "title")
        artist = converted_file._meta.get_field('artist').verbose_name
        self.assertEquals(artist, "artist")
        album = converted_file._meta.get_field('album').verbose_name
        self.assertEquals(album, "album")
        year = converted_file._meta.get_field('year').verbose_name
        self.assertEquals(year, "year")
        comment = converted_file._meta.get_field('comment').verbose_name
        self.assertEquals(comment, "comment")
        track = converted_file._meta.get_field('track').verbose_name
        self.assertEquals(track, "track")
        genre = converted_file._meta.get_field('genre').verbose_name
        self.assertEquals(genre, "genre")





# class ConvertedFileTestCase(APITestCase):




# class ConverterTestCase(APITestCase):


# class AuthenticationTestCase(APITestCase):

class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('example', 'example@example.com')
        self.token = Token.objects.create(user=self.user)

        self.mp3_file_invalid = SimpleUploadedFile('./converter/test_files/wav_example.wav', b'file_content')
        self.mp3_data_invalid = { 'file_name' : 'ble',
                          'file_type' : 'wav',
                          'data_file' : self.mp3_file_invalid}

        self.mp3_file = io.open('./converter/test_files/wav_example.wav', 'rb')
        self.mp3_data = { 'file_name' : 'ble',
                          'file_type' : 'wav',
                          'data_file' : self.mp3_file}
    
    def tearDown(self):
        self.mp3_file_invalid.close()
        
        # self.create_response = self.client.post(
        #     reverse('create'),
        #     self.mp3_data,
        #     format="json")

    def test_authorization(self):
        request = self.client.get('/file')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        # force_authenticate(request, user=self.user, token = self.user.auth_token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        request = self.client.get('/file')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        request = self.client.post('/converter/', self.mp3_data_invalid)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        print(self.mp3_data)
        request = self.client.post('/converter/', data = self.mp3_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.content, b'{"id":"1"}')


