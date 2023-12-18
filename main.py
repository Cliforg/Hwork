import sys
import scan
import shutil
import normalize
from pathlib import Path


def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok = True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok = True)
    new_name = normalize.normalize(path.name.replace('.zip', ''))
    archive_folder = target_folder / new_name

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def process_folder(folder_path):
    result = ""
    for file in folder_path.rglob('*'):
        if file.is_file():
            result += file.name + ', '
    return result

def main(folder_path):
    
    scan.scan(folder_path)


    for file in scan.jpeg_files:
        handle_file(file, folder_path, 'IMAGES') 

    for file in scan.png_files:
        handle_file(file, folder_path, 'IMAGES')                                

    for file in scan.jpg_files:
        handle_file(file, folder_path, 'IMAGES') 

    for file in scan.avi_files:
        handle_file(file, folder_path, 'VIDEO') 

    for file in scan.mp4_files:
        handle_file(file, folder_path, 'VIDEO') 

    for file in scan.mov_files:
        handle_file(file, folder_path, 'VIDEO')

    for file in scan.doc_files:
        handle_file(file, folder_path, 'DOCUMENTS')

    for file in scan.docx_files:
        handle_file(file, folder_path, 'DOCUMENTS')

    for file in scan.txt_files:
        handle_file(file, folder_path, 'DOCUMENTS')

    for file in scan.mp3_files:
        handle_file(file, folder_path, 'AUDIO')

    for file in scan.wav_files:
        handle_file(file, folder_path, 'AUDIO')

    for file in scan.others:
        handle_file(file, folder_path, 'OTHERS')

    for file in scan.archives:
        handle_archive(file, folder_path, 'ARCHIVE') 

    images_result = process_folder(folder_path / 'IMAGES')
    video_result = process_folder(folder_path / 'VIDEO')
    documents_result = process_folder(folder_path / 'DOCUMENTS')
    audio_result = process_folder(folder_path / 'AUDIO')
    others_result = process_folder(folder_path / 'OTHERS')
    archive_result = process_folder(folder_path / 'ARCHIVE')

    remove_empty_folders(folder_path)

    print('List of files in categories: ')
    print("IMAGES:\n", images_result)
    print("VIDEO:\n", video_result)
    print("DOCUMENTS:\n", documents_result)
    print("AUDIO:\n", audio_result)
    print("ARCHIVE:\n", archive_result)    
    print("OTHERS:\n", others_result)



if __name__ == '__main__':
    path = sys.argv[1]


    folder = Path(path)
    main(folder.resolve())
    scan.scan(folder)
    print(f'All known extensions: {scan.extensions}')
    print(f'All unknown extensions: {scan.unknown}')
    