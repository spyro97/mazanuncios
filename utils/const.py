#----------DB Data------------#
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = '1793'
DB_NAME = 'mazanuncios'
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


#----------JWT------------#
JWT_SECRET_KEY = "c07e154e8067407c909be11132e7d1bcee77542afd6c26ba613e2ffd9c3375ea"
JWT_ALGORITH = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5
JWT_EXPIRED_MSG = "Your JWT token is expired! Renew the JWT token!"
JWT_INVALID_MSG = "Invalid JWT token!"
TOKEN_INVALID_CREDENTIALS_MSG = "Invalid username, password match !"
JWT_WRONG_ROLE = "Unauthorized role!"
TOKEN_DESCRIPTION = (
    "It checks username and password if they are true, it returns JWT token to you."
)
TOKEN_SUMMARY = "It returns JWT token."


#----------Redis------------#
REDIS_URL = "redis://localhost"