# proyecto-final-fidi-db
Proyecto Final FiDi Database

## Diagrama de base de datos
```
https://app.quickdatabasediagrams.com/#/d/3G2nHC
```

## Librerias instaladas para el Backend. (contenidas en el Pipfile)
- python-dotenv
- flask-sqlalchemy
- psycopg2-binary
- flask
- flask-migrate
- flask-jwt-extended
- flask-cors
- cloudinary

### configuracion archivo .env
  ```
  DATABASEURI="postgresql+psycopg2://postgres:postgres@localhost:5432/dbfidi"
  JWT_SECRET="f400ca7c5ef4d9dfbc31c58898cc40aa"
  ```

### comandos a ejecutar
- flask db init // solamente la primera vez o si se elimina la carpeta migracion
- flask db migrate // crea migraciones
- flask db upgrade // lleva las migracion a la BD