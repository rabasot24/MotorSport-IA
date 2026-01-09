from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# Tabla de Usuarios (Requisito PDF Sección 5)
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("user", "editor", "admin"), default="user")
    settings = db.Column(db.JSON, nullable=True)  # Para preferencias del perfil

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Tabla de Categorías (Requisito PDF Sección 5)
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    articles = db.relationship("Article", backref="category_rel", lazy=True)


# Tabla de Artículos/Noticias (Requisito PDF Sección 5)
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))  # Para tus fotos actuales
    date = db.Column(db.DateTime, server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))


# Tabla de Vehículos (Requisito PDF Sección 5)
# Tabla de Vehículos (ACTUALIZADA PARA FICHA TÉCNICA)
class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))

    # --- NUEVAS COLUMNAS TÉCNICAS ---
    # En vez de un JSON genérico, usamos columnas reales para poder ordenar y mostrar mejor
    engine = db.Column(db.String(100))  # Ej: V12 6.5L
    horsepower = db.Column(db.Integer)  # Ej: 800
    top_speed = db.Column(db.Integer)  # Ej: 350
    acceleration = db.Column(db.Float)  # Ej: 2.8
    weight = db.Column(db.Integer)  # Ej: 1250

    sounds = db.relationship("Sound", backref="vehicle", lazy=True)


# Tabla de Sonidos (Requisito PDF Sección 5)
class Sound(db.Model):
    __tablename__ = "sounds"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    title = db.Column(db.String(255))
    audio_path = db.Column(db.String(255))


# Tabla de Circuitos para el Quiz (Requisito PDF Sección 11)
class Circuit(db.Model):
    __tablename__ = "circuits"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50))
    image_path = db.Column(db.String(255))
    audio_path = db.Column(db.String(255))
