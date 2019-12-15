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
            track =  1,
            genre = 2
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


class ViewTestCase(APITestCase):

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

        self.cover_image = io.open('./converter/test_files/smile.jpg', 'rb')
        self.cover_image_2 = io.open('./converter/test_files/blee.png', 'rb')
    
    def tearDown(self):
        self.mp3_file_invalid.close()
        self.mp3_file.close()
        self.cover_image.close()
        self.cover_image_2.close()

    def test_authorization(self):
        request = self.client.get('/file')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        # force_authenticate(request, user=self.user, token = self.user.auth_token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        request = self.client.get('/file')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_convert_procedure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        request = self.client.post('/converter', self.mp3_data_invalid) #fail
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.client.post('/converter', data = self.mp3_data) #create
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.content, b'{"id":"1"}')

        request = self.client.get('/file')  #list
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.content, b'[{"id":1,"file_name":"ble","file_type":"mp3","title":""}]')

        request = self.client.get('/file/1/info')  #list
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.content, b'{"file_name":"ble","file_type":"mp3","title":"","artist":"","album":"","year":"","comment":"","track":"","genre":""}')

        info_data = {"title":"bo bo","artist":"bb","album":"ble album","year":"1410","comment":"nope","track":1,"genre":1}
        request = self.client.put('/file/1/info', data = info_data)  #update fields
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

        request = self.client.get('/file/1/info')  #get 1 file info
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.content, b'{"file_name":"ble","file_type":"mp3","title":"bo bo","artist":"bb","album":"ble album","year":"1410","comment":"nope","track":"1","genre":"1"}')

        cover_data = {"cover" : self.cover_image}
        request = self.client.put('/file/1/cover', data = cover_data)  #update cover image
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

        request = self.client.get('/converter/1', ) #get file
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.content[0:41], b'{"data_file":"http://testserver/music/ble')

        cover_data = {"cover" : self.cover_image_2}
        request = self.client.put('/file/1/cover', data = cover_data)  #update cover image
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

        request = self.client.get('/converter/1', ) #get file
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.content[0:41], b'{"data_file":"http://testserver/music/ble')

        request = self.client.delete('/converter/1', ) #delete file
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

        request = self.client.delete('/converter/1', ) #delete file - failed
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(request.content, b'{"detail":"Not found."}')

        request = self.client.get('/converter/1', ) #get file - failed
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(request.content, b'{"detail":"Not found."}')

        request = self.client.get('/file/1/info')  #get 1 file info - failed
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(request.content, b'{"detail":"Not found."}')

class UserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('example_2', 'example@example.com')
        self.token = Token.objects.create(user=self.user)

        self.client_2 = APIClient()
        self.user_2 = User.objects.create_user('example_3', 'example@example.com')
        self.token_2 = Token.objects.create(user=self.user_2)

        self.mp3_file = io.open('./converter/test_files/sample.ogg', 'rb')
        self.mp3_file2 = io.open('./converter/test_files/sample.aac', 'rb')
        self.mp3_file3= io.open('./converter/test_files/sample.wav', 'rb')
        self.mp3_data = { 'file_name' : 'ble',
                          'file_type' : 'ogg',
                          'data_file' : self.mp3_file}

        self.mp3_data_2 = { 'file_name' : 'ble2',
                          'file_type' : 'aac',
                          'data_file' : self.mp3_file2}

        self.mp3_data_3 = { 'file_name' : 'ble3',
                          'file_type' : 'wav',
                          'data_file' : self.mp3_file3}

        self.cover_image = io.open('./converter/test_files/smile.jpg', 'rb')
        self.cover_image_2 = io.open('./converter/test_files/blee.png', 'rb')

    def tearDown(self):
        self.mp3_file.close()
        self.cover_image.close()
        self.cover_image_2.close()

    def test_access_to_forbidden_files(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client_2.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)

        request = self.client.post('/converter', data = self.mp3_data) #create
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.content, b'{"id":"1"}')

        request = self.client.post('/converter', data = self.mp3_data_2) #create
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.content, b'{"id":"2"}')

        request = self.client_2.post('/converter', data = self.mp3_data_3) #create
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.content, b'{"id":"3"}')

        request = self.client_2.get('/file/1/info')  #get 1 file info
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

        request = self.client_2.get('/converter/1', ) #get file - failed
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(request.content, b'{"detail":"Not found."}')

