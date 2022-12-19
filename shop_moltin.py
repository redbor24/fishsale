import requests

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
    response.raise_for_status()
    return response.json()['data']


def get_product_details(client_id, secret_key, product_id):
    access_token = _login(client_id, secret_key)
    prod_link = f'{base_url}/pcm/catalog/products/{product_id}'
    auth_header = {'Authorization': f'Bearer {access_token}'}
    product_resp = requests.get(prod_link, headers=auth_header)
    product_resp.raise_for_status()
    product = product_resp.json()['data']

    inventory_link = f'{base_url}/v2/inventories/{product_id}'
    inventory_resp = requests.get(inventory_link, headers=auth_header)
    inventory = inventory_resp.json()

    return {
        'id': product['id'],
        'name': product['attributes']['name'],
        'description': product['attributes']['description'],
        'price': product['meta']['display_price']['without_tax']['amount'] / 100,
        'currency': product['meta']['display_price']['without_tax']['currency'],
        'sku': product['attributes']['sku'],
        'available': inventory['data']['available'],
    }


def get_product_image(client_id, secret_key, product_id):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{base_url}/pcm/products/{product_id}/relationships/main_image', headers=headers)
    if not response.ok:
        return

    image = response.json()
    if not image['data']:
        return

    response = requests.get(f'{base_url}/v2/files/{image["data"]["id"]}', headers=headers)
    response.raise_for_status()
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
    response.raise_for_status()
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

    customer = {
        'data': {
            'type': 'customer',
            'name': name,
            'email': email
        },
    }
    response = requests.post(f'{base_url}/v2/customers', headers=headers, json=customer)
    response.raise_for_status()


def find_customer_by_email(client_id, secret_key, email):
    access_token = _login(client_id, secret_key)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'{base_url}/v2/customers?filter=eq(email, {email})', headers=headers)
    response.raise_for_status()
    return response.json()['data']
