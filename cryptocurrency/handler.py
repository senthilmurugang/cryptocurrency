import sources
import urllib, json, datetime
from mongoengine import connect
from collections import PriceInfo, OauthClients, OauthAccessTokens, \
    OauthAuthorizationCodes, OauthJwt, OauthRefreshTokens, OauthScopes, OauthUsers, OauthCredentials
import ast, urllib2, urllib3


connect(
    db='cryptocurrency',
    username='client',
    password='openplease',
)


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


def get_oauth_access_tokens(auth_credentials):
    return auth_credentials.oauth_access_tokens


def get_authorize_url(auth_credentials):
    return str(auth_credentials.oauth_token_url)


def get_oauth_clients(auth_credentials):
    return auth_credentials.oauth_clients


def store_auth_token(exchange_name, response):
    OauthCredentials.objects(exchange=exchange_name).modify(
        oauth_access_tokens=response
    )


def get_oauth_access_token(exchange_name):
    auth_credentials = get_client_oauth_credentials(exchange_name)
    access_token = get_oauth_access_tokens(auth_credentials)
    return access_token.access_token


def request_access_token(exchange_name):
    auth_credentials = get_client_oauth_credentials(exchange_name)
    url = get_authorize_url(auth_credentials)
    oauth_client = get_oauth_clients(auth_credentials)
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(basic_auth=oauth_client.client_id+':'+oauth_client.client_secret)
    response = http.request('POST', url, fields={'grant_type': oauth_client.grant_types, 'access_lifetime': 7200},
                            headers=headers)
    print response.data
    store_auth_token(exchange_name, ast.literal_eval(response.data))


def read_collections(collection_name):
    return get_client_oauth_credentials('unocoin').to_json()


def write_collections(data):
    print data
    string_value = json.loads(json.dumps(data['data']))
    object_map = ast.literal_eval(string_value)
    # OauthCredentials.objects.from_json()
    OauthCredentials.objects.create(
        exchange=object_map['exchange'],
        oauth_token_url=object_map['oauth_token_url'],
        oauth_clients=object_map['oauth_clients'],
        oauth_scopes=object_map['oauth_scopes']
    )


def buy_bitcoin(rupees):
    pass


def sell_bitcoin(quantity):
    pass


def update_crypto_currency_rates(currency):
    # url = sources.bitcoin+currency
    # response = urllib.urlopen(url)
    # data = json.load(response)
    http = urllib3.PoolManager()
    response = http.request('POST', sources.rate_url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': 'Bearer '+get_oauth_access_token(sources.exchange)})
    # print response.data
    if response.data and response.data.__contains__('error'):
        print "Error : "+str(response.data)
        request_access_token(sources.exchange)
        update_crypto_currency_rates('inr')
    # PriceInfo.objects.create(
    #     buy = data['buy'],
    #     sell = data['sell'],
    #     currency = data['currency'],
    #     timestamp = datetime.datetime.utcnow()
    # )
    return response.data
