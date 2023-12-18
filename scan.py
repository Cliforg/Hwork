import sys
from pathlib import Path

jpeg_files = []
png_files = []
jpg_files = []
avi_files = []
mp4_files = []
mov_files = []
doc_files = []
docx_files = []
txt_files = []
mp3_files = []
wav_files = []
folders = []
archives = []
others = []
unknown = set()
extensions = set()

registered_extentions = {
    'JPEG': jpeg_files,
    'PNG': png_files,
    'JPG': jpg_files,
    'AVI': avi_files,
    'MP4': mp4_files,
    'MOV': mov_files,
    'DOC': doc_files,
    'DOCX': docx_files,
    'TXT': txt_files,
    'MP3': mp3_files,
    'WAV': wav_files,
    'ZIP': archives
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('IMAGES', 'DOCUMENTS', 'AUDIO', 'VIDEO', 'ARCHIVE', 'OTHERS'):
                folders.append(item)
                scan(item)
            continue
        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extentions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}') 
 

    folder = Path(path)
    scan(folder)              
    print(f'All known extensions: {extensions}')
    print(f'All unknown extensions: {unknown}')
