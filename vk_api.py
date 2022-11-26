import requests

VK_API_URI = 'https://api.vk.com/method'
VK_API_VER = '5.131'

class VK_API_Client:
    """VK API Client"""
    def __init__(self, app_key:str) -> None:
        self.__params = {
            'v' : VK_API_VER,
            'access_token' : app_key
        }
    
    def photos_get(
        self,
        owner_id:str,
        album_id:str,
        **kwargs):
        """
        Method photos.get
        Returns a list of photos in the album.
        Details: https://dev.vk.com/method/photos.get 
        """
        request_params = {'owner_id':owner_id, 'album_id':album_id}
        request_params = request_params | kwargs | self.__params
        api_response = requests.get(VK_API_URI + '/photos.get',
            params=request_params)
        if not api_response.ok: api_response.raise_for_status()
        api_response = api_response.json()
        if 'error' in api_response: raise Exception(
            f'VK_API_Client Error [{api_response["error"]["error_code"]}]',
            api_response['error']['error_msg'])
        return api_response