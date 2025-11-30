# LoteTracker - Generador de Códigos QR para Trazabilidad

LoteTracker es una aplicación de escritorio moderna construida con Python y Flet para la generación y gestión de códigos QR de trazabilidad en entornos agroindustriales. Permite registrar lotes de producción, generar etiquetas QR híbridas (offline/online) y mantener un historial detallado.

## Características Principales

*   **Generación de QR Híbridos**: Los códigos QR contienen información vital legible sin conexión (Producto, Cantidad, Proveedor, Operador) y un enlace a un dashboard en línea para seguimiento en tiempo real.
*   **Autocompletado Inteligente**: Campos de entrada con sugerencias dinámicas basadas en datos históricos para Operadores, Productos y Proveedores.
*   **Gestión de Operadores Bidireccional**: Selección flexible por Nombre o Código de operador, con sincronización automática entre ambos campos.
*   **Entrada Flexible**: Permite seleccionar datos existentes o crear nuevos registros (Productos, Proveedores, Operadores) sobre la marcha.
*   **Historial de Lotes**: Tabla integrada para visualizar los últimos registros generados.
*   **Interfaz Moderna**: Diseño limpio, espacioso y amigable, optimizado para pantallas táctiles o escritorio.
*   **Base de Datos MongoDB**: Almacenamiento robusto y escalable de todos los registros.

## Requisitos Previos

*   Python 3.8 o superior
*   MongoDB (local o remoto)

## Instalación

1.  **Clonar el repositorio**:
    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-directorio>
    ```

2.  **Crear un entorno virtual (recomendado)**:
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**:
    Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```env
    MONGO_URI=mongodb://localhost:27017/
    DB_NAME=lotetracker_db
    BASE_URL=http://tu-ip-local:8550
    ```
    *Asegúrate de reemplazar `tu-ip-local` con la dirección IP de tu máquina si planeas escanear los QR desde otros dispositivos en la misma red.*

## Uso

1.  **Iniciar la aplicación**:
    ```bash
    python main.py
    ```

2.  **Generar un QR**:
    *   **Operador**: Selecciona un nombre o código existente, o escribe uno nuevo.
    *   **Producto**: Escribe el nombre del producto (ej: "Cúrcuma").
    *   **Cantidad**: Ingresa el valor y selecciona la unidad (kg, g, lb, etc.).
    *   **Proveedor**: Selecciona o ingresa el proveedor.
    *   **Fecha**: Por defecto es la actual, pero puedes modificarla.
    *   Haz clic en **"Generar código QR"**.

3.  **Descargar**:
    *   Una vez generado, aparecerá la tarjeta con el código QR.
    *   Haz clic en **"Descargar código QR"** para guardar la imagen PNG.

## Estructura del Proyecto

*   `src/`: Código fuente de la aplicación.
    *   `app.py`: Lógica principal de la interfaz de generación.
    *   `database_manager.py`: Gestión de conexión y consultas a MongoDB.
    *   `components/`: Componentes de UI reutilizables (autocompletado, tarjetas, etc.).
*   `main.py`: Punto de entrada de la aplicación.
*   `requirements.txt`: Lista de dependencias.

## Tecnologías

*   [Flet](https://flet.dev/): Framework de UI para Python.
*   [PyMongo](https://pymongo.readthedocs.io/): Driver de MongoDB para Python.
*   [Segno](https://github.com/heuer/segno): Generador de códigos QR.
