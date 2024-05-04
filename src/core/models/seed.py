filiales_data = [
    {
        "nombre": "Filial Buenos Aires",
        "direccion": "Av. Rivadavia 4163, Buenos Aires",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "315-248-7745"
    },
    {
        "nombre": "Filial La Plata",
        "direccion": "Calle 6 N° 988 entre 51 y 53, La Plata, Buenos Aires",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "403-562-8973"
    },
    {
        "nombre": "Filial Ushuaia",
        "direccion": "Av. Maipú 870, Ushuaia, Tierra del Fuego",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "540-689-1224"
    },
    {
        "nombre": "Filial Santa Rosa",
        "direccion": "Alvear 144, Santa Rosa, La Pampa",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "760-834-2985"
    },
    {
        "nombre": "Filial Mar del Plata",
        "direccion": "San Lorenzo 2455, Mar del Plata, Buenos Aires",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "601-215-4038"
    },
    {
        "nombre": "Filial Mendoza",
        "direccion": "Perú 1457, Mendoza",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "802-431-5510"
    },
    {
        "nombre": "Filial Rosario",
        "direccion": "Buenos Aires 2056, Rosario, Santa Fe",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "209-666-7894"
    },
    {
        "nombre": "Filial Córdoba",
        "direccion": "Obispo Trejo 108, Córdoba",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "423-884-7523"
    },
    {
        "nombre": "Filial San Juan",
        "direccion": "Mendoza 154, San Juan",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "952-546-1234"
    },
    {
        "nombre": "Filial Salta",
        "direccion": "España 132, Salta",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": "508-335-6789"
    },
]

from datetime import datetime

usuarios_data = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "password": "securepassword", 
        "email": "juan.perez@example.com",
        "dni": "12345678",
        "fecha_nacimiento": datetime(1990, 5, 24),
        "telefono": "1122334455",
        "id_rol": 1  
    },
    {
        "nombre": "María",
        "apellido": "González",
        "password": "anothersecurepassword",
        "email": "maria.gonzalez@example.com",
        "dni": "87654321",
        "fecha_nacimiento": datetime(1985, 8, 15),
        "telefono": "5566778899",
        "id_rol": 2
    },
    {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "password": "password1234",
        "email": "carlos.rodriguez@example.com",
        "dni": "34567890",
        "fecha_nacimiento": datetime(1992, 7, 10),
        "telefono": "3344556677",
        "id_rol": 3
    }
]

roles_data = [
    {"nombre": "Visitante"},
    {"nombre": "General"},
    {"nombre": "Colaborador"},
    {"nombre": "Owner"}
]

from src.core.models.database import db
from src.core.models.filial import Filial 
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol 

def agregar_filiales():
    db.session.query(Filial).delete()
    for filial_data in filiales_data:
        filial = Filial(
                nombre=filial_data['nombre'],
                direccion=filial_data['direccion'],
                horarios=filial_data['horarios'],
                dias=filial_data['dias'],
                telefono=filial_data['telefono']
            )
        db.session.add(filial)
        
def agregar_usuarios():
    db.session.query(Usuario).delete()
    for usuario_data in usuarios_data:
        usuario = Usuario(
            nombre=usuario_data['nombre'],
            apellido=usuario_data['apellido'],
            password=usuario_data['password'],
            email=usuario_data['email'],
            dni=usuario_data['dni'],
            fecha_nacimiento=usuario_data['fecha_nacimiento'],
            telefono=usuario_data['telefono'],
            id_rol=usuario_data['id_rol']
        )
        db.session.add(usuario)
    db.session.commit()
    
def agregar_roles():
    db.session.query(Rol).delete() 
    for rol_data in roles_data:
        rol = Rol(nombre=rol_data['nombre'])
        db.session.add(rol)
    db.session.commit()

def seed_db():
    try:
        agregar_filiales()
        agregar_roles()
        agregar_usuarios()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")

from datetime import datetime

usuarios_data = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "password": "securepassword", 
        "email": "juan.perez@example.com",
        "dni": "12345678",
        "fecha_nacimiento": datetime(1990, 5, 24),
        "telefono": "1122334455",
        "id_rol": 1  
    },
    {
        "nombre": "María",
        "apellido": "González",
        "password": "anothersecurepassword",
        "email": "maria.gonzalez@example.com",
        "dni": "87654321",
        "fecha_nacimiento": datetime(1985, 8, 15),
        "telefono": "5566778899",
        "id_rol": 2
    },
    {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "password": "password1234",
        "email": "carlos.rodriguez@example.com",
        "dni": "34567890",
        "fecha_nacimiento": datetime(1992, 7, 10),
        "telefono": "3344556677",
        "id_rol": 3
    },
    {
    "nombre": "Luis",
    "apellido": "Martinez",
    "password": "password5678",
    "email": "luis.martinez@example.com",
    "dni": "45678901",
    "fecha_nacimiento": datetime(1988, 9, 12),
    "telefono": "4455667788",
    "id_rol": 2
},
{
    "nombre": "Sofia",
    "apellido": "Fernandez",
    "password": "sofiapassword",
    "email": "sofia.fernandez@example.com",
    "dni": "56789012",
    "fecha_nacimiento": datetime(1993, 10, 15),
    "telefono": "5566778899",
    "id_rol": 2
},
{
    "nombre": "Pedro",
    "apellido": "Garcia",
    "password": "pedropassword",
    "email": "pedro.garcia@example.com",
    "dni": "67890123",
    "fecha_nacimiento": datetime(1990, 11, 20),
    "telefono": "6677889900",
    "id_rol": 3
}
]

roles_data = [
    {"nombre": "Visitante"},
    {"nombre": "General"},
    {"nombre": "Colaborador"},
    {"nombre": "Owner"}
]

from src.core.models.database import db
from src.core.models.filial import Filial 
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol 

def agregar_filiales():
    db.session.query(Filial).delete()
    for filial_data in filiales_data:
        filial = Filial(
                nombre=filial_data['nombre'],
                direccion=filial_data['direccion'],
                horarios=filial_data['horarios'],
                dias=filial_data['dias'],
                telefono=filial_data['telefono']
            )
        db.session.add(filial)
        
def agregar_usuarios():
    db.session.query(Usuario).delete()
    for usuario_data in usuarios_data:
        usuario = Usuario(
            nombre=usuario_data['nombre'],
            apellido=usuario_data['apellido'],
            password=usuario_data['password'],
            email=usuario_data['email'],
            dni=usuario_data['dni'],
            fecha_nacimiento=usuario_data['fecha_nacimiento'],
            telefono=usuario_data['telefono'],
            id_rol=usuario_data['id_rol']
        )
        db.session.add(usuario)
    db.session.commit()
    
def agregar_roles():
    db.session.query(Rol).delete() 
    for rol_data in roles_data:
        rol = Rol(nombre=rol_data['nombre'])
        db.session.add(rol)
    db.session.commit()

def seed_db():
    try:
        agregar_filiales()
        agregar_roles()
        agregar_usuarios()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")
