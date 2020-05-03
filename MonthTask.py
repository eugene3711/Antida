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

