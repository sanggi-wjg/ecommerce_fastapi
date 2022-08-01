import os.path
from functools import lru_cache
from os import path

from pydantic import BaseSettings

base = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


class Settings(BaseSettings):
    base_root: str = base

    debug: bool = True
    reload: bool = True
    port: int = 9002

    mail_from: str
    mail_password: str

    secret_key: str
    access_token_algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = os.path.join(base, ".env")

    @property
    def template_root(self):
        return os.path.join(self.base_root, "templates")

    @property
    def media_root(self):
        return os.path.join(self.base_root, "media")

    @property
    def user_profile_root(self):
        path = os.path.join(self.media_root, 'profile')
        if not os.path.exists(path):
            os.mkdir(path)
        return path


@lru_cache()
def get_settings():
    return Settings()
