from pydub import AudioSegment
from io import StringIO, BytesIO
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

def convert_to_mp3(request_data):
    if(request_data['file_type'] != "mp3"):
        request_data['file_type'] = "mp3"
        mp3_data = request_data['data_file']
        sound = AudioSegment.from_file(mp3_data.file)
        print(request_data)
        buf = BytesIO()
        request_data['data_file'].file = sound.export(buf ,format="mp3")
        request_data['data_file'].name = request_data['file_name']+".mp3"

def add_info(instance, data):
    tag = EasyID3(data.seq_file)
    tag['title'] = instance['title']
    tag['artist'] = instance['artist']
    tag['album'] = instance['album']
    tag['date'] = instance['year']
    tag['comment'] = instance['comment']
    tag['tracknumber'] = instance['track']
    tag['genre'] = instance['genre']
    tag.save()
    data.save()


def add_cover(instance, data):
    tag = ID3(data)
    tag['APIC'] = APIC(data=instance['cover'].file)
    tag.save()
    data.save()
