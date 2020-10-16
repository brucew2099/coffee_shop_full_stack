import dotenv
from os.path import abspath, dirname, join

project_dir = dirname(abspath(__file__))

DOTENV_PATH = join(project_dir, '.env')

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    join(project_dir, dotenv.get_key(DOTENV_PATH, 'DATABASE_FILENAME')))
