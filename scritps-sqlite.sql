-- Tabla de sitios analizados
CREATE TABLE IF NOT EXISTS sitios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    ip TEXT,
    status_code INTEGER,
    redireccion TEXT,
    fecha_analisis TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de headers HTTP
CREATE TABLE IF NOT EXISTS headers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sitio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    valor TEXT,
    FOREIGN KEY (sitio_id) REFERENCES sitios(id)
);

-- Tabla de certificados SSL
CREATE TABLE IF NOT EXISTS certificados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sitio_id INTEGER NOT NULL,
    valido_desde TEXT,
    valido_hasta TEXT,
    FOREIGN KEY (sitio_id) REFERENCES sitios(id)
);

-- Detalles del sujeto del certificado
CREATE TABLE IF NOT EXISTS cert_sujetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificado_id INTEGER NOT NULL,
    clave TEXT NOT NULL,
    valor TEXT,
    FOREIGN KEY (certificado_id) REFERENCES certificados(id)
);

-- Detalles del emisor del certificado
CREATE TABLE IF NOT EXISTS cert_emisores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificado_id INTEGER NOT NULL,
    clave TEXT NOT NULL,
    valor TEXT,
    FOREIGN KEY (certificado_id) REFERENCES certificados(id)
);