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
    product_resp = requests.get(prod_link, headers=auth_header)
    product = product_resp.json()['data']

    inventory_link = f'{base_url}/v2/inventories/{product_id}'
    inventory_resp = requests.get(inventory_link, headers=auth_header)
    inventory = inventory_resp.json()

    return {
        'id': product['id'],
        'name': product['attributes']['name'],
        'description': product['attributes']['description'],
        'price': product['meta']['display_price']['without_tax']['amount']/100,
        'currency': product['meta']['display_price']['without_tax']['currency'],
        'sku': product['attributes']['sku'],
        'available': inventory['data']['available'],
    }


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


def get_cart(client_id, secret_key, cart_id):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'{base_url}/v2/carts/{cart_id}/items', headers=headers)
    response.raise_for_status()
    cart_positions = response.json()

    cart = {
        'summa': cart_positions['meta']['display_price']['with_tax']['amount'] / 100,
    }

    cart_products = []
    for position in cart_positions['data']:
        product = {
            'cart_item_id': position['id'],
            'sku': position['sku'],
            'name': position['name'],
            'description': position['description'],
            'quantity': position['quantity'],
            'cost': position['value']['amount'] / 100,
            'currency': position['value']['currency']
        }
        cart_products.append(product)
    cart['products'] = cart_products

    return cart


def create_cart(client_id, secret_key, user_id):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}

    json_data = {
        'data': {
            'type': 'flow',
            'name': f'user cart {user_id}',
            'slug': f'user_cart_{user_id}',
            'description': 'Пользовательская корзина',
            'enabled': True,
        },
    }
    response = requests.post(f'{base_url}/v2/carts/', headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()['data']['id']


def add_product_to_cart(client_id, secret_key, cart_id, product_id, quantity):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}

    json_data = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': quantity,
        },
    }
    response = requests.post(f'{base_url}/v2/carts/{cart_id}/items', headers=headers, json=json_data)
    return response.json()


def del_product_from_cart(client_id, secret_key, cart_id, cart_item_id):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.delete(f'{base_url}/v2/carts/{cart_id}/items/{cart_item_id}', headers=headers)
    response.raise_for_status()


def delete_cart(client_id, secret_key, cart_id):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.delete(f'{base_url}/v2/carts/{cart_id}', headers=headers)
    response.raise_for_status()


def save_customer(client_id, secret_key, name, email):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}

    json_data = {
        'data': {
            'type': 'customer',
            'name': name,
            'email': email
        },
    }
    response = requests.post(f'{base_url}/v2/customers', headers=headers, json=json_data)
    response.raise_for_status()


def find_customer_by_email(client_id, secret_key, email):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'{base_url}/v2/customers?filter=eq(email, {email})', headers=headers)
    response.raise_for_status()
    return response.json()['data']


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    shop_client_id = env('SHOP_CLIENT_ID')
    shop_secret_key = env('SHOP_SECRET_KEY')

    print(create_cart(shop_client_id, shop_secret_key, '901108747'))
    # update.effective_user.id
    exit()

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
    # pprint(get_product_details(shop_client_id, shop_secret_key, product_id))
    # print(get_product_image(shop_client_id, shop_secret_key, product_id))
    # exit()
    # product_id = '425fdd15-511a-4e9a-b1a9-eea086988855'
    prod_details = get_product_details(shop_client_id, shop_secret_key, product_id)
    pprint(prod_details)  # маленькая. Есть картинка
    # print(prod_details['price']['RUB']['amount'])
    # print(get_product_image(shop_client_id, shop_secret_key, product_id))
    # exit()

    # print('My cart')
    # pprint(get_cart(shop_client_id, shop_secret_key, 'd42ff308-943e-40b7-b592-ea0d4877989e'))
    # pprint(get_cart_items(shop_client_id, shop_secret_key, 'd42ff308-943e-40b7-b592-ea0d4877989e'))
