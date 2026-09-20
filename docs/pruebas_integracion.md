# Informe de pruebas de integración - blacklist_email

## 1. Objetivo

Crear y ejecutar una colección de Postman para validar las capacidades principales del servicio `blacklist_email`, ejecutar dicha colección de manera local mediante Newman y automatizar las pruebas mediante GitHub Actions.

## 2. Servicio evaluado

El proyecto corresponde a un servicio desarrollado con Flask, SQLAlchemy y PostgreSQL, ejecutado mediante Docker Compose.

La aplicación se encuentra disponible localmente en:

```text
http://localhost:5001
```

## 3. Capacidades probadas

La colección de Postman contiene las siguientes pruebas:

| Prueba              | Método | Endpoint              | Resultado esperado |
| ------------------- | ------ | --------------------- | ------------------ |
| Health Check        | GET    | `/blacklists/ping`    | HTTP 200           |
| Crear Blacklist     | POST   | `/blacklists`         | HTTP 201           |
| Consultar Blacklist | GET    | `/blacklists/<email>` | HTTP 200           |

Las operaciones que requieren autenticación utilizan un token Bearer.

## 4. Creación de la colección en Postman

Se creó una colección de Postman denominada:

```text
blacklist_email
```

La colección utiliza las siguientes variables:

* `RUTA_BASE`: URL base del servicio.
* `TOKEN`: token utilizado para la autenticación.
* `TEST_EMAIL`: correo utilizado durante las pruebas.

Para evitar conflictos con registros existentes en la base de datos, el correo de prueba se genera dinámicamente antes de ejecutar la petición de creación.

Ejemplo:

```text
newman-<timestamp>@example.com
```

De esta manera, cada ejecución utiliza un correo diferente.

## 5. Pruebas incluidas en la colección

### 5.1 Health Check

Se realiza una petición:

```http
GET /blacklists/ping
```

Esta prueba no requiere autenticación.

Se valida que:

* La respuesta tenga código HTTP `200`.
* La respuesta contenga el mensaje `pong`.

### 5.2 Crear Blacklist

Se realiza una petición:

```http
POST /blacklists
```

La petición utiliza autenticación Bearer y envía información en formato JSON.

Ejemplo del cuerpo utilizado:

```json
{
    "email": "{{TEST_EMAIL}}",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "blocked_reason": "Prueba de integración Newman"
}
```

Se valida que la respuesta tenga código HTTP:

```text
201 CREATED
```

### 5.3 Consultar Blacklist

Se realiza una petición:

```http
GET /blacklists/{{TEST_EMAIL}}
```

También utiliza autenticación Bearer.

Se valida que:

* La respuesta tenga código HTTP `200`.
* El correo consultado se encuentre registrado en la blacklist.

## 6. Exportación de la colección

La colección fue exportada desde Postman en formato JSON.

El archivo generado es:

```text
blacklist_email.postman_collection.json
```

Este archivo se encuentra en la raíz del proyecto y permite ejecutar las pruebas mediante Newman sin necesidad de abrir Postman.

## 7. Instalación de Newman

Para ejecutar la colección desde la terminal se instaló Newman de manera global mediante npm:

```bash
npm install -g newman
```

La versión utilizada fue:

```text
Newman 6.2.2
```

## 8. Ejecución local con Newman

Con la aplicación ejecutándose mediante Docker Compose, se ejecutó la colección utilizando:

```bash
newman run ./blacklist_email.postman_collection.json \
  --env-var "RUTA_BASE=http://localhost:5001" \
  --env-var "TOKEN=<token configurado>"
```

El parámetro `RUTA_BASE` permite indicar la dirección donde se encuentra ejecutándose la API.

El parámetro `TOKEN` proporciona el token necesario para realizar las operaciones protegidas.

## 9. Resultado de la ejecución local

La colección se ejecutó correctamente mediante Newman.

Resultado obtenido:

```text
iterations 1
failed 0

requests 3
failed 0

test-scripts 3
failed 0

prerequest-scripts 1
failed 0

assertions 5
failed 0
```

Las tres solicitudes fueron ejecutadas correctamente:

| Prueba              | Resultado     |
| ------------------- | ------------- |
| Health Check        | `200 OK`      |
| Crear Blacklist     | `201 CREATED` |
| Consultar Blacklist | `200 OK`      |

Además, se ejecutaron cinco assertions y ninguna presentó errores.

## 10. Automatización con GitHub Actions

Para automatizar las pruebas se creó el workflow:

```text
.github/workflows/pruebas_integracion.yml
```

El workflow contiene un job denominado:

```text
pruebas_integracion
```

El workflow se configuró para ejecutarse cuando se realiza un `push` o un `pull request` sobre la rama `main`.

## 11. Funcionamiento del workflow

El proceso automatizado realiza las siguientes actividades:

1. Descarga el repositorio mediante `actions/checkout`.
2. Configura Node.js.
3. Instala Newman mediante npm.
4. Crea temporalmente el archivo `.env`.
5. Levanta la aplicación y la base de datos mediante Docker Compose.
6. Espera hasta que la API esté disponible.
7. Ejecuta la colección de Postman mediante Newman.
8. Muestra los logs de Docker si ocurre algún error.
9. Detiene los servicios al finalizar las pruebas.

## 12. Configuración del secreto de GitHub

Para evitar almacenar directamente el token de autenticación dentro del código fuente, se configuró un secreto de GitHub denominado:

```text
BEARER_TOKEN
```

Este secreto es utilizado por el workflow para:

* Configurar la variable `BEARER_TOKEN` de la aplicación.
* Proporcionar el token a Newman durante la ejecución de la colección.

El valor del token no se almacena directamente en el repositorio.

## 13. Ejecución en GitHub Actions

El workflow `pruebas_integracion` se ejecutó correctamente en GitHub Actions.

Resultado:

```text
succeeded
```

La ejecución completa tuvo una duración aproximada de:

```text
47 segundos
```

Durante la ejecución se levantaron correctamente:

* La aplicación Flask mediante Gunicorn.
* La base de datos PostgreSQL.
* El entorno Docker Compose.

## 14. Resultado de las pruebas en GitHub Actions

Newman ejecutó la colección dentro del workflow y obtuvo los siguientes resultados:

```text
iterations                1
failed                    0

requests                  3
failed                    0

test-scripts              3
failed                    0

prerequest-scripts        1
failed                    0

assertions                5
failed                    0
```

Las pruebas realizadas fueron:

| Prueba              | Resultado     |
| ------------------- | ------------- |
| Health Check        | `200 OK`      |
| Crear Blacklist     | `201 CREATED` |
| Consultar Blacklist | `200 OK`      |

Resultado general:

```text
3 solicitudes ejecutadas
0 solicitudes fallidas
5 assertions ejecutadas
0 assertions fallidas
```

## 15. Repositorio

El código fuente, la colección de Postman, el workflow de GitHub Actions y el informe se encuentran disponibles en el siguiente repositorio:

https://github.com/jalith19/blacklits-clase

También se puede consultar directamente la ejecución del workflow `pruebas_integracion` desde la sección Actions del repositorio.

## 16. Estructura relevante del proyecto

La estructura relacionada con la actividad quedó organizada de la siguiente manera:

```text
blacklist_app/
│
├── .github/
│   └── workflows/
│       └── pruebas_integracion.yml
│
├── docs/
│   └── pruebas_integracion.md
│
├── blacklist_email.postman_collection.json
│
├── Dockerfile
│
├── docker-compose.yml
│
└── ...
```

## 17. Cambios realizados

Para cumplir con la actividad se realizaron los siguientes cambios:

* Creación de la colección `blacklist_email` en Postman.
* Exportación de la colección en formato JSON.
* Configuración de variables para la URL, token y correo de prueba.
* Implementación de pruebas automáticas dentro de la colección.
* Generación dinámica del correo utilizado durante las pruebas.
* Instalación y ejecución local de Newman.
* Verificación de tres endpoints del servicio.
* Creación del workflow de GitHub Actions.
* Creación del job `pruebas_integracion`.
* Instalación automática de Newman dentro de GitHub Actions.
* Levantamiento de Flask y PostgreSQL mediante Docker Compose.
* Ejecución automática de la colección mediante Newman.
* Configuración del secreto `BEARER_TOKEN` en GitHub.
* Modificación del `Dockerfile` para ejecutar Gunicorn con un único worker.
* Creación de la carpeta `/docs`.
* Creación del informe en formato Markdown.

## 18. Evidencias obtenidas

Durante el desarrollo de la actividad se obtuvieron las siguientes evidencias:

### Ejecución local

Newman ejecutó correctamente:

```text
3 requests
0 failed

5 assertions
0 failed
```

### Ejecución automática

GitHub Actions ejecutó correctamente el job:

```text
pruebas_integracion
```

con estado:

```text
succeeded
```

La ejecución tuvo una duración aproximada de 47 segundos.

### Repositorio

El proyecto se encuentra publicado en GitHub:

https://github.com/jalith19/blacklits-clase

## 19. Conclusión

Se creó una colección de Postman para validar las principales capacidades del servicio `blacklist_email`.

La colección fue exportada correctamente a formato JSON y posteriormente ejecutada de manera local mediante Newman, obteniendo tres solicitudes exitosas y cinco assertions exitosas.

Posteriormente, se creó el workflow `pruebas_integracion` en GitHub Actions para automatizar las pruebas de integración. El workflow instala Newman, configura las variables necesarias, levanta la aplicación Flask y PostgreSQL mediante Docker Compose y ejecuta automáticamente la colección.

La ejecución del workflow finalizó correctamente, obteniendo cero solicitudes fallidas y cero assertions fallidas.

Con esto se logró automatizar el proceso de pruebas de integración del servicio y dejar documentado el procedimiento realizado dentro de la carpeta `/docs` en formato Markdown.
