# 🛡️ Analizador de Sitios Web – Desafío de Ciberseguridad Prex

Este programa fue desarrollado como parte del proceso de selección para un puesto en el área de Ciberseguridad de Prex. Su objetivo es realizar un análisis básico de una URL dada, brindando información clave sobre su accesibilidad, seguridad y posibles redirecciones.

---

## 📌 ¿Qué hace el programa?

Al ejecutar el script, se solicita al usuario ingresar una URL. A partir de esa entrada, el programa realiza los siguientes pasos:

1. **Verifica si el sitio está accesible**

   - Realiza una solicitud HTTP y muestra el código de estado (`200`, `301`, etc.).
   - Informa si el sitio redirige a otro dominio.

2. **Obtiene la dirección IP del dominio**

   - Resuelve el nombre DNS y muestra la IP pública asociada.

3. **Analiza los encabezados HTTP**

   - Muestra los headers recibidos del servidor.

4. **Inspecciona el certificado SSL (si corresponde)**

   - Si el sitio usa HTTPS, se conecta por SSL y extrae:
     - Emisor del certificado
     - Sujeto del certificado
     - Fecha de inicio y vencimiento

5. **Guarda todo el resultado en un archivo JSON**

   - El archivo `resultado_analisis.json` contiene el informe completo.

---

## 🧠 ¿Por qué es útil esto en ciberseguridad?

Este análisis inicial permite validar:

- Si un sitio es legítimo y está online
- Qué tecnología de seguridad utiliza (certificados, redirecciones, headers)
- Si el certificado es válido o expiró
- Si está protegido por HTTPS y qué entidad lo emite

Todo esto forma parte de los **controles básicos de higiene digital** al evaluar activos, endpoints o dominios externos.

---

## ⚙️ Requisitos técnicos

- Python 3.8+
- Librería `requests`
- Acceso a internet
- Compatible con Windows, Linux o MacOS

---

## ▶️ ¿Cómo se usa?

1. Asegurate de tener Python y pip instalados
2. (Opcional) Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install requests
   ```
4. Ejecutar el script:
   ```bash
   python analizador_prex.py
   ```
5. Ingresar la URL a analizar cuando se solicite
6. Ver los resultados en pantalla y en el archivo generado

---

## 📦 Archivos generados

- `resultado_analisis.json`: contiene toda la información del análisis en formato estructurado

---

## 💡 Extensiones posibles

Este script puede evolucionar para incluir:

- Verificación de políticas HTTP (HSTS, CSP, CAA)
- Escaneo de puertos (superficial)
- Revisión de reputación del dominio en listas negras
- Análisis de DNS (MX, TXT, SPF, etc.)
- Integración con herramientas como VirusTotal, Shodan o Censys

---

## 👨‍💻 Autores

Desarrollado por ChatGPT para acompañar a un perfil técnico de infraestructura en su aplicación al rol de Ciberseguridad en Prex.

---

## 📩 Contacto

Para dudas o mejoras, contactar a tu referente técnico o al área de RRHH de Prex.

---

> “La ciberseguridad comienza por conocer el entorno.”

