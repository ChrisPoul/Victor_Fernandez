from textwrap import dedent


def get_with_iva(price):
    price_with_iva = str(round(price * 1.16, 2))

    if price_with_iva[-2:] == ".0":
        price_with_iva += "0"

    return "$" + price_with_iva


class Shelly:

    def __init__(self):
        self.brand = "ALLTERCO ROBOTICS EOOD"


class Shelly_1:

    def __init__(self):
        self.code = "SHELLY1"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly 1"
        self.image = ""
        self.description = dedent("""
        Relevador / Interruptor WIFI
        Industrial y residencial inteligente /
        Hasta 16A / Soporta Google /Alexa /
        Nube P2P y control Local /
        """)
        self.wholesaler_price = 13.19
        self.customer_price = 22.62


class Shelly_Plug:

    def __init__(self):
        self.code = "SHELLYPLUGS"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly Plug"
        self.image = ""
        self.description = dedent("""
        Adaptador WIFI NUBE P2P Shelly,
        Tomacorriente, Calendarios,
        MEDICIÓN DE CONSUMO
        """)
        self.wholesaler_price = 24.94
        self.customer_price = 40.60


class Shelly_Dimmer:

    def __init__(self):
        self.code = "SHELLYDIMMER"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly Dimmer"
        self.image = ""
        self.description = dedent("""
        (MÁS PEQUEÑO DEL MUNDO) DIMMMER WIFI CLOUD /
        Inalámbrico residencial inteligente
        / Protección de sobre carga / 16A
        / Soporta Google / Alexa / Nube P2P y local /
        """)
        self.wholesaler_price = 27.80
        self.customer_price = 45.24


class Shelly_25:

    def __init__(self):
        self.code = "SHELLY25"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly 25"
        self.image = ""
        self.description = dedent("""
        Doble Relevador / Interruptor WIFI
        CLOUD Industrial y residencial
        Inteligente / Medidor de consumo /
        10A / Soporta Google /Alexa /
        Nube P2P y local / Ideal para
        persinas y garege
        """)
        self.wholesaler_price = 21.38
        self.customer_price = 45.24


class Shelly_1_PM:

    def __init__(self):
        self.code = "SHELLY1PM"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = ""
        self.image = "Shelly 1 PM"
        self.description = dedent("""
        Relevador / Interruptor WIFI CLOUD
        / Industrial y residencial Inteligente
        / Medidor de consumo, protección
        hasta 3500W / 16A / Soporta
        Google / Alexa / Nube P2P y
        control local /
        """)
        self.wholesaler_price = 16.39
        self.customer_price = 33.64


class Shelly_HT:

    def __init__(self):
        self.code = "SHELLYHT"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly HT"
        self.image = ""
        self.description = dedent("""
        Sensor inalámbrico de temperatura
        y humedad, App gratis, métricas de
        lectura en graficas y notificaciones
        en celular.
        """)
        self.wholesaler_price = 26.37
        self.customer_price = 42.92


class Shelly_RGBW2:

    def __init__(self):
        self.code = "SHELLY-RGBW2"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly RGBW2"
        self.image = ""
        self.description = dedent("""
        Relevador inalámbrico para el
        control de iluminación color en
        tiras LED.
        """)
        self.wholesaler_price = 28.51
        self.customer_price = 46.40


class Shelly_1L:

    def __init__(self):
        self.code = "SHELLY1L"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly 1L"
        self.image = ""
        self.description = dedent("""
        Relevador SIN usar cable Neutro /
        Interruptor WIFI INDUSTRIAL
        Industrial y residencial inteligente /
        Hasta 5A / Soporta Google /Alexa /
        Nube P2P y control Local /
        """)
        self.wholesaler_price = 21.38
        self.customer_price = 34.80


class Shelly_HC7:

    def __init__(self):
        self.code = "HC7"
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.name = "Shelly HC7"
        self.image = ""
        self.description = dedent("""
        HUB Controlador inteligente para
        dispositivos Zwave, Zigbee,
        integrable con Shelly, Lutron entre
        otras, APP gratis sin pago de
        anualidad o mensualidad.
        """)
        self.wholesaler_price = 144.68
        self.customer_price = 235.48
