# settings.py
import pygame

# ========================= settings.py =========================
# CONFIGURACIÓN COMPLETA DEL JUEGO - MUNDO LIBRE MATEMÁTICO

# ==================== CONFIGURACIÓN DE PANTALLA ====================
# NOTA: NO inicializar pygame aquí

# Modos de pantalla
PANTALLA_COMPLETA = True
MODO_DESARROLLO = False

# Valores por defecto (se ajustarán en main.py)
ANCHO = 1920
ALTO = 1080
FPS = 60
TAM = 48

# ==================== DIVISIÓN DE PANTALLA ====================
PORCENTAJE_MENU = 0.10          # 10% para menú superior
PORCENTAJE_ANCHO_JUEGO = 0.70   # 70% ancho para área de juego
PORCENTAJE_ALTO_JUEGO = 0.70    # 70% alto para área de juego
PORCENTAJE_PANEL = 0.30         # 30% ancho para panel derecho

# ==================== COLORES BÁSICOS ====================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 100, 255)
GRIS = (100, 100, 100)
GRIS_OSCURO = (50, 50, 50)
GRIS_CLARO = (200, 200, 200)

# ==================== CONFIGURACIÓN DE ZOOM ====================
ZOOM_MIN = 0.5
ZOOM_MAX = 2.0
ZOOM_INCREMENTO = 0.1
ZOOM_POR_DEFECTO = 1.0

# ==================== CONFIGURACIÓN DE BALAS ====================
VELOCIDAD_BALA_MIN = 5
VELOCIDAD_BALA_MAX = 20
VELOCIDAD_BALA_DEFAULT = 10
VELOCIDAD_BALA_INCREMENTO = 1
BALAS_MAXIMAS = 30
BALAS_RECARGA = 10
TIEMPO_RECARGA = 2.0
TIEMPO_ENTRE_DISPAROS = 8
DISPAROS_MAXIMOS_SIMULTANEOS = 5

# ==================== CONFIGURACIÓN DE ENEMIGOS ====================
VEL_ENEMIGO = 1.5
RANGO_VISION_CORTO = 150
RANGO_VISION_LARGO = 400
TIEMPO_ENTRE_DISPAROS_ENEMIGOS = 90
VELOCIDAD_BALA_ENEMIGA = 5

# ==================== CONFIGURACIÓN DE TÚNELES ====================
MODO_OSCURO = True
LUZ_RADIO = 120
LUZ_RADIO_TUNEL = 70
LUZ_RADIO_NORMAL = 120
OSCURIDAD_TUNEL_ALPHA = 210

# ==================== COLORES DE TEXTO ====================
TEXTO_TITULO = (255, 215, 0)          # Dorado
TEXTO_NIVEL = (138, 43, 226)          # Violeta
TEXTO_PUNTOS = (255, 215, 0)          # Dorado
TEXTO_FRANJA = (50, 30, 10)           # Marrón oscuro para franja
TEXTO_PERGA_TITULO = (80, 50, 30)     # Marrón para título pergamino
TEXTO_PERGA_NORMAL = (60, 40, 20)     # Marrón oscuro para texto pergamino
TEXTO_SOMBRA = (30, 30, 30)           # Negro para sombras
TEXTO_VIDAS = (255, 105, 97)          # Rojo claro
TEXTO_SECUNDARIO = (200, 200, 200)    # Gris claro
TEXTO_OPERACION = (57, 255, 20)       # Verde brillante
TEXTO_CORRECTO = (0, 255, 127)        # Verde esmeralda
TEXTO_RESPUESTA = (255, 255, 51)      # Amarillo
TEXTO_INCORRECTO = (255, 69, 0)       # Rojo naranja
TEXTO_BALAS = (100, 200, 255)         # Azul claro
TEXTO_NORMAL = (255, 255, 255)        # Blanco
TEXTO_CONTROL_IMPORTANTE = (100, 200, 255)  # Azul claro
TEXTO_TUNEL = (255, 200, 50)          # Amarillo oscuro
TEXTO_TUNEL_BRILLO = (255, 255, 150)  # Amarillo brillante
TEXTO_ENCABEZADO = (100, 200, 255)    # Azul claro
TEXTO_ENEMIGOS = (255, 99, 71)        # Rojo tomate
TEXTO_MISION_TITULO = (255, 165, 0)   # Naranja
TEXTO_MISION_DESC = (200, 200, 255)   # Azul muy claro
TEXTO_MISION_PROG = (144, 238, 144)   # Verde claro
TEXTO_MISION_COMP = (50, 205, 50)     # Verde lima
TEXTO_NPC_NOMBRE = (255, 215, 0)      # Dorado
TEXTO_NPC_DIALOGO = (240, 240, 240)   # Blanco casi puro
TEXTO_INVENTARIO = (255, 200, 100)    # Amarillo anaranjado
TEXTO_ITEM = (200, 255, 200)          # Verde muy claro
TEXTO_PRECIO = (255, 255, 100)        # Amarillo
TEXTO_EXPERIENCIA = (147, 112, 219)   # Púrpura medio

# ==================== CONFIGURACIÓN DE JUEGO ====================
VIDAS_INICIALES = 3
BALAS_INICIALES = 15
OPERACIONES_NECESARIAS = 3

# Sistema de puntos
PUNTOS_ENEMIGO_BASICO = 20
PUNTOS_ENEMIGO_CAMUFLADO = 30
PUNTOS_ENEMIGO_DISPARADOR = 50
PUNTOS_COFRE_RESUELTO = 100
PUNTOS_NIVEL_COMPLETADO = 500
BONUS_TUNEL_ENEMIGO = 10
PUNTOS_EXPLORACION = 25
PUNTOS_MISION_BASE = 50

# Sistema de daño
DANO_ENEMIGO_NORMAL = 1
DANO_ENEMIGO_TUNEL = 2
DANO_BALA_ENEMIGA_NORMAL = 1
DANO_BALA_ENEMIGA_FUEGO = 2
DANO_BALA_ENEMIGA_TUNEL = 3

# Sistema de experiencia
EXPERIENCIA_ENEMIGO_BASICO = 10
EXPERIENCIA_ENEMIGO_CAMUFLADO = 15
EXPERIENCIA_ENEMIGO_DISPARADOR = 25
EXPERIENCIA_COFRE = 20
EXPERIENCIA_EXPLORACION = 15
EXPERIENCIA_MISION = 50
EXPERIENCIA_NIVEL_BASE = 100  # Experiencia necesaria para subir de nivel

# ==================== SISTEMA DE MUNDO ====================
NUM_AREAS_MUNDO = 8
PROBABILIDAD_ENEMIGO = 0.1
PROBABILIDAD_COFRE = 0.05
PROBABILIDAD_NPC = 0.02

# Tipos de áreas actualizados con nueva progresión
TIPOS_AREAS = ["bosque", "lago", "montaña", "pantano", "pueblo", "aldea", "cueva", "ruinas", "mazmorra", "castillo", "reino", "capital"]

# Peligrosidad por tipo de área (1-10)
PELIGROSIDAD_AREAS = {
    "bosque": 2,
    "lago": 1,
    "montaña": 3,
    "pantano": 4,
    "pueblo": 1,  # Seguro
    "aldea": 2,   # Un poco más peligroso
    "cueva": 5,
    "ruinas": 6,
    "mazmorra": 8,
    "castillo": 4,  # Defendido pero no muy peligroso
    "reino": 3,     # Seguro
    "capital": 1    # Muy seguro
}

# Recursos por área
RECURSOS_AREAS = {
    "bosque": ["madera", "hierbas", "frutas", "setas", "flores"],
    "lago": ["peces", "agua", "algas", "piedras lisas", "conchas"],
    "montaña": ["piedras", "cristales", "hierro", "carbón", "cobre"],
    "pantano": ["hongos", "raíces", "hierbas raras", "barro", "fósiles"],
    "pueblo": ["comida", "herramientas", "telas", "cerámica", "velas"],
    "aldea": ["pociones", "libros", "mapas", "instrumentos", "joyas"],
    "cueva": ["minerales", "gemas", "fósiles", "cristales", "huesos"],
    "ruinas": ["artefactos", "libros antiguos", "mapas", "joyas", "armas"],
    "mazmorra": ["tesoros", "armas mágicas", "pociones raras", "gemas", "libros prohibidos"],
    "castillo": ["armaduras", "espadas", "escudos", "joyas reales", "documentos"],
    "reino": ["oro", "plata", "sedas", "especias", "vino"],
    "capital": ["tesoro real", "artefactos sagrados", "libros de conocimiento", "mapas mundiales", "reliquias"]
}

# ==================== SISTEMA DE MISIONES ====================
# Añadir misiones de progresión
MISIONES_PROGRESION = {
    "explorar_bosque": "Explora 3 áreas de la naturaleza",
    "llegar_pueblo": "Encuentra y llega al Pueblo Principal",
    "rescatar_aldeano": "Rescata a un aldeano secuestrado en las cuevas",
    "explorar_ruinas": "Explora las Ruinas Antiguas",
    "derrotar_guardian": "Derrota al Guardián de la Mazmorra",
    "llegar_castillo": "Llega al Castillo Real",
    "salvar_reino": "Salva al Reino de la amenaza oscura"
}

# ==================== SISTEMA DE MISIONES ====================
NUM_MISIONES_SIMULTANEAS = 3
TIEMPO_MISION = 300  # 5 minutos en segundos para misiones con tiempo
RECOMPENSA_MISION_BASE = 100
RECOMPENSA_MISION_EXTRA = 50

# Tipos de misiones
TIPOS_MISIONES = ["matar", "recolectar", "resolver", "explorar", "entregar"]

# ==================== SISTEMA DE NPCs ====================
NPC_TIPOS = ["profesor", "aldeano", "comerciante", "explorador", "guerrero", "mago", "arquero", "curandero"]
NPC_NOMBRES = ["Mateo", "Sofía", "Carlos", "Ana", "Luis", "María", "Pedro", "Laura", "David", "Elena"]

# ==================== SISTEMA DE TIENDA ====================
PRECIOS_TIENDA = {
    "pocion_vida": 50,
    "balas_extra": 30,
    "mapa": 100,
    "llave": 150,
    "pocion_velocidad": 75,
    "pocion_fuerza": 80,
    "pocion_defensa": 70,
    "mapa_mundial": 200,
    "brujula": 120,
    "antidoto": 60
}

# ==================== SISTEMA DE INVENTARIO ====================
INVENTARIO_MAXIMO = 20
POCION_VIDA_CURACION = 1
POCION_VELOCIDAD_DURACION = 30000  # 30 segundos en milisegundos
POCION_VELOCIDAD_BONUS = 2

# ==================== CONFIGURACIÓN DE CONTROLES ====================
# Usar códigos numéricos ya que pygame no está inicializado aquí
TECLA_ARRIBA = 119           # w
TECLA_ABAJO = 115            # s
TECLA_IZQUIERDA = 97         # a
TECLA_DERECHA = 100          # d
TECLA_DISPARAR = 1           # Click izquierdo
TECLA_INTERACTUAR = 101      # e
TECLA_RECARGAR = 114         # r
TECLA_REINICIAR = 102        # f
TECLA_MAPA = 109             # m
TECLA_MISIONES = 113         # q
TECLA_INVENTARIO = 105       # i
TECLA_TIENDA = 116           # t
TECLA_ESTADISTICAS = 117     # u
TECLA_CONTROLES = 9          # TAB
TECLA_ZOOM_MAS = 43          # +
TECLA_ZOOM_MENOS = 45        # -
TECLA_ZOOM_NORMAL = 122      # z
TECLA_VELOCIDAD_MAS = 50     # 2
TECLA_VELOCIDAD_MENOS = 49   # 1
TECLA_VELOCIDAD_DEFAULT = 48 # 0
TECLA_LUZ_TOGGLE = 108       # l
TECLA_SALIR = 27             # ESC
TECLA_SIGUIENTE_DIALOGO = 32 # ESPACIO
TECLA_ACEPTAR_MISION = 13    # ENTER
TECLA_CANCELAR_MISION = 8    # BACKSPACE

# Teclas para cambiar de área (1-8)
TECLA_AREA_1 = 49  # 1
TECLA_AREA_2 = 50  # 2
TECLA_AREA_3 = 51  # 3
TECLA_AREA_4 = 52  # 4
TECLA_AREA_5 = 53  # 5
TECLA_AREA_6 = 54  # 6
TECLA_AREA_7 = 55  # 7
TECLA_AREA_8 = 56  # 8

# ==================== CONFIGURACIÓN DE DEBUG ====================
MOSTRAR_FPS = True
MOSTRAR_COORDENADAS = False
MOSTRAR_COLISIONES = False
MOSTRAR_AREAS = True
MODO_DIOS = False
MOSTRAR_INFO_AREAS = False
MOSTRAR_CURSOR = True
MOSTRAR_HITBOXES = False
MOSTRAR_DEBUG_MISIONES = False
MOSTRAR_DEBUG_NPCS = False

# ==================== CONFIGURACIÓN DE SONIDO ====================
VOLUMEN_GENERAL = 0.7
VOLUMEN_MUSICA = 0.5
VOLUMEN_EFECTOS = 0.8
HABILITAR_SONIDO = True

# ==================== CONFIGURACIÓN DE EFECTOS ====================
TIEMPO_TRANSICION = 1000  # 1 segundo para transiciones entre áreas
ALPHA_TRANSICION = 180
TIEMPO_MENSAJE = 3000     # 3 segundos para mensajes
TIEMPO_DIALOGO = 5000     # 5 segundos para diálogos

# ==================== CONSTANTES DE RENDIMIENTO ====================
LIMITE_ENEMIGOS = 20
LIMITE_BALAS = 30
LIMITE_PARTICULAS = 50
LIMITE_DECALS = 100

# ==================== CONSTANTES DE UI ====================
TAM_FUENTE_TITULO = 48
TAM_FUENTE_SUBTITULO = 32
TAM_FUENTE_NORMAL = 24
TAM_FUENTE_PEQUEÑA = 18
TAM_FUENTE_MUY_PEQUEÑA = 14

MARGEN_UI = 10
ESPACIADO_ELEMENTOS = 5
GROSOR_BORDE = 2
RADIO_ESQUINAS = 8

# Colores UI
COLOR_FONDO_MENU = (40, 40, 60, 230)
COLOR_FONDO_PANEL = (30, 30, 45, 220)
COLOR_FONDO_INVENTARIO = (50, 40, 60, 240)
COLOR_FONDO_DIALOGO = (20, 20, 30, 240)
COLOR_BORDE = (100, 100, 150, 255)
COLOR_RESALTADO = (255, 215, 0, 100)
COLOR_SELECCION = (100, 200, 255, 150)

# ==================== CONFIGURACIÓN DE SISTEMA ====================
VERSION_JUEGO = "1.0.0"
AUTOR = "Equipo Matemático"
NOMBRE_JUEGO = "Mundo Libre Matemático"
DESCRIPCION_JUEGO = "Un juego educativo RPG donde las matemáticas te ayudan a explorar un mundo lleno de aventuras"

# ==================== MENSAJES DEL JUEGO ====================
MENSAJES_BIENVENIDA = [
    "¡Bienvenido al Mundo Libre Matemático!",
    "Usa las matemáticas para resolver problemas y avanzar en tu aventura.",
    "Habla con los NPCs para obtener misiones.",
    "Presiona 'M' para ver el mapa mundial.",
    "Presiona 'Q' para ver tus misiones activas.",
    "Presiona 'I' para abrir tu inventario.",
    "Presiona 'E' para interactuar con objetos y personajes.",
    "¡Diviértete aprendiendo matemáticas!"
]

MENSAJES_NPC = {
    "profesor": [
        "El conocimiento es poder, joven aventurero.",
        "¿Resolviste el problema que te di?",
        "La práctica hace al maestro, no te rindas.",
        "Cada problema resuelto te acerca a la sabiduría."
    ],
    "comerciante": [
        "¡Bienvenido a mi tienda!",
        "¿Necesitas suministros para tu aventura?",
        "Los mejores precios de toda la región.",
        "Vuelve pronto, siempre tengo nuevas mercancías."
    ]
}

print(f"⚙️ Configuración cargada - {NOMBRE_JUEGO} v{VERSION_JUEGO}")
print(f"📐 Resolución por defecto: {ANCHO}x{ALTO}")
print(f"🎮 Pantalla completa: {'SÍ' if PANTALLA_COMPLETA else 'NO'}")
print(f"🌍 Sistema: Mundo Libre con {NUM_AREAS_MUNDO} áreas")
print(f"🎯 Sistema de Misiones: {len(TIPOS_MISIONES)} tipos")
print(f"👥 NPCs: {len(NPC_TIPOS)} tipos diferentes")
print("=" * 60)
print(f"📖 {DESCRIPCION_JUEGO}")
print("=" * 60)
