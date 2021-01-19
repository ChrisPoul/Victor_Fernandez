DROP TABLE IF EXISTS product;

CREATE TABLE product (
    grupo TEXT NOT NULL,
    serie TEXT NOT NULL,
    codigo TEXT PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    marca TEXT NOT NULL,
    imagen TEXT NOT NULL,
    mi_precio INT NOT NULL,
    precio_venta INTEGER NOT NULL,
    inventario INTEGER NOT NULL
);
