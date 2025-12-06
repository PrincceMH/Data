# CRM Django - Sistema de Gestión de Clientes

Aplicación Django para gestionar clientes, compañías, representantes de ventas e interacciones.

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/PrincceMH/Data.git
cd Data
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv 

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install django faker
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

## Poblar la Base de Datos

Generar datos ficticios (3 representantes, 1000 clientes, 500,000 interacciones):

```bash
python manage.py populate_db
```

## Ejecutar el Proyecto

Iniciar el servidor:
```bash
python manage.py runserver
```

Acceder a la aplicación en: **http://127.0.0.1:8000/**

## Funcionalidades

### Vista Principal (CRM)

La aplicación muestra una tabla con todos los clientes que incluye:

- **Nombre completo** del cliente
- **Empresa** a la que pertenece
- **Cumpleaños** en formato legible (ejemplo: "February 5")
- **Última interacción** con tiempo relativo y tipo (ejemplo: "2 days ago (Call)")
- **Representante** asignado

### Filtros Disponibles

- **Búsqueda por nombre**: Encuentra clientes escribiendo su nombre
- **Filtro de cumpleaños**:
  - Cumpleaños hoy
  - Cumpleaños esta semana
  - Cumpleaños este mes

### Ordenamiento

Puedes ordenar la tabla por cualquiera de estas columnas (ascendente o descendente):
- Nombre del cliente
- Empresa
- Cumpleaños
- Fecha de última interacción

### Base de Datos

El sistema maneja 4 tablas principales:

- **User**: Representantes de ventas con email único y contraseña cifrada
- **Company**: Empresas donde trabajan los clientes
- **Customer**: Clientes vinculados a una empresa y un representante
- **Interaction**: Registro de todas las interacciones (Call, Email, SMS, Facebook, WhatsApp, LinkedIn, Meeting, Video Call)

