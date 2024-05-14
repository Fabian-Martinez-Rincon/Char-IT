from werkzeug.security import generate_password_hash
import json

# Lista de usuarios en formato JSON como string
usuarios_json = '''
[
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "password": "contrageneral", 
        "email": "usuario.general@gmail.com",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455",
        "id_rol": 1  
    },
    {
        "nombre": "María",
        "apellido": "González",
        "password": "contrageneral2",
        "email": "usuario.general2@gmail.com",
        "dni": "87654321",
        "fecha_nacimiento": "1985-08-15",
        "telefono": "5566778899",
        "id_rol": 1
    },
    {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "password": "contrageneral3",
        "email": "usuario.general3@gmail.com",
        "dni": "34567890",
        "fecha_nacimiento": "1992-07-10",
        "telefono": "3344556677",
        "id_rol": 1
    },
    {
    "nombre": "Luis",
    "apellido": "Martinez",
    "password": "contracolaborador",
    "email": "usuario.colaborador@gmail.com",
    "dni": "45678901",
    "fecha_nacimiento": "1988-09-12",
    "telefono": "4455667788",
    "id_rol": 2
},
{
    "nombre": "Sofia",
    "apellido": "Fernandez",
    "password": "contracolaborador2",
    "email": "usuario.colaborador2@gmail.com",
    "dni": "56789012",
    "fecha_nacimiento": "1993-10-15",
    "telefono": "5566778899",
    "id_rol": 2
},
{
    "nombre": "Pedro",
    "apellido": "Garcia",
    "password": "contraowner",
    "email": "usuario.owner@gmail.com",
    "dni": "67890123",
    "fecha_nacimiento": "1990-11-20",
    "telefono": "6677889900",
    "id_rol": 3
}
]
'''

# Convertir el string JSON a una estructura de datos de Python
usuarios = json.loads(usuarios_json)

# Hashear las contraseñas de cada usuario
for usuario in usuarios:
    usuario['password'] = generate_password_hash(usuario['password'], method='pbkdf2:sha256')

# Imprimir los usuarios con las contraseñas hasheadas
print(json.dumps(usuarios, indent=4))
