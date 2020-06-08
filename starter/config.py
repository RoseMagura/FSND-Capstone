class TestConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost:5432/casting'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    