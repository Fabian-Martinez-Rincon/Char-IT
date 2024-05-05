## Char-IT

- [Para Colaborar](#para-colaborar)
- [Iniciar el Proyecto](#iniciar-el-proyecto)
- [Rutas del admin](#rutas-del-admin)
- [Categorias](#categorias)

## Para Colaborar

- Para asegurarnos de que estamos en la rama main, antes de crear una mara
    ```bash
    git branch
    ```
- Si ya creamos una rama y queremos ir a esa, usamos
    ```bash
    git checkout {nombre-rama}
    ```
- Si no existe la rama, la creamos con un nombre descriptivo
    ```bash
    git branch {nombre-rama} o git checkout -b {nombre-rama}  //Para movernos despues de crearla
    ```
- Una vez que estamos en la rama, hacemos un pull para asegurarnos de que estamos actualizados
    ```bash
    git pull origin main
    ```
- Hacemos la pull request
    ```bash
    git add .
    git commit -m "Mensaje descriptivo"
    git push origin {nombre-rama}
    ```

---

## Iniciar el Proyecto

Descargamos la version de python

- [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)

#### Paso 1 Creamos el entorno Virtual
```bash
python -m venv .venv
```

#### Paso 2 Activamos el entorno
```bash
.venv\Scripts\activate
```

Dependiendo el idioma

```bash
.venv/Scripts/activate
```

En caso de no tener permisos
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

#### Instalamos las dependencias (Solo hace falta la primera vez)

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

#### Ejecutamos el proyecto en modo desarrollador

```bash
flask resetdb
flask seeddb
```

Se rompio el `livetw dev`, la solucion momentanea es hacer `flask run --debug` y `livetw dev --no-flask` en otra terminal

#### No hace falta

```bash
livetw init -d
livetw build
```

---

#### Para configurar las variables de entorno, copiamos y renombramos el archivo `.env.example` a `.env` y configuramos las variables de entorno.

```json
DB_PASS = "password_example"
```

---

## Rutas del admin

Listar filiales
```bash
http://url_local/
```

Listar usuarios generales
```bash
http://url_local/generales
```

Listar colaboradores
```bash
http://url_local/colaboradores
```

Listar publicaciones
```bash
http://url_local/publicaciones
```

---

## Categorias

- **Electrodomésticos** - Esenciales en cada hogar.
    - Refrigerador
    - Lavadora
    - Secadora
    - Microondas
    - Licuadora
    - Tostadora
    - Cafetera
    - Aspiradora
    - Aire acondicionado
    - Estufa eléctrica
- **Electrónica** - Muy demandada, especialmente dispositivos móviles y computadoras.
    - Smartphone
    - Tablet
    - Laptop
    - Cámara digital
    - Televisor
    - Altavoces Bluetooth
    - Consola de videojuegos
    - Smartwatch
    - Kindle
    - Drones
- **Muebles** - Importantes para aquellos que se mudan o renuevan su hogar.
    - Sofá
    - Mesa de comedor
    - Silla de escritorio
    - Librería
    - Cama
    - Mesita de noche
    - Escritorio
    - Armario
    - Sillón reclinable
    - Estantería
- **Herramientas** - Necesarias para mantenimiento del hogar y aficionados al bricolaje.
    - Taladro
    - Sierra circular
    - Martillo
    - Juego de destornilladores
    - Llave inglesa
    - Cinta métrica
    - Nivel
    - Alicates
    - Lijadora
    - Caja de herramientas
- **Ropa** - Alta rotación y demanda constante.
    - Jeans
    - Camiseta
    - Vestido
    - Chaqueta
    - Zapatos deportivos
    - Bufanda
    - Gorra
    - Suéter
    - Traje
    - Sandalias
- **Libros** - Popular entre estudiantes y aficionados a la lectura.
    - Novelas
    - Biografías
    - Libros de cocina
    - Libros de autoayuda
    - Diccionarios
    - Enciclopedias
    - Libros de ciencia ficción
    - Manga
    - Libros de historia
    - Poesía
- **Deportes** - Equipos y accesorios para una variedad de actividades físicas.
    - Balón de fútbol
    - Raqueta de tenis
    - Bicicleta
    - Patines
    - Equipo de natación
    - Ropa deportiva
    - Saco de boxeo
    - Pesas
    - Esterilla de yoga
    - Zapatillas de running
- **Juegos** - Para familias, niños y entusiastas de juegos de mesa y videojuegos.
    - Juegos de mesa
    - Cartas de póker
    - Rompecabezas
    - Juegos de video
    - Ajedrez
    - Dados
    - Juegos de rol
    - Juegos educativos para niños
    - Juegos de estrategia
    - Cubo de Rubik
- **Arte** - Artículos decorativos para el hogar.
    - Cuadros al óleo
    - Esculturas
    - Fotografías enmarcadas
    - Grabados
    - Arte digital impreso
    - Murales
    - Cerámica
    - Joyería artesanal
    - Tapices
    - Instalaciones artísticas




