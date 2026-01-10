from app import app, db
from models import User


def crear_administrador():
    with app.app_context():
        # 1. Comprobar si ya existe
        admin = User.query.filter_by(email="admin@motorsport.com").first()

        if admin:
            print("⚠️ El usuario 'admin@motorsport.com' ya existe.")
            # Si quieres, le cambiamos la contraseña para asegurarnos
            admin.set_password("1234")
            print("🔄 Contraseña restablecida a: 1234")
        else:
            # 2. Si no existe, lo creamos
            print("👤 Creando nuevo Super-Admin...")
            nuevo_admin = User(
                username="Admin",
                email="admin@motorsport.com",
                role="admin",  # Asegúrate de que tu modelo tiene este campo
            )
            nuevo_admin.set_password("1234")
            db.session.add(nuevo_admin)
            print("✅ Usuario creado con éxito.")

        db.session.commit()
        print("\n🚀 LISTO: Entra con:")
        print("   Email: admin@motorsport.com")
        print("   Pass:  1234")


if __name__ == "__main__":
    crear_administrador()
