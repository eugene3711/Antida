import eyed3
from pprint import pprint
# -*- coding: utf-8 -*-
import click
import os
import re


def rightCode(name):
    return name.encode("cp1252").decode("cp1251")


def getMP3s(files, source_path):
    mp3s = []
    for file in files:
        try:
            if file[-3:] == "mp3":
                mp3s.append(eyed3.load(os.path.join(source_path, file)))
                mp3s[-1].file_name = file[:-4]
        except PermissionError:
            print(f'Нет доступа к файлу "{file}"')
    return mp3s


def giveName(file):
    pattern = re.compile("[A-Za-z0-9А-Яа-я]+")

    try:
        track = file.tag.title

    except:
        track = file.file_name[:-3]

    try:
        artist = file.tag.artist
        album = file.tag.album
    except:
        print(f'Файл "{file.file_name}" не был перемещен, нет данных об альбоме или исполнителе')
        return None, None, None
    if artist and album:
        if not (pattern.fullmatch(artist) and pattern.fullmatch(album) and pattern.fullmatch(track)):
            track = rightCode(track)
            artist = rightCode(artist)
            album = rightCode(album)

        while album[-1] == ".":  # если имя файла заканчивается на точку, то не удается найти файл
            album = album[:-1]

        return track, artist, album
    else:
        return None, None, None


def rename(file, name, source_path):
    try:
        old_name = os.path.join(source_path, vars(file)['_path'])
        new_name = os.path.join(source_path, name)
        os.rename(old_name, new_name)
    except:
        print(f'Не удалось переименовать файл "{file.file_name}"')


def transfer(source_path, dest_path, artist, album, name, old_name, file):
    try:
        old_path_name = os.path.join(source_path, name)
        new_path_name = os.path.join(dest_path, artist, album, name)

        if os.path.exists(new_path_name):
            os.remove(new_path_name)

        os.renames(old_path_name, new_path_name)

        print(f"{old_name} -> {new_path_name}")

    except Exception as e:
        print(f'Не удалось переместить файл "{file.file_name}"')
        print(f'Error message: {e}')


def main(source_path, dest_path):
    # проверка директорий на доступность
    if not (os.access(source_path, mode=os.W_OK) and os.access(dest_path, mode=os.R_OK)):
        return "Нет доступа!"

    # список файлов в папке
    files = os.listdir(source_path)
    print(files)

    # проверка файлов на доступность

    # список mp3 файлов
    mp3s = getMP3s(files, source_path)

    # обработка
    for file in mp3s:
        old_name = os.path.join(source_path, vars(file)['_path'])

        # получить имя
        track, artist, album = giveName(file)
        if track is None:
            continue
        name = f"{track} - {artist} - {album}.mp3"

        # переименовать
        rename(file, name, source_path)

        # переместить
        transfer(source_path, dest_path, artist, album, name, old_name, file)

    return "\t Done!"


@click.command()
@click.option('-s', '--src-dir', default=os.getcwd(), help='Папка для исходных файлов')
@click.option('-d', '--dst-dir', default=os.getcwd(), help='Папка назначения')
def output(src_dir, dst_dir):
    click.echo(src_dir)
    click.echo(dst_dir)
    answer = main(src_dir, dst_dir)
    click.echo(answer)


if __name__ == '__main__':
    output()

'''

проверить директории на доступность
проверить файлы на доступность

for each in mp3:
    read <название трека> - <исполнитель> - <альбом>.mp3
        считать
        разобраться с недостающим
        переименовать или бросить
    проверка директории <исполнитель>/<альбом>/<имя файла>
        (создать)
        переместить



       <директория назначения>/<исполнитель>/<альбом>/<имя файла>.mp3
Если в тегах нет информации о названии трека, использует оригинальное имя файла.
Если в тегах нет информации об исполнителе или альбоме, пропускает файл, оставляя его без изменений в исходной директории.
Если в целевой директории файл с таким названием уже существует - заменять его.

target_path = os.path.join(current_path, 'music')

# mode - выставляет права пользователей для каталога
    # o777 - означает что всем можно читать, писать и выполнять файлы каталога
    # exist_ok - не вызывает ошибку если путь уже существует
    os.makedirs(target_path, mode=0o777, exist_ok=True)
    target_path_exists = os.path.exists(target_path) # True

# Переименуем файл music в музыка
old_path_name = os.path.join(current_path, 'музыка', 'file.mp3') # /home/user/music/file.mp3
new_path_name = os.path.join(current_path, 'музыка', "It's my life.mp3") # /home/user/music/It's my life.mp3
os.rename(old_path_name, new_path_name)

Перемещение
old_path_name = os.path.join(current_path, 'музыка', "It's my life.mp3")
new_path_name = os.path.join(current_path, 'music', 'Bon Jovi', "It's my life.mp3")
# Перемещаем файл в новую директорию
# /home/user/музыка/It's my life.mp3 -> /home/user/music/Bon Jovi/It's my life.mp3
os.renames(old_path_name, new_path_name)

Метод os.renames() перенесет файл в целевую директорию по следующим правилам:

Рекурсивно создаст недостающие директории
Перезапишет целевой файл если он существует
Удалит старую директорию, если она пуста 


for mp3 in mp3s:
    print(f"Name {mp3.info}")
    print(f"\tArtist -  {mp3.tag.artist}")
    print(f"\t Album - {mp3.tag.album}")
    print(f"\t Album Artist - {mp3.tag.album_artist}")
    print(f"\t Title - {mp3.tag.title}")
    print(f"\t Track Num - {mp3.tag.track_num}")
    pprint(vars(mp3)['_path'])

# do everything in functions

'''
