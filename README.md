# Analizador de URLs con FastAPI, SQLite y Docker

Este proyecto implementa una API REST para analizar URLs, guardar sus resultados en una base de datos SQLite y consultarlos luego desde una interfaz web. Es ideal para testear seguridad, certificados, headers y redirecciones de cualquier sitio. Fue desarrollado para ser desplegado en contenedores Docker y operado desde Portainer.

---

## Características principales

* Análisis de cualquier URL (HTTP/HTTPS):

  * Obtención de IP
  * Código de estado (status code)
  * Redirecciones
  * Headers HTTP
  * Certificado SSL (validez, sujeto, emisor)
* Persistencia en SQLite mediante SQLAlchemy.
* API REST construida con **FastAPI**.
* UI interactiva via **Swagger** en `/docs`.
* Consulta y administración de datos desde interfaz web (sqlite-web).
* Totalmente dockerizado y funcional desde Portainer.

---

## Endpoints disponibles

* `POST /analizar`

  * Cuerpo JSON:

    ```json
    {
      "url": "https://www.google.com"
    }
    ```
  * Resultado: guarda los datos del análisis en la base y devuelve un mensaje confirmando la operación.

---

## Modelo de datos

El modelo sigue una estructura relacional normalizada. Ver imagen `ERD.png` incluida:

* `sitios`: tabla principal con los resultados generales del análisis.
* `headers`: headers HTTP asociados a cada sitio.
* `certificados`: información del certificado SSL.
* `cert_sujetos`: sujeto del certificado.
* `cert_emisores`: emisor del certificado.

---

## Requisitos locales (solo para desarrollo)

* Python >= 3.10
* SQLite3

Instalación:

```bash
pip install -r requirements.txt
```

Ejecución:

```bash
uvicorn analizador_prex_api:app --reload
```

---

## Despliegue en Docker / Portainer

### Docker Compose (recomendado)

```yaml
version: '3.8'

services:
  analizador-api:
    image: jmercadot/analizador-api:latest
    container_name: analizador-api
    ports:
      - "5000:8000"
    volumes:
      - analisis_sqlite:/data
      - analisis_sqlite:/app
    command: uvicorn analizador_prex_api:app --host 0.0.0.0 --port 8000
    restart: unless-stopped

  sqliteweb:
    image: coleifer/sqlite-web
    container_name: sqlite-web
    ports:
      - "8080:8080"
    volumes:
      - analisis_sqlite:/data
    restart: unless-stopped

volumes:
  analisis_sqlite:
```

### Accesos recomendados

* API Swagger UI: `http://<IP>:5000/docs`
* Interfaz SQLite Web: `http://<IP>:8080`

---

## Extras

* Compatible con despliegue en AWS EC2.
* Acceso externo controlado por Security Groups y firewall.
* Imágenes alojadas en DockerHub:

  * `jmercadot/analizador-api`
  * `coleifer/sqlite-web`

---

## Autor

* Proyecto desarrollado por **Jesús Mercado** para Prex.
* Soporte, documentación y despliegue Docker por Jesus Mercado
