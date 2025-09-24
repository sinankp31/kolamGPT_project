import os

class Config:
    """Base configuration class with settings common to all environments."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_default_key')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GEMINI_MODEL_NAME = os.environ.get('GEMINI_MODEL_NAME', 'gemini-1.5-flash')
    KOLAM_GPT_SYSTEM_PROMPT = os.environ.get('KOLAM_GPT_SYSTEM_PROMPT', 'You are KolamGPT, an expert on the traditional South Indian art of kolam. Provide helpful, accurate information about kolam patterns, techniques, cultural significance, and related topics.')

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    CONTACT_RECIPIENT = os.environ.get('CONTACT_RECIPIENT', MAIL_USERNAME)

    @staticmethod
    def init_app(app):
        # This method can be used for app-specific initialization
        pass

class DevelopmentConfig(Config):
    """Configuration settings for development."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration settings for production."""
    DEBUG = False
    # Add any production-specific settings here, e.g., database URIs

# A dictionary to easily access the configuration classes by name
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}