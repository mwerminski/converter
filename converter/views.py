
from django.shortcuts import render
from django.http import QueryDict
from django.http import HttpResponse
from rest_framework import viewsets, mixins, status
from converter.models import Mp3
from converter.serializers import FileSerializer, Mp3InfoSerializer, CoverImageSerializer, Mp3ResponseFileSerializer, FileResponseSerializer, ShortMp3InfoSerliazer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser
from converter.permissions import IsOwner
from converter.convert_music import convert_to_mp3, add_info, add_cover
from pydub.exceptions import PydubException
import os

class ConvertedFileViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = Mp3.objects.all()
    permission_classes = (IsOwner,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'put', 'delete']

    def list(self, request, *args, **kwargs): #Done
        '''Get list of converted files '''
        self.serializer_class = ShortMp3InfoSerliazer
        response = super().list(request, *args, **kwargs)
        if(response.data):
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):  #Done
        '''Update info about selected file'''
        self.serializer_class = Mp3InfoSerializer
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs): #Done
        '''Get tag info about selected file'''
        self.serializer_class = Mp3InfoSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return Mp3.objects.all()
        return Mp3.objects.filter(owner=user)


class FileInfoViewSet(mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsOwner,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'post', 'delete']
    '''file conversion handler'''

    def create(self, request, *args, **kwargs): #Done
        '''Upload file and convert to .mp3 format'''

        try:
            convert_to_mp3(request.data)
        except PydubException as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
          obj = file_serializer.save(owner=self.request.user)
          return Response({ "id" : str(obj.id)}, status=status.HTTP_201_CREATED)
        else:
          return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs): #Done
        '''Get selected .mp3 file'''
        self.serializer_class = Mp3ResponseFileSerializer
        instance = self.get_object()
        data_file = self.get_serializer(instance)

        path = "."+data_file.get_path(instance)
        add_info(Mp3InfoSerializer(instance), path)
        image_path = None

        if CoverImageSerializer(instance)['cover'].value:
            image_path = "."+CoverImageSerializer().get_path(instance)
        add_cover(CoverImageSerializer(instance), path, image_path)

        return Response(data_file.data)
    
    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return Mp3.objects.all()
        return Mp3.objects.filter(owner=user)

class CoverImageViewSet(mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = CoverImageSerializer
    permission_classes = (IsOwner,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['put', 'delete']
    '''Cover image handler'''

    def update(self, request, *args, **kwargs): #Done
        '''add / change image cover'''
        serializer_class = CoverImageSerializer
        kwargs['partial'] = True

        instance = self.get_object()
        if CoverImageSerializer(instance)['cover'].value:
            image_path = "."+CoverImageSerializer().get_path(instance)
            if os.path.exists(image_path):
               os.remove(image_path)
            

        response = super().update(request, *args, **kwargs)
        if(response.status_code == 200):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return response

    def destroy(self, request, *args, **kwargs): #Done
        '''Remove image cover'''
        kwargs['partial'] = True
        instance = self.get_object()
        instance.cover.delete(save=True)
        response = super().update(request, *args, **kwargs)
        if(response.status_code == 200):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return response

    
    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            return Mp3.objects.all()
        return Mp3.objects.filter(owner=user)

   