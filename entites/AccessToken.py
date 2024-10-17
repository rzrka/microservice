import secrets

class AccessToken:

    def __init__(self, token: str = None):
        self.token = token
        self.expire_second = 86400

    def __repr__(self):
        return self.token

    def get_access_token(self):
        return {
            "access_token": self.token,
            "token_type": "bearer",
        }

    def generate_token(self):
        self.token = secrets.token_urlsafe(32)
        return self

