import requests

YAD_URL = 'https://cloud-api.yandex.net/v1/disk'

class YAD_API_Client:
    """ Yandex.Disk API Client"""
    def __init__(self, token) -> None:
        self.__headers = {
            'Accept':'application/json',
            'Content-Type':'application/json',
            'Authorization':token
            }

    def get_file_meta_data(self, file_path: str):
        """
        Gets meta information about a file or folder.
        The file (folder) name is passed in the 'file_path' parameter.
        Returns the request.response object.
        Details: https://yandex.ru/dev/disk/api/reference/meta.html
        """
        params = {'path': file_path}
        file_info_url = ''.join([YAD_URL, '/resources'])
        return requests.get(
            file_info_url, headers=self.__headers, params=params)
    
    def create_folder(self, folder_name):
        """
        Create Folder 'folder_name'
        Returns the request.response.json().
        Details: https://yandex.ru/dev/disk/api/reference/create-folder.html
        """
        params = {'path': folder_name}
        new_folder_url = ''.join([YAD_URL, '/resources'])
        api_response = requests.put(
            new_folder_url, headers=self.__headers, params=params)
        if not api_response.ok: api_response.raise_for_status()
        return api_response.json()

    def upload_file_from_url(self, file_name, source_url):
        """
        Download a file from the 'source_url' to Disk as 'file_name'
        Details: https://yandex.ru/dev/disk/api/reference/upload-ext.html
        """
        file_upload_url = ''.join([YAD_URL, '/resources/upload'])
        params = {'path': file_name, 'url': source_url}
        api_response = requests.post(file_upload_url,
            params=params, headers=self.__headers)
        if not api_response.ok: api_response.raise_for_status()
        return api_response

    def delete_file(self, file_name, permanently=False):
        """
        Delete a file or folder 'file_name'
        If the 'permanently' is True, the file is permanently deleted,
        bypassing the Trash
        Details: https://yandex.ru/dev/disk/api/reference/delete.html
        """
        file_delete_url = ''.join([YAD_URL, '/resources'])
        params = {'path': file_name, 'permanently': permanently}
        api_response = requests.delete(file_delete_url,
            params=params, headers=self.__headers)
        if not api_response.ok: api_response.raise_for_status()
        return api_response