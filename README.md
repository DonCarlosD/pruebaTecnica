# Prueba Técnica - Django REST API

Este proyecto es una API desarrollada en **Django + Django REST Framework**, que permite gestionar remisiones, ventas y créditos, incluyendo endpoints para cierre de remisiones y reportes diarios de ventas.

---

## Requisitos

- Python 3.12+ (recomendado)
- SQLite
- pip / virtualenv

---

## Instalación

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd pruebaTecnica
```
2. Crear entorno virtual:
```bash
    python -m venv venv
```
3. Activar entorno virtual:
```bash
    venv\Scripts\activate
```
4. Instalar dependencias:
```bash
    pip install -r requirements.txt
```
## Migraciones
Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
## Poblar la base de datos (Seeds)
Ejecutar
```bash
python manage.py seed
```
## Ejecutar el servidor 
```bash
python manage.py runserver
```
la api estara disponible 
http://127.0.0.1:8000/commerce/api/v1

## Ejecutar pruebas
```bash
python manage.py test
```
para correr pruebas unicamente en el modulo commerce:
```bash
python manage.py test commerce
```

Autor
Carlos Daniel Ochoa Mejía