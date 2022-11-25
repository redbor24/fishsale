import requests
from environs import Env
from pprint import pprint

base_url = 'https://api.moltin.com'


def _login(client_id, secret_key):
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': secret_key,
    }
    response = requests.post(f'{base_url}/oauth/access_token', data=data)
    return response.json()['access_token']


def get_products(client_id, secret_key):
    access_token = _login(client_id, secret_key)
    prod_link = f'{base_url}/pcm/catalog/products'
    auth_header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(prod_link, headers=auth_header)
    return response.json()['data']


def get_product_details(client_id, secret_key, product_id):
    access_token = _login(client_id, secret_key)
    prod_link = f'{base_url}/pcm/catalog/products/{product_id}'
    auth_header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(prod_link, headers=auth_header)
    return response.json()['data']


def get_product_image(client_id, secret_key, product_id):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{base_url}/pcm/products/{product_id}/relationships/main_image', headers=headers)

    parsed = response.json()
    if not parsed['data']:
        return

    file_id = response.json()['data']['id']
    response = requests.get(f'{base_url}/v2/files/{file_id}', headers=headers)
    return response.json()['data']['link']['href']


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    shop_client_id = env('SHOP_CLIENT_ID')
    shop_secret_key = env('SHOP_SECRET_KEY')

    # products = get_products(shop_client_id, shop_secret_key)
    # prods = []
    # for product in products:
    #     name = product['attributes']['name']
    #     product_id = product['id']
    #     prods.append({
    #             'id': product_id,
    #             'name': name
    #         }
    #     )
    # pprint(prods)

    product_id = '2de526c6-d465-40db-9701-2e766e9aaf43'  # большая. Нет картинки
    pprint(get_product_details(shop_client_id, shop_secret_key, product_id))
    print(get_product_image(shop_client_id, shop_secret_key, product_id))
    # exit()
    product_id = '425fdd15-511a-4e9a-b1a9-eea086988855'
    pprint(get_product_details(shop_client_id, shop_secret_key, product_id))  # маленькая. Есть картинка
    print(get_product_image(shop_client_id, shop_secret_key, product_id))
    exit()
