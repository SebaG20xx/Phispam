# Phispam


## Descripción

El script realiza las siguientes acciones:

1. **Generación de RUT chileno**: Utiliza una función para generar un RUT válido con dígito verificador.
2. **Generación de contraseña aleatoria**: Crea una contraseña aleatoria que cumple con ciertos requisitos de seguridad.
3. **Simulación de sesión de navegador**: Utiliza la librería `requests` para simular una sesión de navegador y mantener las cookies.
4. **Realización de solicitudes HTTP**: Realiza solicitudes GET y POST para interactuar con el sitio web de phishing.
5. **Envío de datos falsos**: Envía datos de inicio de sesión y los 50 casilleros de la superclave usando datos aleatorios
6. **Ejecución continua**: El script se ejecuta en un bucle infinito, enviando spam cada 5 segundos para llenar la base de datos del sitio de phishing con datos inútiles.

## Uso

1. **Clonar el repositorio**: Clona este repositorio en tu máquina local.
    ```bash
    git clone https://github.com/SebaG20xx/Phispam.git
    cd Phispam
    ```

2. **Instalar los requisitos**: Instala los paquetes de Python necesarios.
    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecutar el script**: Ejecuta el script en tu entorno de desarrollo o servidor.
    ```bash
    python phispam.py
    ```




## Licencia

Este proyecto está licenciado bajo los términos de la [MIT License](LICENSE).


