from mongoengine import Document, fields, EmbeddedDocument
import datetime


class PriceInfo(Document):
    buy = fields.LongField(required=True)
    sell = fields.LongField(required=True)
    currency = fields.StringField(required=True)
    timestamp = fields.DateTimeField(required=True)


class OauthClient(EmbeddedDocument):
    client_id = fields.StringField(primary_key=True)
    client_secret = fields.StringField()
    redirect_uri = fields.StringField()
    grant_types = fields.StringField()
    scope = fields.StringField()
    user_id = fields.StringField()


class OauthAccessToken(EmbeddedDocument):
    access_token = fields.StringField(primary_key=True)
    expires_in = fields.LongField()
    scope = fields.StringField()
    token_type = fields.StringField()


class OauthAuthorizationCodes(EmbeddedDocument):
    authorization_code = fields.StringField(primary_key=True)
    client_id = fields.StringField()
    user_id = fields.StringField()
    redirect_uri = fields.StringField()
    expires = fields.DateTimeField()
    scope = fields.StringField()
    id_token = fields.StringField()


class OauthRefreshToken(EmbeddedDocument):
    refresh_token = fields.StringField(primary_key=True)
    client_id = fields.StringField()
    user_id = fields.StringField()
    expires = fields.DateTimeField()
    scope = fields.StringField()


class OauthUsers(EmbeddedDocument):
    username = fields.StringField()
    password = fields.StringField()
    first_name = fields.StringField()
    last_name = fields.StringField()
    email = fields.StringField()
    email_verified = fields.BooleanField()
    scope = fields.StringField()


class OauthScopes(EmbeddedDocument):
    scope = fields.StringField(primary_key=True)
    is_default = fields.BooleanField()


class OauthJwt(EmbeddedDocument):
    client_id = fields.StringField()
    subject = fields.StringField()
    public_key = fields.StringField()


class OauthCredentials(Document):
    exchange = fields.StringField(primary_key=True)
    oauth_token_url = fields.StringField(required=True)
    oauth_client = fields.EmbeddedDocumentField(OauthClient)
    oauth_access_token = fields.EmbeddedDocumentField(OauthAccessToken)
    oauth_authorization_codes = fields.EmbeddedDocumentListField(OauthAuthorizationCodes)
    oauth_refresh_token = fields.EmbeddedDocumentField(OauthRefreshToken)
    oauth_users = fields.EmbeddedDocumentListField(OauthUsers)
    oauth_scopes = fields.EmbeddedDocumentListField(OauthScopes)
    oauth_jwt = fields.EmbeddedDocumentListField(OauthJwt)


class Info(EmbeddedDocument):
    quantity = fields.LongField()
    buy_or_sell_rate = fields.LongField()
    buy_rate = fields.LongField()
    sell_rate = fields.LongField()


class History(EmbeddedDocument):
    date = fields.DateTimeField(default=datetime.datetime.utcnow().isoformat())
    action = fields.StringField()
    info = fields.EmbeddedDocumentField(Info)


class Expenses(EmbeddedDocument):
    buy_fee = fields.FloatField(default=0.012)
    sell_fee = fields.FloatField(default=0.012)


class TransactionInfo(Document):
    history = fields.EmbeddedDocumentListField(History)
    expenses = fields.EmbeddedDocumentField(Expenses)

