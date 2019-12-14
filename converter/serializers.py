from converter.models import Mp3
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mp3
        fields = ['file_name', 'file_type', 'data_file']

        extra_kwargs = {
            'owner': { 'read_only': True }
        }

class Mp3InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mp3
        fields = ['file_name', 'file_type','file_type',
        'header','title','artist','album','year','comment','zero_byte',
        'track','genre']

class ShortMp3InfoSerliazer(serializers.ModelSerializer):
    class Meta:
        model = Mp3
        fields = ['id', 'file_name', 'file_type', 'title']

class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mp3
        fields = ['cover']
    
    def get_path(self, instance):
        return instance.cover.url

class Mp3ResponseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mp3
        fields = ['data_file']

    def get_path(self, instance):
        return instance.data_file.url

class FileResponseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Mp3
        fields = ['id','file_name','file_type']