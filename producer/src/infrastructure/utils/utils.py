import secrets

def generate_share_token():
    return secrets.token_urlsafe(40)
