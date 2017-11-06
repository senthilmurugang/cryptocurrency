from mongoengine import Document, fields, EmbeddedDocument


class PriceInfo(Document):
    buy = fields.LongField(required=True)
    sell = fields.LongField(required=True)
    currency = fields.StringField(required=True)
    timestamp = fields.DateTimeField(required=True)


class OauthClients(EmbeddedDocument):
    client_id = fields.StringField(primary_key=True)
    client_secret = fields.StringField()
    redirect_uri = fields.StringField()
    grant_types = fields.StringField()
    scope = fields.StringField()
    user_id = fields.StringField()


class OauthAccessTokens(EmbeddedDocument):
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


class OauthRefreshTokens(EmbeddedDocument):
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
    oauth_clients = fields.EmbeddedDocumentField(OauthClients)
    oauth_access_tokens = fields.EmbeddedDocumentField(OauthAccessTokens)
    oauth_authorization_codes = fields.EmbeddedDocumentField(OauthAuthorizationCodes)
    oauth_refresh_tokens = fields.EmbeddedDocumentField(OauthRefreshTokens)
    oauth_users = fields.EmbeddedDocumentField(OauthUsers)
    oauth_scopes = fields.EmbeddedDocumentField(OauthScopes)
    oauth_jwt = fields.EmbeddedDocumentField(OauthJwt)

