from Base_Item import Item


class Shelly(Item):

    def __init__(self, values):
        Item.__init__(self, values)
        self.brand = "ALLTERCO ROBOTICS EOOD"
        self.image = ""


class Shelly_1(Shelly):

    def __init__(self):
        code = "SHELLY1"
        name = "Shelly 1"
        description = """
        Relevador / Interruptor WIFI
        Industrial y residencial inteligente /
        Hasta 16A / Soporta Google /Alexa /
        Nube P2P y control Local /"""
        my_price = 13.19
        sell_price = 22.62

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_Plug(Shelly):

    def __init__(self):
        code = "SHELLYPLUGS"
        name = "Shelly Plug"
        description = """
        Adaptador WIFI NUBE P2P Shelly,
        Tomacorriente, Calendarios,
        MEDICIÓN DE CONSUMO"""
        my_price = 24.94
        sell_price = 40.60

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_Dimmer(Shelly):

    def __init__(self):
        code = "SHELLYDIMMER"
        name = "Shelly Dimmer"
        description = """
        (MÁS PEQUEÑO DEL MUNDO) DIMMMER WIFI CLOUD /
        Inalámbrico residencial inteligente
        / Protección de sobre carga / 16A
        / Soporta Google / Alexa / Nube P2P y local /"""
        my_price = 27.80
        sell_price = 45.24

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_25(Shelly):

    def __init__(self):
        code = "SHELLY25"
        name = "Shelly 25"
        description = """
        Doble Relevador / Interruptor WIFI
        CLOUD Industrial y residencial
        Inteligente / Medidor de consumo /
        10A / Soporta Google /Alexa /
        Nube P2P y local / Ideal para
        persinas y garage"""
        my_price = 21.38
        sell_price = 45.24

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_1_PM(Shelly):

    def __init__(self):
        code = "SHELLY1PM"
        name = "Shelly 1 PM"
        description = """
        Relevador / Interruptor WIFI CLOUD
        / Industrial y residencial Inteligente
        / Medidor de consumo, protección
        hasta 3500W / 16A / Soporta
        Google / Alexa / Nube P2P y
        control local /"""
        my_price = 16.39
        sell_price = 33.64

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_HT(Shelly):

    def __init__(self):
        code = "SHELLYHT"
        name = "Shelly HT"
        description = """
        Sensor inalámbrico de temperatura
        y humedad, App gratis, métricas de
        lectura en graficas y notificaciones
        en celular."""
        my_price = 26.37
        sell_price = 42.92

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_RGBW2(Shelly):

    def __init__(self):
        code = "SHELLY-RGBW2"
        name = "Shelly RGBW2"
        description = """
        Relevador inalámbrico para el
        control de iluminación color en
        tiras LED."""
        my_price = 28.51
        sell_price = 46.40

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_1L(Shelly):

    def __init__(self):
        code = "SHELLY1L"
        name = "Shelly 1L"
        description = """
        Relevador SIN usar cable Neutro /
        Interruptor WIFI INDUSTRIAL
        Industrial y residencial inteligente /
        Hasta 5A / Soporta Google /Alexa /
        Nube P2P y control Local /"""
        my_price = 21.38
        sell_price = 34.80

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)


class Shelly_HC7(Shelly):

    def __init__(self):
        code = "HC7"
        name = "Shelly HC7"
        description = """
        HUB Controlador inteligente para
        dispositivos Zwave, Zigbee,
        integrable con Shelly, Lutron entre
        otras, APP gratis sin pago de
        anualidad o mensualidad."""
        my_price = 144.68
        sell_price = 235.48

        values = [code, name, description, my_price, sell_price]
        Shelly.__init__(self, values)
