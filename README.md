# Enriquecimiento de transacciones

## Instalación

⚠️ Este proyecto se encuentra privado, por lo que es necesario que se otorgue
acceso antes de su instalación.

Crea el archivo de variables de entorno con nombre `.env` y las siguiente variables.

```text
DATABASE_NAME=getxerpa
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

SECRET_KEY=soy-una-super-secret-key

ALLOWED_HOSTS=getxerpa.localhost
```

Instalación de dependencias:

```sh
poetry install
```

Configura el host para este servicio agregando al archivo `/etc/hosts` lo siguiente:

```text
127.0.0.1 getxerpa.localhost
```

Para facilitar el desarrollo puedes usar postgres con el docker-compose
disponible en el proyecto:

```sh
docker-compose pull
docker-compose up -d
```

Cargar fixtures:

```sh
python manage.py loaddata transactions.json
python manage.py loaddata categorytypes.json
python manage.py loaddata categories.json
python manage.py loaddata merchants.json
python manage.py loaddata keywords.json
```

## Ejemplo de uso

Enriquecer un listado de transacciones:

```sh
curl -X 'POST' \
  'http://getxerpa.localhost:8000/api/api/transactions/bulk-create/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "id": "3fa66f64-5717-4562-b3fc-2c963f66afa6",
    "description": "Uber",
    "amount": 0,
    "date": "2023-12-29"
  },
  {
    "id": "2eb006b8-d970-4c66-acb6-70e0ebff5cf5",
    "description": "Uber Eats",
    "amount": 0,
    "date": "2023-12-29"
  }
]'
```

Respuesta:

```json
{
  "count": 2,
  "category_enrichment": 2,
  "merchant_enrichment": 2,
  "transactions": [
    {
      "id": "3fa66f64-5717-4562-b3fc-2c963f66afa6",
      "enrichment": {
        "merchant_id": "424b4f71-d3b9-4865-84ec-b32052df1333",
        "category_id": "d3a36995-2900-4bf0-b1c3-8fc186b057c6"
      },
      "description": "Uber",
      "amount": 0,
      "date": "2023-12-29"
    },
    {
      "id": "2eb006b8-d970-4c66-acb6-70e0ebff5cf5",
      "enrichment": {
        "merchant_id": "f9b21d31-c9b7-4891-a380-ede2c12cb1f9",
        "category_id": "0a634e46-79fb-4bd1-a0f7-0fda27076a1a"
      },
      "description": "Uber Eats",
      "amount": 0,
      "date": "2023-12-29"
    }
  ]
}
```

## Desarrollo

### Tecnologías utilizadas

- **Poetry**: gestor de dependencias para Python
- **Django**: framework para la creación aplicaciones web
- **Django Rest Framework**: librería para crear APIs Rest
- **markdownlint-cli2**: librería para análisis estático de archivos markdown

### Diseño

Se desarrolló una api rest utilizando Django debido a la robustes en la
construcción de APIs y las librerías disponibles facilitando el uso de la
base de datos, organización e integración con Celery.

![image](https://github.com/SaulHormazabal/getxerpa/assets/1095706/5b27a7a0-2d86-40ea-bffd-831a49fee36a)

### Modelo de datos

Para facilitar el cálculo de estadística se relegó la tarea a la base de datos
utilizando una vista, favoreciendo la integridad de los datos y un mayor rendimiento.

![image](https://github.com/SaulHormazabal/getxerpa/assets/1095706/8c5be283-d4d8-4e9b-931c-02ddef5aa5bc)

### Componentes

![image](https://github.com/SaulHormazabal/getxerpa/assets/1095706/42c70946-ea8a-4ae3-ab47-98c92710b6f2)

### Enriquecimiento

El enriquecimiento se realiza dentro de una vista de Postgres en donde se buscar
keyword dentro de la descripción de las transacciones.

Para el caso en que una descripción de transacción tenga más de una keyword será
el peso el que determine cual tiene mayor relevancia.

### Integración continua

El proyecto tiene configurado un proceso de integración continua usando GitHub
Actions donde se evalúa lo siguiente:

- Tests: pruebas para asegurar el correcto funcionamiento ante modificaciones
en el código fuente
- Análisis estático de markdown: permite mantener un formato consistente
favoreciendo un estilo de escritura fácil de leer sin un visualizador
- Análisis estático de código Python: Se utiliza Flake8 y PyLint
- Cobertura: se debe mantener un mínimo de cobertura del 90%
