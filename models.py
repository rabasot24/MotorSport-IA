from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


# Tabla de Usuarios
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("user", "editor", "admin"), default="user")
    settings = db.Column(db.JSON, nullable=True)
    score = db.Column(db.Integer, default=0)

    # RELACIÓN: Un usuario tiene muchos comentarios
    comments = db.relationship("Comment", backref="author_rel", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Tabla de Categorías
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    articles = db.relationship("Article", backref="category_rel", lazy=True)


# Tabla de Artículos/Noticias
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    # --- ESTA LÍNEA ES LA QUE FALTA PARA QUE SE VEAN ---
    comments = db.relationship(
        "Comment", backref="article_rel", lazy=True, cascade="all, delete-orphan"
    )


# Tabla de Vehículos
class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    engine = db.Column(db.String(100))
    horsepower = db.Column(db.Integer)
    top_speed = db.Column(db.Integer)
    acceleration = db.Column(db.Float)
    weight = db.Column(db.Integer)
    sounds = db.relationship("Sound", backref="vehicle", lazy=True)


# Tabla de Sonidos
class Sound(db.Model):
    __tablename__ = "sounds"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    title = db.Column(db.String(255))
    audio_path = db.Column(db.String(255))


# Tabla de Circuitos
class Circuit(db.Model):
    __tablename__ = "circuit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    image = db.Column(db.String(200))
    audio = db.Column(db.String(200))


# Tabla de Comentarios
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
