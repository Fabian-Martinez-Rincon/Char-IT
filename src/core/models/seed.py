filiales_data = [
    {
        "nombre": "Filial Buenos Aires",
        "direccion": "Av. Rivadavia 4163, Buenos Aires",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial La Plata",
        "direccion": "Calle 6 N° 988 entre 51 y 53, La Plata, Buenos Aires",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Ushuaia",
        "direccion": "Av. Maipú 870, Ushuaia, Tierra del Fuego",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Santa Rosa",
        "direccion": "Alvear 144, Santa Rosa, La Pampa",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Mar del Plata",
        "direccion": "San Lorenzo 2455, Mar del Plata, Buenos Aires",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Mendoza",
        "direccion": "Perú 1457, Mendoza",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Rosario",
        "direccion": "Buenos Aires 2056, Rosario, Santa Fe",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Córdoba",
        "direccion": "Obispo Trejo 108, Córdoba",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial San Juan",
        "direccion": "Mendoza 154, San Juan",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    {
        "nombre": "Filial Salta",
        "direccion": "España 132, Salta",
        "horarios": "8:00 a 16:00",
        "dias": "lunes a viernes",
        "telefono": ""
    },
    # Continúa con los otros lugares...
]


from src.core.models.database import db
from . import Filial  # Asegúrate de que la ruta de importación sea correcta

def seed_db():
    try:
        # Elimina filiales existentes para evitar duplicados
        db.session.query(Filial).delete()
        
        # Añade nuevas filiales
        for filial_data in filiales_data:
            filial = Filial(
                nombre=filial_data['nombre'],
                direccion=filial_data['direccion'],
                horarios=filial_data['horarios'],
                dias=filial_data['dias'],
                telefono=filial_data['telefono']
            )
            db.session.add(filial)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")


