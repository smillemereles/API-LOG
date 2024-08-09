## API de Gestión de Logs

## API simple para enviar y consultar logs, construida con Python, Flask y SQL Server.

## Requisitos

- Python 3.7+
- SQL Server
- pip

## Instalación

1. Clonar el repositorio
2. Instalar dependencias: `pip install flask pyodbc`
3. Crear base de datos 'logsdb' en SQL Server con tabla 'logs'
4. Configurar `DB_CONFIG` en `servidor_central.py`

## Uso

1. Iniciar servidor: `python servidor_central.py`
2. Simular envío de logs: `python servicio_simulado.py`

## Endpoints

- POST /logs: Enviar logs
- GET /logs: Consultar logs (parámetros opcionales: startDate, endDate, serviceName)

Nota: Todas las solicitudes requieren clave API en el encabezado 'x-api-key'.

## Estructura del Proyecto

- `servidor_central.py`: Servidor principal
- `servicio_simulado.py`: Simula envío de logs
- `auths.py`: Autenticación de clave API

Para más detalles, consultar el código fuente.# API-LOG
