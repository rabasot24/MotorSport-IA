import os


class Config:
    # Clave secreta para seguridad (obligatorio según PDF sección 7)
    SECRET_KEY = "tu_clave_secreta_super_segura"
    # La base de datos se guardará en un archivo local 'motorsport.db'
    SQLALCHEMY_DATABASE_URI = "sqlite:///motorsport.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
