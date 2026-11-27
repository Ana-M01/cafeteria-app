# Aire en Colombia — PM2.5 por departamento y año
- URL pública: https://suenos-en-cafe.onrender.com
- Repositorio: https://github.com/Ana-M01/cafeteria-app
- Correr: `docker build -t mi-app . && docker run --rm -p 8765:8765 --env-file .env mi-app` y abrir http://localhost:8765
- Datos: [Calidad del Aire en Colombia (Promedio Anual)](https://www.datos.gov.co/d/kekd-7v7h), IDEAM – SISAIRE, datos.gov.co, licencia CC BY-SA 4.0 (archivo `datos/calidad_aire.csv`, descargado el 26/11/2026)
- Variables: `NOMBRE_APP`, `CLAVE_ADMIN` (se configuran en Render; copie `.env.example` como `.env` para correrla local)
