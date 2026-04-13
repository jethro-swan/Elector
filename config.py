import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') \
                 or "buHoFre$hVuwucF3jRamN3Dryfr0fuv9"
