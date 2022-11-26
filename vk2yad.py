import app_config

from vk_api import VK_API_Client
from yad_api import YAD_API_Client

import os
from urllib.parse import urlparse
import datetime
import pprint
import json
from tqdm import tqdm

YAD_FOLDER_NAME = 'VK Photos'

def get_a_list_of_photos_from_vk(vk_user_id, number_of_photos):
    """
    Get a list of photos from the 'vk_user_id' profile
    Return list of 'number_of_photos' photos of maximum size
    """
    vk_api = VK_API_Client(app_config.VK_APP_KEY)
    vk_api_response = vk_api.photos_get(
        vk_user_id, album_id='profile', extended='1', photo_sizes='1')
    photos_list = []
    for item in vk_api_response['response']['items']:
        photos_list.append({
            'likes_count':item['likes']['count'],
            'date':item['date'],
            'url':item['sizes'][-1]['url'],
            'size':item['sizes'][-1]['height'] * item['sizes'][-1]['width'],
            'size_type':item['sizes'][-1]['type']
            })
    photos_list = sorted(
        photos_list, key=lambda x: x['size'], reverse=True)
    return photos_list[0:number_of_photos:]

def upload_photos_to_yad(yad_token, folder_name, photos_list):
    """
    Upload files from the list 'photos_list' to the Yandex.Disk of the user
    with the token 'yad_token' to the folder 'folder_name'.
    'progress' parameter is indicator
    of the program operation process (tqdm object)
    """
    yad_api = YAD_API_Client(yad_token)
    """If the folder 'folder_name' is missing, then create it"""
    if not yad_api.get_file_meta_data(folder_name).ok:
        yad_api.create_folder(folder_name)
    
    copy_log = []
    overwrite_all = False
    progress_iterator = tqdm(photos_list)
    for item in progress_iterator:
        file_ext = os.path.splitext(urlparse(item['url']).path)[1]
        file_name = f'{item["likes_count"]}{file_ext}'
        if next((x for x in copy_log if x['file_name'] == file_name), None):
            photo_date = datetime.datetime.fromtimestamp(item['date'])
            photo_date = photo_date.strftime('%Y-%m-%d-%H-%M-%S')
            file_name = f'{item["likes_count"]}-{photo_date}{file_ext}'
        copy_log.append({'file_name':file_name, 'size':item['size_type']})
        full_path = os.path.join(folder_name, file_name)
        delete_file = False
        file_exists = yad_api.get_file_meta_data(full_path).ok
        if file_exists and not overwrite_all:
            progress_iterator.clear()
            delete_file = input(f'Файл \'{file_name}\' уже существует. '
                'Перезаписать? (Y/N/All): ')
            progress_iterator.refresh()
            overwrite_all = delete_file.upper() == 'ALL'
            delete_file = delete_file.upper() == 'Y'
        delete_file = file_exists and (delete_file or overwrite_all)
        if delete_file:
            yad_api.delete_file(full_path)
        
        tqdm.write(f'Копируется файл: {file_name}')
        yad_api.upload_file_from_url(full_path, item['url'])
    
    return copy_log

def save_log(copy_log):
    print('\nОперация сопирования завершена успешно. '
        'Скопированы следующие файлы:')
    pprint.pprint(copy_log)

    log_file_name = ''.join(['log_',
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), '.json'])
    if not os.path.exists('log'):
        os.makedirs('log')
    full_log_path = '/'.join(['log', log_file_name])
    with open(full_log_path, 'w', encoding='utf-8') as f:
        json.dump(copy_log, f, ensure_ascii=False, indent=4)

    print(f'Лог сохранён в файле {full_log_path}.')

def main():
    msg = 'Копирование фотографий с профиля пользователя VK на Яндекс.Диск'
    print(f'\n{msg}')
    print('='*len(msg))

    try:
        """Get input data from the user"""
        vk_user_id = input('Введите \'id\' пользователя VK: ')
        number_of_photos = input(
            'Введите количество сохраняемых фотографий (по умолчанию 5): ')
        number_of_photos = int(number_of_photos) if number_of_photos else 5
        yad_token = input('Введите \'токен\' доступа к Яндекс.Диску : ')
        yad_token =  app_config.YAD_TOKEN if not yad_token else yad_token

        """Get a list of photos from VK"""
        print('\nПолучение списка фотографий из профиля VK...')
        vk_photos = get_a_list_of_photos_from_vk(vk_user_id, number_of_photos)

        """Upload files from the list to Yandex.Disk"""
        copy_log = upload_photos_to_yad(
            yad_token, YAD_FOLDER_NAME, vk_photos)
        
        save_log(copy_log)

    except Exception as e:
        print('\nОбнаружена ошибка (строка '
            f'{e.__traceback__.tb_lineno}): {e}\n')

main()