## Char-IT

<details><summary>Para colaborar</summary>

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

</details>

<details><summary>Para colaborar</summary>

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

#### No hace falta

```bash
livetw init -d
livetw build
```

</details>

### Comandos de configuración (Opcional)

```bash
flask resetdb
flask seeddb
```

Para correr la aplicación

```bash
livetw dev
```

o los siguientes dos
```bash
flask run --debug
livetw dev --no-flask
```

#### Para configurar las variables de entorno, copiamos y renombramos el archivo `.env.example` a `.env` y configuramos las variables de entorno.

```json
DB_PASS = "password_example"
DB_USER = "user_example"
DB_NAME = "database_example"
DB_HOST = "host_example"
```

---

#### Rutas para la primera demo

- `/eliminar_publicaciones`
- `/eliminar_colaboradores`
- `/eliminar_generales`