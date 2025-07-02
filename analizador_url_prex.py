#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de análisis básico de sitios web para el desafío de Ciberseguridad de Prex.
Autor: ChatGPT (adaptado para un perfil de infraestructura)
Requisitos: Python 3.8+ y requests
"""

import requests
import socket
import ssl
import json
from urllib.parse import urlparse


def analizar_url(url):
    """
    Recibe una URL, verifica si está activa, obtiene su IP, headers, certificados SSL
    y si realiza redirecciones. Devuelve toda la información en un diccionario.
    """
    datos = {"url": url}

    # 1. Verificamos si el sitio está accesible (status 200, 301, etc.)
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        datos["status_code"] = response.status_code
        datos["headers"] = dict(response.headers)
        datos["redireccionado"] = response.url if response.url != url else None
    except requests.exceptions.RequestException as e:
        datos["error"] = str(e)
        return datos

    # 2. Resolvemos la IP del dominio
    try:
        host = urlparse(url).hostname
        ip = socket.gethostbyname(host)
        datos["ip"] = ip
    except socket.error as e:
        datos["ip_error"] = str(e)

    # 3. Obtenemos certificado SSL (si el sitio es HTTPS)
    if url.startswith("https"):
        try:
            contexto = ssl.create_default_context()
            with socket.create_connection((host, 443), timeout=10) as sock:
                with contexto.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    datos["certificado"] = {
                        "sujeto": dict(x[0] for x in cert.get("subject", [])),
                        "emisor": dict(x[0] for x in cert.get("issuer", [])),
                        "valido_desde": cert.get("notBefore"),
                        "valido_hasta": cert.get("notAfter")
                    }
        except Exception as e:
            datos["certificado_error"] = str(e)

    return datos


if __name__ == "__main__":
    # Solicitamos la URL al usuario
    url = input("Ingrese la URL a analizar (ej: https://prex.com.uy): ").strip()
    resultado = analizar_url(url)

    # Mostramos por pantalla en formato legible
    print(json.dumps(resultado, indent=4, ensure_ascii=False))

    # Guardamos en archivo JSON
    with open("resultado_analisis.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
