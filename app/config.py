class DevelopmentConfig:
    DEBUG = True

class ProductionConfig:
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
