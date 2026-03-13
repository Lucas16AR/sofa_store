# Sofa Store – Configurador de Sillones

Sistema web desarrollado con Flask que permite a los usuarios configurar sillones personalizados seleccionando diferentes opciones (telas, colores, rellenos, etc.).

El sistema genera pedidos personalizados que pueden ser gestionados por un administrador.

Este proyecto fue desarrollado como parte del programa educativo **Conectados x Mendoza Futura**.

---

# Características principales

## Usuarios
- Registro de usuarios
- Inicio de sesión
- Visualización de pedidos realizados

## Cliente
- Visualización de productos disponibles
- Configuración personalizada de sofás
- Selección de opciones por categoría
- Cálculo automático del precio final
- Registro del pedido en el sistema
- Envío del pedido por WhatsApp

## Administrador
Panel de administración que permite:

- Crear productos
- Activar o desactivar productos
- Crear categorías de opciones
- Crear opciones de configuración
- Definir costos adicionales por opción
- Activar o desactivar opciones
- Visualizar pedidos realizados
- Ver datos de contacto del cliente

---

# Tecnologías utilizadas

- Python 3
- Flask
- Flask Login
- Flask WTF
- Flask SQLAlchemy
- Flask Migrate
- SQLite
- Bootstrap

---

# Estructura del proyecto
# Sofa Store – Configurador de Sofás

Sistema web desarrollado con Flask que permite a los usuarios configurar sofás personalizados seleccionando diferentes opciones (telas, colores, rellenos, etc.).

El sistema genera pedidos personalizados que pueden ser gestionados por un administrador.

Este proyecto fue desarrollado como parte del programa educativo **Conectados x Mendoza Futura**.

---

# Características principales

## Usuarios
- Registro de usuarios
- Inicio de sesión
- Visualización de pedidos realizados

## Cliente
- Visualización de productos disponibles
- Configuración personalizada de sofás
- Selección de opciones por categoría
- Cálculo automático del precio final
- Registro del pedido en el sistema
- Envío del pedido por WhatsApp

## Administrador
Panel de administración que permite:

- Crear productos
- Activar o desactivar productos
- Crear categorías de opciones
- Crear opciones de configuración
- Definir costos adicionales por opción
- Activar o desactivar opciones
- Visualizar pedidos realizados
- Ver datos de contacto del cliente

---

# Tecnologías utilizadas

- Python 3
- Flask
- Flask Login
- Flask WTF
- Flask SQLAlchemy
- Flask Migrate
- SQLite
- Bootstrap

---

# Estructura del proyecto
sofa_store
│
├── app
│ ├── routes
│ │ ├── admin.py
│ │ ├── auth.py
│ │ └── public.py
│ │
│ ├── models.py
│ ├── forms
│ ├── templates
│ ├── static
│ └── extensions.py
│
├── migrations
├── instance
├── config.py
├── run.py
└── requirements.txt

---

# Instalación del proyecto

1. Clonar el repositorio o descargar el proyecto

2. Crear entorno virtual

python -m venv .venv

3. Activar entorno virtual

Windows: .venv\Scripts\activate

4. Instalar dependencias

pip install -r requirements.txt

5. Inicializar base de datos

flask db upgrade

6. Ejecutar el servidor

python run.py

El sistema estará disponible en: http://127.0.0.1:5000

---

# Usuario administrador

El sistema crea automáticamente un administrador inicial:

Email: admin@sofastore.com

Password: admin123

---

# Posibles mejoras futuras

- Sistema de compatibilidad entre opciones
- Gestión de stock
- Integración con pagos online
- Panel de estadísticas
- Gestión avanzada de pedidos

---

# Autor

Proyecto desarrollado como práctica educativa dentro del programa **Conectados x Mendoza Futura**.