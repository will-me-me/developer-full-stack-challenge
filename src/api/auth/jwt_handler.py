# this file is responsible for singing, enconding , decoding, and returning JWTS

from typing import Optional
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, Header, Request, Security

from base64 import decode
import time
import jwt
from decouple import config
# from db import db

JWT_SECRET= 'ec3ff9a38bcab75746634261b69fe71b5540130e33785e3f449f9d61626d3400'
JWT_ALGORITHM= 'HS256'


# If the request has an Authorization header, try to parse it as a Bearer token, and if that fails,
# return None.
class OptionalBearer():
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                return await HTTPBearer()(request)
            except:
                return 


security = HTTPBearer()

optional = OptionalBearer()


def sign_jwt(user_data: dict, expires=None):
    """
    It signs the JWT with the user payload and returns the token
    
    :param user_data: The user data dictionary
    :type user_data: dict
    :param expires: The expiration time of the token, defaults to None
    :type expires: [type], optional
    :return: The token
    """
    username = user_data.get('username')
    user_id = user_data.get('id')
    
    payload = {
        'username': username,
        'id': user_id,
        'expiry': expires or time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decodeJWT(token: str):
    """
    It decodes the token, checks if it's expired, and returns the payload
    
    :param token: The token to decode
    :type token: str
    :return: The payload of the token.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        raise ValueError("Invalid Token")
    if payload['expiry'] < time.time():
        raise ValueError("Token Expired")
    return payload


def jwt_dependecy(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    > If the user is authenticated, return the user object, otherwise raise an error
    
    :param credentials: HTTPAuthorizationCredentials = Security(security)
    :type credentials: HTTPAuthorizationCredentials
    :return: The user object
    """
    user = decodeJWT(credentials.credentials)
    if user:
        return user
    raise ValueError("Unauthorized: 401")


def jwt_optional(credentials: Optional[HTTPAuthorizationCredentials] = Security(optional)):
    """
    If the user is logged in, return the user object, otherwise return an empty object
    
    :param credentials: Optional[HTTPAuthorizationCredentials] = Security(optional)
    :type credentials: Optional[HTTPAuthorizationCredentials]
    :return: A dictionary with the user's information.
    """
    try:
        user = decodeJWT(credentials.credentials)
        return user or {}
    except:
        return {}
    

jwt_required = Depends(jwt_dependecy)