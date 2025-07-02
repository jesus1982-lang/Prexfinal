# analizador_prex_api.py con SQLAlchemy, SQLite y FastAPI
import os
print("📌 Usando base en:", os.path.abspath("analisis.db"))

import requests
import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

Base = declarative_base()

# --- MODELOS DB ---
class Sitio(Base):
    __tablename__ = 'sitios'
    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    ip = Column(Text)
    status_code = Column(Integer)
    redireccion = Column(Text)
    fecha_analisis = Column(DateTime, default=datetime.now)
    headers = relationship("Header", backref="sitio")
    certificado = relationship("Certificado", uselist=False, backref="sitio")

class Header(Base):
    __tablename__ = 'headers'
    id = Column(Integer, primary_key=True)
    sitio_id = Column(Integer, ForeignKey('sitios.id'), nullable=False)
    nombre = Column(Text, nullable=False)
    valor = Column(Text)

class Certificado(Base):
    __tablename__ = 'certificados'
    id = Column(Integer, primary_key=True)
    sitio_id = Column(Integer, ForeignKey('sitios.id'), nullable=False)
    valido_desde = Column(Text)
    valido_hasta = Column(Text)
    sujetos = relationship("CertSujeto", backref="certificado")
    emisores = relationship("CertEmisor", backref="certificado")

class CertSujeto(Base):
    __tablename__ = 'cert_sujetos'
    id = Column(Integer, primary_key=True)
    certificado_id = Column(Integer, ForeignKey('certificados.id'), nullable=False)
    clave = Column(Text, nullable=False)
    valor = Column(Text)

class CertEmisor(Base):
    __tablename__ = 'cert_emisores'
    id = Column(Integer, primary_key=True)
    certificado_id = Column(Integer, ForeignKey('certificados.id'), nullable=False)
    clave = Column(Text, nullable=False)
    valor = Column(Text)

# --- CONEXIÓN DB ---
engine = create_engine('sqlite:///analisis.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# --- APP FASTAPI ---
app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.post("/analizar")
def analizar_endpoint(peticion: URLRequest):
    url = peticion.url
    datos = {"url": url}
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        datos["status_code"] = response.status_code
        datos["headers"] = dict(response.headers)
        datos["redireccion"] = response.url if response.url != url else None
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error al conectar: {e}")

    try:
        host = urlparse(url).hostname
        ip = socket.gethostbyname(host)
        datos["ip"] = ip
    except socket.error:
        datos["ip"] = None

    datos["certificado"] = None
    if url.startswith("https"):
        try:
            contexto = ssl.create_default_context()
            with socket.create_connection((host, 443), timeout=10) as sock:
                with contexto.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    datos["certificado"] = {
                        "valido_desde": cert.get("notBefore"),
                        "valido_hasta": cert.get("notAfter"),
                        "sujeto": dict(x[0] for x in cert.get("subject", [])),
                        "emisor": dict(x[0] for x in cert.get("issuer", []))
                    }
        except Exception as e:
            pass

    sitio = Sitio(
        url=url,
        ip=datos.get("ip"),
        status_code=datos.get("status_code"),
        redireccion=datos.get("redireccion")
    )
    session.add(sitio)
    session.commit()

    for k, v in datos.get("headers", {}).items():
        session.add(Header(sitio_id=sitio.id, nombre=k, valor=v))

    cert_info = datos.get("certificado")
    if cert_info:
        cert = Certificado(
            sitio_id=sitio.id,
            valido_desde=cert_info.get("valido_desde"),
            valido_hasta=cert_info.get("valido_hasta")
        )
        session.add(cert)
        session.commit()

        for k, v in cert_info.get("sujeto", {}).items():
            session.add(CertSujeto(certificado_id=cert.id, clave=k, valor=v))
        for k, v in cert_info.get("emisor", {}).items():
            session.add(CertEmisor(certificado_id=cert.id, clave=k, valor=v))

    session.commit()
    return {"message": f"Análisis de {url} guardado en base de datos."}