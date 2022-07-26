import datetime
from pathlib import Path

from pydantic import BaseSettings

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent, '.env')
        env_file_encoding = 'utf-8'


class PostgresSettings(BaseConfig):
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: str = '5432'

    @property
    def uri(self):
        return f'postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    @property
    def dsl(self):
        return {
            'dbname': self.DB,
            'user': self.USER,
            'password': self.PASSWORD,
            'host': self.HOST,
            'port': self.PORT,
        }

    class Config:
        env_prefix = 'PG_'


class ElasticSettings(BaseConfig):
    HOST: str
    PORT: str = '9200'
    INDEX: dict = {'films': 'movies', 'persons': 'persons', 'genres': 'genres'}
    INDEX_FILES: dict[str, Path] = {
        'films': Path(Path(__file__).parent, 'index_scheme/films_schema.json'),
        'persons': Path(Path(__file__).parent, 'index_scheme/persons_schema.json'),
        'genres': Path(Path(__file__).parent, 'index_scheme/genres_schema.json'),
    }

    class Config:
        env_prefix = 'ES_'

    @property
    def hosts(self):
        return [{'host': self.HOST, 'port': self.PORT}]


class ProjectSettings(BaseConfig):
    DEFAULT_PROCESS_TIME: datetime.datetime = datetime.datetime(2010, 1, 1)
    LOG_CONFIG: dict = LOGGING_CONFIG
    SECRET: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'

    postgres: PostgresSettings = PostgresSettings()
    elastic: ElasticSettings = ElasticSettings()
    FAST_APU_URL: str = 'http://fastapi:8000'


settings = ProjectSettings()
