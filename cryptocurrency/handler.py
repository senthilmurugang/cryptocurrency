import sources
import json
from mongoengine import connect
from collections import PriceInfo, OauthCredentials
import ast
import urllib3


connect(
    db='cryptocurrency',
    username='client',
    password='openplease',
)


def convert_to_json(string_to_convert):
    try:
        return json.loads(string_to_convert)
    except:
        return dict()


def get_price_history(currency, from_date, to_date):
    array = []
    for record in PriceInfo.objects:
        array.append(json.dumps({
            'sell': record.sell,
            'buy': record.buy,
            'currency': record.currency,
            'timestamp': str(record.timestamp)
        }))
    return array


def get_client_oauth_credentials(exchange_name):
    return OauthCredentials.objects(exchange=exchange_name).first()


def get_authorize_url(auth_credentials):
    return str(auth_credentials.oauth_token_url)


def get_oauth_client(auth_credentials):
    return auth_credentials.oauth_client


def store_auth_token(exchange_name, response):
    OauthCredentials.objects(exchange=exchange_name).update_one(
        oauth_access_token=response
    )


def get_oauth_access_token(exchange_name):
    auth_credentials = get_client_oauth_credentials(exchange_name)
    print auth_credentials.oauth_access_token.access_token
    return auth_credentials.oauth_access_token.access_token


def request_access_token(exchange_name):
    auth_credentials = get_client_oauth_credentials(exchange_name)
    url = get_authorize_url(auth_credentials)
    oauth_client = get_oauth_client(auth_credentials)
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(basic_auth=oauth_client.client_id+':'+oauth_client.client_secret)
    response = http.request('POST', url, fields={'grant_type': oauth_client.grant_types, 'access_lifetime': 7200},
                            headers=headers)
    print response.data
    store_auth_token(exchange_name, json.loads(response.data))


def read_collections(collection_name):
    return get_client_oauth_credentials('unocoin').to_json()


def write_collections(data):
    string_value = json.loads(json.dumps(data['data']))
    object_map = ast.literal_eval(string_value)
    print object_map
    old = OauthCredentials.objects(exchange=object_map['exchange']).first()
    if old:
        # print type(old), old.oauth_scopes
        if not old.oauth_scope:
            old.oauth_scope = object_map['oauth_scope']
        if not old.oauth_authorization_codes:
            old.oauth_authorization_codes = object_map['oauth_authorization_codes']
        if not old.oauth_refresh_token:
            old.oauth_refresh_token = object_map['oauth_refresh_token']
        if not old.oauth_users:
            print object_map['oauth_users']
            OauthCredentials.objects(exchange=object_map['exchange']).update_one(
                add_to_set__oauth_users=object_map['oauth_users']
            )
        if not old.oauth_jwt:
            old.oauth_jwt = object_map['oauth_jwt']
        if not old.oauth_clients:
            old.oauth_client = object_map['oauth_client']
        old.save()
    else:
        # print old
        OauthCredentials.objects.create(
            exchange=object_map['exchange'],
            oauth_token_url=object_map['oauth_token_url'],
            oauth_client=object_map['oauth_client'],
            oauth_authorization_codes=object_map['oauth_authorization_codes'],
            # oauth_refresh_token=object_map['oauth_refresh_token'],
            oauth_users=object_map['oauth_users'],
            oauth_scopes=object_map['oauth_scopes'],
            oauth_jwt=object_map['oauth_jwt']
        )


def buy_bitcoin(rupees):
    pass


def sell_bitcoin(quantity):
    pass


def http_requester(request_type, url, data, headers):
    try:
        http = urllib3.PoolManager()
        if data is None and data != '':
            response = http.request(request_type, url, fields=data, headers=headers)
        else:
            response = http.request(request_type, url, headers=headers)
    except:
        response = ''
        print "Error occurred"
    return response


def get_current_price(currency):
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + get_oauth_access_token(sources.exchange)}
    response = http_requester('POST', sources.test_url, '', headers)
    response_json = convert_to_json(response.data)
    if response_json and response_json.__contains__('error') and \
            filter(lambda x : x == response_json['error'], ['expired_token', 'invalid_token']):
        print "Error : " + str(response_json)
        request_access_token(sources.exchange)
        update_crypto_currency_rates('inr')
    print response.data
    return response_json


def update_crypto_currency_rates(currency):
    response = get_current_price(currency)
    return response


def calculate_profit(history, current_price, selling_expense):
    pass


def calculate_profits():
    current_price = ''
    selling_expense = ''
    history_list = []
    profit_list = list()
    for history in history_list:
        profit_list.append(calculate_profit(history, current_price, selling_expense))
    return profit_list


if __name__ == '__name__':
    #call any function
    pass

