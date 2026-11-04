# LUSH EbirTribE EMX-1

**LUSH EbirTribE EMX-1** es un clon de la mítica caja de ritmos y sintetizador **Korg Electribe EMX-1**, desarrollado en Python. El proyecto replica la interfaz de usuario, las funciones de secuenciación y las capacidades de síntesis de audio del hardware original en un entorno de software accesible.

## Características

* **Emulación de EMX-1:** Recreación de las funciones lógicas, de secuenciación y de síntesis basadas en el hardware original.
* **Interfaz Gráfica Modular:** Interfaz de usuario diseñada en módulos limpios y widgets personalizados (`ui.py`, `widget.py`, `interface.py`).
* **Motor de Audio Integrado:** Gestión y reproducción de muestras y síntesis en tiempo real (`audio.py`).
* **Sistema de Archivos Propio:** Estructura optimizada para guardar y cargar patrones, muestras y configuraciones (`filesys.py`).

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

* `ebirtribe.py`: Punto de entrada principal para ejecutar la aplicación.
* `app.py`: Orquestador de sistemas e interfaces
* `emx.py`: Lógica central del sistema y emulación de los componentes internos de la Electribe.
* `audio.py`: Motor de audio y procesamiento de sonido.
* `ui.py` / `interface.py` / `widget.py`: Implementación de la interfaz gráfica y los controles visuales.
* `filesys.py`: Manejo del almacenamiento y carga de archivos.
* `resources/`: Carpeta destinada a almacenar assets, imágenes, muestras de audio, tipografías...

## Instalación

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/pinakure/ebirtribe.git
   cd ebirtribe
   ```

2. Instala las dependencias requeridas utilizando el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para iniciar la aplicación, ejecuta el archivo principal `ebirtribe.py` desde tu terminal:

```bash
python ebirtribe.py
```

## Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo `LICENSE` incluido en este repositorio para más detalles.
