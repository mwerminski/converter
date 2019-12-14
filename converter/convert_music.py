from pydub import AudioSegment
from io import StringIO, BytesIO
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from PIL import Image

def convert_to_mp3(request_data):
    if(request_data['file_type'] != "mp3"):
        request_data['file_type'] = "mp3"
        mp3_data = request_data['data_file']
        sound = AudioSegment.from_file(mp3_data.file)
        print(request_data)
        buf = BytesIO()
        request_data['data_file'].file = sound.export(buf ,format="mp3")
        request_data['data_file'].name = request_data['file_name']+".mp3"

def add_info(instance, file_path):
    tag = None
    EasyID3.RegisterTextKey('comment', 'COMM')
    try:
        tag = EasyID3(file_path)
    except:
        tag = mutagen.File(file_path, easy=True)
        tag.add_tags()

    tag.delete()
    tag.save()
    
    tag['title'] = check_text(instance['title'])
    tag['artist'] = check_text(instance['artist'])
    tag['album'] = check_text(instance['album'])
    tag['date'] = check_text(instance['year'])
    tag['comment'] = check_text(instance['comment'])
    tag['tracknumber'] = check_text(instance['track'])
    tag['genre'] = check_text(instance['genre'])
    tag.save(v2_version=3)

def add_cover(instance, file_path, image_path):
    print(image_path)
    if image_path != '.' and image_path:
        tag = ID3(file_path)
        mime = get_mime(image_path)
        with open(image_path, 'rb') as im:
            tag['APIC'] = APIC(encoding=3, mime=mime, type=3, desc=u'Cover',data=im.read())
        tag.save()

def check_text(text):
    if repr(text) == '<BoundField value= errors=None>': return ''
    else: return text

def get_mime(path):
    if '.png' in path.lower():
        return 'image/png'
    elif '.jpg' in path.lower():
        return 'image/jpeg'
    else:
        im = Image.open(path)
        im = im.convert('RGB')
        im.save(path, quality=95)
        return 'image/jpeg'
