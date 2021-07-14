import urllib.request
import os
import base64
import json
import socket
import zlib
import threading

def main():
    print('1) Upload a file to the server')
    print('2) Display all firmware')
    print('3) Filtration')
    print('4) Search')
    choose = input('Choose: ')
    menu(int(choose))


def menu(choose):
    if choose == 1:
        sockets()
    elif choose == 2:
        list()
    elif choose == 3:
        filtr()
    elif choose == 4:
        find()
    else:
        print('invalid input')
        main()


def sockets():
    platform = input('Platform: ')
    scope = input('Scope: ')
    version = input('Version: ')
    desc = input('Description: ')
    path_file = input('Enter the path to the file: ')

    host = '127.0.0.1'
    port = 0
    server = ("127.0.0.1", 9090)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(0)
    rT = threading.Thread(args=("RecvThread", sock))
    rT.start()

    fopen = open(f'{path_file}', 'rb')
    lists = fopen.read()
    fileSumCheck = hex(zlib.crc32(lists))
    size = len(lists)

    sock.sendto(("Upload").encode("utf-8"), server)
    sock.sendto((scope).encode("utf-8"), server)
    sock.sendto((platform).encode("utf-8"), server)
    sock.sendto((version).encode("utf-8"), server)
    sock.sendto((desc).encode("utf-8"), server)
    sock.sendto((fileSumCheck).encode("utf-8"), server)
    sock.sendto((size).encode("utf-8"), server)
    while lists:
        sock.send(lists)
        lists = fopen.read()
    sock.close()


def list():
    url = f'http://localhost:8000/get'
    request = urllib.request.Request(url)
    base64string = base64.b64encode(bytes('%s:%s' % ('user', 'user'), 'ascii'))
    request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
    result = urllib.request.urlopen(request)
    resulttext = result.read()
    json_obj_1 = json.loads(resulttext.decode())
    items_full = json_obj_1['content']
    for i, item in enumerate(items_full):
        items_platform = items_full[i]['platform']
        items_version = items_full[i]['version']
        items_scope = items_full[i]['scope']
        print(i + 1, f'Platform: {items_platform}, scope: {items_scope}, version: {items_version}, ')
    print('\n')

    print('1) Download file')
    print('2) contain')
    print('3) exit')
    choose = input('Choose: ')
    if int(choose) == 1:
        download_firmware = input('Choose which firmware to download: ')
        i = int(download_firmware) - 1

        items_platform = items_full[i]['platform']
        items_version = items_full[i]['version']
        items_scope = items_full[i]['scope']
        print('\nYou have selected the firmware: ')
        print(f'Platform: {items_platform}, scope: {items_scope}, version: {items_version}')

        uuid = items_full[i]['uuid']
        download_url = f'http://localhost:8000/load?UUID={uuid}'

        request_download = urllib.request.Request(download_url)
        base64string = base64.b64encode(bytes('%s:%s' % ('user', 'user'), 'ascii'))
        request_download.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
        result_download = urllib.request.urlopen(request_download)
        resulttext_download = result_download.read()
        json_obj_download = json.loads(resulttext_download.decode())
        items_download = json_obj_download['downloadUrl']

        download_file(items_download)
    elif int(choose) == 2:
        main()
    elif int(choose) == 3:
        exit(0)
    else:
        print('Invalid input')
        main()


def filtr():
    platform = input('Platform (Android, iOS Any): ')
    scope = input('Scope: ')
    print('1) Поиск между версиями')
    print('2) Найти версию')
    choos = input('Choose')
    if int(choos) == 1:
        lversion = input('Введите минимальную версию: ')
        rversion = input('Введите максимальную версию: ')
        url = f'http://localhost:8000/get?platform={platform}&lversion={lversion}&rversion={rversion}&scope={scope}'
    elif int(choos) == 2:
        version = input('Version: ')
        url = f'http://localhost:8000/get?platform={platform}&version={version}&scope={scope}'

    request = urllib.request.Request(url)
    base64string = base64.b64encode(bytes('%s:%s' % ('user', 'user'), 'ascii'))
    request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
    result = urllib.request.urlopen(request)
    resulttext = result.read()
    json_obj_1 = json.loads(resulttext.decode())
    items_full = json_obj_1['content']

    for i, item in enumerate(items_full):
        items_platform = items_full[i]['platform']
        items_version = items_full[i]['version']
        items_scope = items_full[i]['scope']
        print(i + 1, f'Platform: {items_platform}, scope: {items_scope}, version: {items_version}')
    print('\n')

    print('1) Download file')
    print('2) contain')
    print('3) exit')
    choose = input('Choose: ')
    if int(choose) == 1:
        download_firmware = input('Choose which firmware to download: ')
        i = int(download_firmware) - 1

        items_platform = items_full[i]['platform']
        items_version = items_full[i]['version']
        items_scope = items_full[i]['scope']
        print('\nYou have selected the firmware: ')
        print(f'Platform: {items_platform}, scope: {items_scope}, version: {items_version}')

        uuid = items_full[i]['uuid']
        download_url = f'http://localhost:8000/load?UUID={uuid}'

        request_download = urllib.request.Request(download_url)
        base64string = base64.b64encode(bytes('%s:%s' % ('user', 'user'), 'ascii'))
        request_download.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
        result_download = urllib.request.urlopen(request_download)
        resulttext_download = result_download.read()
        json_obj_download = json.loads(resulttext_download.decode())
        items_download = json_obj_download['downloadUrl']

        download_file(items_download)
    elif int(choose) == 2:
        main()
    elif int(choose) == 3:
        exit(0)
    else:
        print('Invalid input')
        main()


def find():
    pass


def download_file(url):
    name_file = input('\nName file: ')
    directory = input('Where to put the file?\n')
    file_path = f"{directory}{name_file}.oic"
    urllib.request.urlretrieve(url, file_path)
    print(f'The file has been downloaded, located in the directory:  {file_path}')
    deletefile(file_path)


def deletefile(file_path):
    delete_file = input('Delete a file?(y/n)\n')
    if delete_file == 'y':
        os.remove(file_path)
    elif delete_file == 'n':
        print('You have not deleted the file')
    else:
        print("Invalid input")
        deletefile(file_path)

    print('1) contain')
    print('2) exit')
    vvod = input('Choose: ')
    if int(vvod) == 1:
        main()
    elif int(vvod) == 2:
        exit(0)
    else:
        print('Invalid input')
        main()


main()
pass
