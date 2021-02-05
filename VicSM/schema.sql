DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS client;

CREATE TABLE product (
    grupo TEXT NOT NULL,
    serie TEXT NOT NULL,
    codigo TEXT PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    marca TEXT NOT NULL,
    imagen TEXT NOT NULL,
    mi_precio INTEGER NOT NULL,
    precio_venta INTEGER NOT NULL,
    inventario INTEGER NOT NULL
);

CREATE TABLE client (
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tel TEXT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cambio INTEGER NOT NULL,
    proyecto TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    cotizacion TEXT NOT NULL
);

CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id FOREIGN KEY (client_id) REFERENCES client (id),
    grupo TEXT NOT NULL,
    totals List,
    total INTEGER NOT NULL,
    cantidades LIST,
    products LIST
);
