import requests
from pprint import pprint

base_url = 'https://api.moltin.com'
headers = {'Content-Type': 'application/x-www-form-urlencoded',}
client_id = 'a4752893f001710fcd6cb1fd2f19d2c8429db2b603'
secret_key = '8349aeeba1e51cbe387e810f4b6e9f8ea697c433a8'
data = f'client_id={client_id}&client_secret={secret_key}&grant_type=client_credentials'

response = requests.post(f'{base_url}/oauth/access_token', headers=headers, data=data)
access_token = response.json()['access_token']
print(f'access_token: {access_token}')

headers = {'Authorization': access_token,}

# 1. Create a custom flow for shipping providers by making the following request:
# json_data = {
#     'data': {
#         'type': 'flow',
#         'name': 'shipping_provider',
#         'slug': 'shipping_provider',
#         'description': 'Creates a new shipping provider resource',
#         'enabled': True,
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/flows', headers=headers, json=json_data)
# pprint(response.text)
flow_id = 'ca265da9-d039-4613-9546-e88d59f87d31'

# 2. Create Name field for the shipping provider by making the following request:
# json_data = {
#     'data': {
#         'type': 'field',
#         'name': 'Name',
#         'slug': 'name',
#         'field_type': 'string',
#         'description': 'Shipping provider name',
#         'required': False,
#         'default': 0,
#         'enabled': True,
#         'order': 1,
#         'relationships': {
#             'flow': {
#                 'data': {
#                     'type': 'flow',
#                     'id': flow_id,
#                 },
#             },
#         },
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/fields', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"609d1a36-c2ed-42a9-acc2-5cde216b3611","type":"field","field_type":"string","slug":"name","name":"Name","description":"Shipping '
#  'provider '
#  'name","required":false,"default":0,"enabled":true,"order":1,"omit_null":false,"validation_rules":[],"links":{"self":"https://api.moltin.com/v2/flows/ca265da9-d039-4613-9546-e88d59f87d31/fields/609d1a36-c2ed-42a9-acc2-5cde216b3611"},"relationships":{"flow":{"data":{"id":"ca265da9-d039-4613-9546-e88d59f87d31","type":"flow"}}},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:07:43.855Z","updated_at":"2022-11-24T08:07:43.855Z"}}}}')

# 3. Create Cost field for the shipping provider by making the following request:
# json_data = {
#     'data': {
#         'type': 'field',
#         'name': 'Cost',
#         'slug': 'cost',
#         'field_type': 'integer',
#         'description': 'Shipping provider cost',
#         'required': False,
#         'default': 0,
#         'enabled': True,
#         'order': 1,
#         'relationships': {
#             'flow': {
#                 'data': {
#                     'type': 'flow',
#                     'id': flow_id,
#                 },
#             },
#         },
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/fields', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"899f5b05-14a5-4717-a377-aab1235e05c3","type":"field","field_type":"integer","slug":"cost","name":"Cost","description":"Shipping '
#  'provider '
#  'cost","required":false,"default":0,"enabled":true,"order":1,"omit_null":false,"validation_rules":[],"links":{"self":"https://api.moltin.com/v2/flows/ca265da9-d039-4613-9546-e88d59f87d31/fields/899f5b05-14a5-4717-a377-aab1235e05c3"},"relationships":{"flow":{"data":{"id":"ca265da9-d039-4613-9546-e88d59f87d31","type":"flow"}}},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:41:21.577Z","updated_at":"2022-11-24T08:41:21.577Z"}}}}')
# exit()

# 4. Create a new core flow that extends the orders resource by making the following request:
# json_data = {
#     'data': {
#         'type': 'flow',
#         'name': 'orders',
#         'slug': 'orders',
#         'description': 'Extending the orders resource',
#         'enabled': True,
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/flows', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"5f2047a5-d694-434e-8d3c-460336275b5d","type":"flow","name":"orders","slug":"orders","description":"Extending '
#  'the orders '
#  'resource","enabled":true,"links":{"self":"https://api.moltin.com/v2/flows/5f2047a5-d694-434e-8d3c-460336275b5d"},"relationships":{},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:10:04.106Z","updated_at":"2022-11-24T08:10:04.106Z"}}}}')
orders_flow_id = '5f2047a5-d694-434e-8d3c-460336275b5d'

# 5. Create a Consignment ID field to store and display the consignment number for each order as in the following example:
# json_data = {
#     'data': {
#         'type': 'field',
#         'name': 'Consignment ID',
#         'slug': 'consignment-id',
#         'field_type': 'string',
#         'description': 'Consignment number for each order',
#         'required': False,
#         'default': 0,
#         'enabled': True,
#         'order': 1,
#         'relationships': {
#             'flow': {
#                 'data': {
#                     'type': 'flow',
#                     'id': flow_id,
#                 },
#             },
#         },
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/fields', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"29d1422d-9796-45ee-af4b-cfb70c6ea7cf","type":"field","field_type":"string","slug":"consignment-id","name":"Consignment '
#  'ID","description":"Consignment number for each '
#  'order","required":false,"default":0,"enabled":true,"order":1,"omit_null":false,"validation_rules":[],"links":{"self":"https://api.moltin.com/v2/flows/ca265da9-d039-4613-9546-e88d59f87d31/fields/29d1422d-9796-45ee-af4b-cfb70c6ea7cf"},"relationships":{"flow":{"data":{"id":"ca265da9-d039-4613-9546-e88d59f87d31","type":"flow"}}},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:12:12.795Z","updated_at":"2022-11-24T08:12:12.795Z"}}}}')

# 6. Create a Shipping Provider relationship field as in the following example:
# json_data = {
#     'data': {
#         'type': 'field',
#         'name': 'Shipping Provider',
#         'slug': 'shipping-provider',
#         'description': 'The shipping provider used to send the order',
#         'required': False,
#         'field_type': 'relationship',
#         'relationships': {
#             'flow': {
#                 'data': {
#                     'type': 'flow',
#                     'id': flow_id,
#                 },
#             },
#         },
#         'validation_rules': [
#             {
#                 'type': 'one-to-one',
#                 'to': 'shipping-provider',
#             },
#         ],
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/fields', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"a0e786b9-74c3-4efc-a710-33c1f9337fb6","type":"field","field_type":"relationship","slug":"shipping-provider","name":"Shipping '
#  'Provider","description":"The shipping provider used to send the '
#  'order","required":false,"default":null,"enabled":true,"order":null,"omit_null":false,"validation_rules":[{"type":"one-to-one","to":"shipping-provider"}],"links":{"self":"https://api.moltin.com/v2/flows/ca265da9-d039-4613-9546-e88d59f87d31/fields/a0e786b9-74c3-4efc-a710-33c1f9337fb6"},"relationships":{"flow":{"data":{"id":"ca265da9-d039-4613-9546-e88d59f87d31","type":"flow"}}},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:13:31.871Z","updated_at":"2022-11-24T08:13:31.871Z"}}}}')

# 7. Create entries for the Shipping Provider flow fields that you created in the previous step as in the following example:
# json_data = {
#     'data': {
#         'type': 'entry',
#         'name': 'Ralphio 720',
#         'cost': 720,
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/flows/shipping_provider/entries', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"d4482439-b265-4d29-8b2f-5113bb367d01","type":"entry","name":"Ralphio '
#  '720","consignment-id":"0","meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:20:51.016Z","updated_at":"2022-11-24T08:20:51.016Z"}},"links":{"self":"https://api.moltin.com/v2/flows/shipping_provider/entries/d4482439-b265-4d29-8b2f-5113bb367d01"}}}')
shipping_provider_entry_id = 'd4482439-b265-4d29-8b2f-5113bb367d01'

# 8. If you don’t have any existing flow for the cart resource, create a new core flow for carts that extends your carts
# resource as in the following example:
# json_data = {
#     'data': {
#         'type': 'flow',
#         'name': 'carts',
#         'slug': 'carts',
#         'description': 'Extending the carts resource',
#         'enabled': True,
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/flows', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"59b016d9-7748-4712-9c38-798e71da8dca","type":"flow","name":"carts","slug":"carts","description":"Extending '
#  'the carts '
#  'resource","enabled":true,"links":{"self":"https://api.moltin.com/v2/flows/59b016d9-7748-4712-9c38-798e71da8dca"},"relationships":{},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:24:21.435Z","updated_at":"2022-11-24T08:24:21.435Z"}}}}')
cart_flow_id = '59b016d9-7748-4712-9c38-798e71da8dca'

# 9. Create a relationship field between the shipping provider flow and the carts flow as in the following example:
# json_data = {
#     'data': {
#         'type': 'field',
#         'name': 'Shipping Provider',
#         'slug': 'shipping-provider',
#         'description': 'The shipping provider used to send the order',
#         'required': False,
#         'field_type': 'relationship',
#         'relationships': {
#             'flow': {
#                 'data': {
#                     'type': 'flow',
#                     'id': cart_flow_id,
#                 },
#             },
#         },
#         'validation_rules': [
#             {
#                 'type': 'one-to-one',
#                 'to': 'shipping-provider',
#             },
#         ],
#     },
# }
#
# response = requests.post('https://api.moltin.com/v2/fields', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"fc51e3c7-f679-4541-9f1b-e38e9e51b9eb","type":"field","field_type":"relationship","slug":"shipping-provider","name":"Shipping '
#  'Provider","description":"The shipping provider used to send the '
#  'order","required":false,"default":null,"enabled":true,"order":null,"omit_null":false,"validation_rules":[{"type":"one-to-one","to":"shipping-provider"}],"links":{"self":"https://api.moltin.com/v2/flows/59b016d9-7748-4712-9c38-798e71da8dca/fields/fc51e3c7-f679-4541-9f1b-e38e9e51b9eb"},"relationships":{"flow":{"data":{"id":"59b016d9-7748-4712-9c38-798e71da8dca","type":"flow"}}},"meta":{"owner":"store","timestamps":{"created_at":"2022-11-24T08:27:07.677Z","updated_at":"2022-11-24T08:27:07.677Z"}}}}')

# 10. Do the following and create an order:
#   10.1. Replace the :cart-reference with a value, such as 1234 in the following request and get the cart:
# response = requests.get(f'{base_url}/v2/carts/{cart_flow_id}', headers=headers)
# pprint(response.text)

#   10.2. Make the following request with the product id that you created in the store earlier and add the item to the cart:
# product_id = '425fdd15-511a-4e9a-b1a9-eea086988855'
# json_data = {
#     'data': {
#         'id': product_id,
#         'type': 'cart_item',
#         'quantity': 1,
#     },
# }
#
# response = requests.get(f'{base_url}/v2/carts/{cart_flow_id}/items', headers=headers, json=json_data)
# # response = requests.get('https://api.moltin.com/v2/carts/:cart-reference/items', headers=headers, json=json_data)
# pprint(response.text)
# '{"data":[],"meta":{"display_price":{"with_tax":{"amount":0,"currency":"","formatted":"0"},"without_tax":{"amount":0,"currency":"","formatted":"0"},"tax":{"amount":0,"currency":"","formatted":"0"},"discount":{"amount":0,"currency":"","formatted":"0"},"without_discount":{"amount":0,"currency":"","formatted":"0"}},"timestamps":{"created_at":"2022-11-24T08:44:48Z","updated_at":"2022-11-24T08:44:48Z","expires_at":"2022-11-24T08:44:48Z"}}}'

#   10.3. Add the shipping provider to the cart by creating a relationship entry for the Ralphio 720 as in the following example:
# json_data = {
#     'data': {
#         'id': shipping_provider_entry_id,
#         'type': 'entry',
#     },
# }
#
# # response = requests.post('https://api.moltin.com/v2/carts/entries/:cart-reference/relationships/shipping-provider',
# response = requests.post(f'{base_url}/v2/carts/{cart_flow_id}/relationships/shipping-provider', headers=headers, json=json_data)
# pprint(response.text)
# '{"data":{"id":"d4482439-b265-4d29-8b2f-5113bb367d01","type":"entry"}}'

#   10.4. Make the following request and add the custom item, shipping charge, to the cart:
# json_data = {
#     'data': {
#         'type': 'custom_item',
#         'name': 'Ralphio 720',
#         'sku': 'ralphio-720',
#         'description': 'Adds charges for shipping',
#         'quantity': 1,
#         'price': {
#             'amount': 720,
#         },
#     },
# }
#
# # response = requests.post('https://api.moltin.com/v2/carts/:cart-reference/items', headers=headers, json=json_data)
# response = requests.post(f'{base_url}/v2/carts/{cart_flow_id}/items', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":[{"id":"255d4217-d9a1-4b43-bcc5-fe9c91fa8d33","type":"custom_item","name":"Ralphio '
#  '720","description":"Adds charges for '
#  'shipping","sku":"ralphio-720","slug":"","image":{"mime_type":"","file_name":"","href":""},"quantity":1,"manage_stock":false,"unit_price":{"amount":720,"currency":"RUB","includes_tax":true},"value":{"amount":720,"currency":"RUB","includes_tax":true},"links":{},"meta":{"display_price":{"with_tax":{"unit":{"amount":720,"currency":"RUB","formatted":"7.20"},"value":{"amount":720,"currency":"RUB","formatted":"7.20"}},"without_tax":{"unit":{"amount":720,"currency":"RUB","formatted":"7.20"},"value":{"amount":720,"currency":"RUB","formatted":"7.20"}},"tax":{"unit":{"amount":0,"currency":"RUB","formatted":"0.00"},"value":{"amount":0,"currency":"RUB","formatted":"0.00"}},"discount":{"unit":{"amount":0,"currency":"RUB","formatted":"0.00"},"value":{"amount":0,"currency":"RUB","formatted":"0.00"}},"without_discount":{"unit":{"amount":720,"currency":"RUB","formatted":"7.20"},"value":{"amount":720,"currency":"RUB","formatted":"7.20"}}},"timestamps":{"created_at":"2022-11-24T09:01:03Z","updated_at":"2022-11-24T09:01:03Z"}}}],"meta":{"display_price":{"with_tax":{"amount":720,"currency":"RUB","formatted":"7.20"},"without_tax":{"amount":720,"currency":"RUB","formatted":"7.20"},"tax":{"amount":0,"currency":"RUB","formatted":"0.00"},"discount":{"amount":0,"currency":"RUB","formatted":"0.00"},"without_discount":{"amount":720,"currency":"RUB","formatted":"7.20"}},"timestamps":{"created_at":"2022-11-24T09:01:03Z","updated_at":"2022-11-24T09:01:03Z","expires_at":"2022-12-01T09:01:03Z"}}}')

#   10.5. To Checkout the cart as an anonymous user, use the customer object and make the following request:
# json_data = {
#     'data': {
#         'customer': {
#             'email': 'leslie.knope@gov.com',
#             'name': 'Leslie Knope',
#         },
#         'billing_address': {
#             'first_name': 'Leslie',
#             'last_name': 'Knope',
#             'company_name': 'Parks and Recreations Dept.',
#             'line_1': '2nd Floor British India House',
#             'line_2': '15 Carliol Square',
#             'city': 'Pawnee',
#             'postcode': 'NE1 6UF',
#             'county': 'Indiana',
#             'country': 'US',
#         },
#         'shipping_address': {
#             'first_name': 'Leslie',
#             'last_name': 'Knope',
#             'company_name': 'Parks and Recreations Dept.',
#             'phone_number': '(555) 555-1234',
#             'line_1': '2nd Floor British India House',
#             'line_2': '15 Carliol Square',
#             'city': 'Pawnee',
#             'postcode': 'NE1 6UF',
#             'county': 'Indiana',
#             'country': 'US',
#             'instructions': 'Leave with Ron Swanson',
#         },
#     },
# }
#
# # response = requests.post('https://api.moltin.com/v2/carts/:cart-reference/checkout', headers=headers, json=json_data)
# response = requests.post(f'{base_url}/v2/carts/{cart_flow_id}/checkout', headers=headers, json=json_data)
# pprint(response.text)
# ('{"data":{"id":"c09fb199-171f-47ca-8055-3837b80f3091","type":"order","status":"incomplete","payment":"unpaid","shipping":"unfulfilled","anonymized":false,"customer":{"name":"Leslie '
#  'Knope","email":"leslie.knope@gov.com"},"shipping_address":{"first_name":"Leslie","last_name":"Knope","phone_number":"(555) '
#  '555-1234","company_name":"Parks and Recreations Dept.","line_1":"2nd Floor '
#  'British India House","line_2":"15 Carliol '
#  'Square","city":"Pawnee","postcode":"NE1 '
#  '6UF","county":"Indiana","country":"US","instructions":"Leave with Ron '
#  'Swanson"},"billing_address":{"first_name":"Leslie","last_name":"Knope","company_name":"Parks '
#  'and Recreations Dept.","line_1":"2nd Floor British India House","line_2":"15 '
#  'Carliol Square","city":"Pawnee","postcode":"NE1 '
#  '6UF","county":"Indiana","country":"US"},"links":{},"meta":{"display_price":{"with_tax":{"amount":720,"currency":"RUB","formatted":"7.20"},"without_tax":{"amount":720,"currency":"RUB","formatted":"7.20"},"tax":{"amount":0,"currency":"RUB","formatted":"0.00"},"discount":{"amount":0,"currency":"RUB","formatted":"0.00"},"balance_owing":{"amount":720,"currency":"RUB","formatted":"7.20"},"paid":{"amount":0,"currency":"RUB","formatted":"0.00"},"authorized":{"amount":0,"currency":"RUB","formatted":"0.00"},"without_discount":{"amount":720,"currency":"RUB","formatted":"7.20"}},"timestamps":{"created_at":"2022-11-24T09:12:10Z","updated_at":"2022-11-24T09:12:10Z"}},"relationships":{"items":{"data":[{"type":"item","id":"91fdfeee-dcb1-40a6-a5a2-f3d170fa46c9"}]}}},"included":{"items":[{"type":"order_item","id":"91fdfeee-dcb1-40a6-a5a2-f3d170fa46c9","quantity":1,"product_id":"","name":"Ralphio '
#  '720","sku":"ralphio-720","unit_price":{"amount":720,"currency":"RUB","includes_tax":true},"value":{"amount":720,"currency":"RUB","includes_tax":true},"links":{},"meta":{"display_price":{"with_tax":{"unit":{"amount":720,"currency":"RUB","formatted":"7.20"},"value":{"amount":720,"currency":"RUB","formatted":"7.20"}},"without_tax":{"unit":{"amount":720,"currency":"RUB","formatted":"7.20"},"value":{"amount":720,"currency":"RUB","formatted":"7.20"}},"tax":{"unit":{"amount":0,"currency":"RUB","formatted":"0.00"},"value":{"amount":0,"currency":"RUB","formatted":"0.00"}},"discount":{"unit":{"amount":0,"currency":"RUB","formatted":"0.00"},"value":{"amount":0,"currency":"RUB","formatted":"0.00"}},"without_discount":{"unit":{"amount":720,"currency":"RUB","formatted":"7.20"},"value":{"amount":720,"currency":"RUB","formatted":"7.20"}}},"timestamps":{"created_at":"2022-11-24T09:12:10Z","updated_at":"2022-11-24T09:12:10Z"}},"relationships":{"cart_item":{"data":{"type":"cart_item","id":"255d4217-d9a1-4b43-bcc5-fe9c91fa8d33"}}}}]}}')
order_id = 'c09fb199-171f-47ca-8055-3837b80f3091'

#   10.6. To add Ralphio 720 to the order, make the following request and create a relationship entry for the shipping provider:
# json_data = {
#     'data': {
#         'id': shipping_provider_entry_id,
#         'type': 'entry',
#     },
# }
# response = requests.post('https://api.moltin.com/v2/orders/:order-id/relationships/shipping-provider', headers=headers, json=json_data)
# response = requests.post(f'{base_url}/v2/orders/{order_id}/relationships/shipping-provider', headers=headers, json=json_data)
# response = requests.get(f'{base_url}/v2/orders/{order_id}/relationships', headers=headers, json=json_data)
# pprint(response.text)
# '{"data":null}'

#   10.7. Make the following request and update the order with the consignment ID:


# 11. Make the following request and get the order with the shipping details:
# response = requests.get(f'{base_url}/v2/orders/{order_id}', headers=headers)
# pprint(response.json())
# {'data': {'anonymized': False,
#           'billing_address': {'city': 'Pawnee',
#                               'company_name': 'Parks and Recreations Dept.',
#                               'country': 'US',
#                               'county': 'Indiana',
#                               'first_name': 'Leslie',
#                               'last_name': 'Knope',
#                               'line_1': '2nd Floor British India House',
#                               'line_2': '15 Carliol Square',
#                               'postcode': 'NE1 6UF'},
#           'customer': {'email': 'leslie.knope@gov.com', 'name': 'Leslie Knope'},
#           'id': 'c09fb199-171f-47ca-8055-3837b80f3091',
#           'links': {},
#           'meta': {'display_price': {'authorized': {'amount': 0,
#                                                     'currency': 'RUB',
#                                                     'formatted': '0.00'},
#                                      'balance_owing': {'amount': 720,
#                                                        'currency': 'RUB',
#                                                        'formatted': '7.20'},
#                                      'discount': {'amount': 0,
#                                                   'currency': 'RUB',
#                                                   'formatted': '0.00'},
#                                      'paid': {'amount': 0,
#                                               'currency': 'RUB',
#                                               'formatted': '0.00'},
#                                      'tax': {'amount': 0,
#                                              'currency': 'RUB',
#                                              'formatted': '0.00'},
#                                      'with_tax': {'amount': 720,
#                                                   'currency': 'RUB',
#                                                   'formatted': '7.20'},
#                                      'without_discount': {'amount': 720,
#                                                           'currency': 'RUB',
#                                                           'formatted': '7.20'},
#                                      'without_tax': {'amount': 720,
#                                                      'currency': 'RUB',
#                                                      'formatted': '7.20'}},
#                    'timestamps': {'created_at': '2022-11-24T09:12:10Z',
#                                   'updated_at': '2022-11-24T09:12:10Z'}},
#           'payment': 'unpaid',
#           'relationships': {'items': {'data': [{'id': ' ,
#                                                 'type': 'item'}]}},
#           'shipping': 'unfulfilled',
#           'shipping_address': {'city': 'Pawnee',
#                                'company_name': 'Parks and Recreations Dept.',
#                                'country': 'US',
#                                'county': 'Indiana',
#                                'first_name': 'Leslie',
#                                'instructions': 'Leave with Ron Swanson',
#                                'last_name': 'Knope',
#                                'line_1': '2nd Floor British India House',
#                                'line_2': '15 Carliol Square',
#                                'phone_number': '(555) 555-1234',
#                                'postcode': 'NE1 6UF'},
#           'status': 'incomplete',
#           'type': 'order'}}



# Очистка корзины ???
response = requests.delete(f'{base_url}/v2/carts/{shipping_provider_entry_id}/items', headers=headers)

# Получаем содержимое корзины
# 'https://api.moltin.com/v2/carts/:reference'
print('-'*20 + ' КОРЗИНА ' + '-'*20)
response = requests.get(f'{base_url}/v2/carts/{shipping_provider_entry_id}', headers=headers)
pprint(response.json())

# Добавляем в корзину какую-то фигню, которой нет в справочнике товаров
json_data = {
    'data': {
        'type': 'custom_item',
        'name': 'Something 152',
        'sku': 'something-152',
        'description': 'Неизвестный каталогу товар',
        'quantity': 3,
        'price': {
            'amount': 152,
        },
    },
}

# response = requests.post('https://api.moltin.com/v2/carts/:cart-reference/items', headers=headers, json=json_data)
response = requests.post(f'{base_url}/v2/carts/{cart_flow_id}/items', headers=headers, json=json_data)
print('-'*20 + ' Добавили фигню ' + '-'*20)
pprint(response.json())
exit()
response = requests.get(f'{base_url}/v2/carts/{shipping_provider_entry_id}', headers=headers)
pprint(response.json())
