## Char-IT

- [Para Colaborar](#para-colaborar)
- [Iniciar el Proyecto](#iniciar-el-proyecto)

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
    git branch {nombre-rama}
    ```
- Una vez que estamos en la rama, hacemos un pull para asegurarnos de que estamos actualizados
    ```bash
    git pull
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
livetw dev
```

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