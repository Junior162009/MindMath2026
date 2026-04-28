# niveles.py - 10 NIVELES COMPLETOS + JEFE FINAL ÉPICO
import random

# =============================================================
# SISTEMA DE SÍMBOLOS DEL MAPA
# =============================================================
# 1  = Pared de piedra
# 0  = Suelo normal (iluminado)
# T  = Túnel oscuro
# P  = Posición inicial del jugador
# D  = Puerta / salida del nivel
# C  = Cofre (requiere resolver operación matemática)
# E  = Enemigo básico (rojo)
# G  = Enemigo camuflado (verde)
# S  = Enemigo disparador (azul)
# B  = Jefe final (BOSS)
# N  = NPC (personaje no jugable)
# =============================================================

# ─────────────────────────────────────────────────────────────
# NIVEL 0 — PUEBLO INICIAL (Tutorial)
# Objetivo: Aprender los controles. Sin enemigos.
# ─────────────────────────────────────────────────────────────
NIVEL_0 = [
    "1111111111111111111111111",
    "1N      C         N    1",
    "1   111111   111111    1",
    "1   1    1   1    1    1",
    "1   1    1   1    1    1",
    "1   111111   111111    1",
    "1       C               D",
    "1   P           C      1",
    "1       N              1",
    "1111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 1 — LA PRIMERA CUEVA (Introducción al combate)
# Objetivo: Elimina los enemigos y resuelve 2 cofres.
# ─────────────────────────────────────────────────────────────
NIVEL_1 = [
    "1111111111111111111111",
    "1P  0  0  0  0  0  01",
    "1  E        C       1",
    "1  111111111111111  1",
    "1  1000000000000 1  1",
    "1  1  E   C    1 1  1",
    "1  1000000000001 1  1",
    "1  111111111111  1  1",
    "1       E            D",
    "1111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 2 — TÚNELES ESTRECHOS
# Objetivo: Navega los túneles oscuros. Cuidado con los camuflados.
# ─────────────────────────────────────────────────────────────
NIVEL_2 = [
    "111111111111111111111111",
    "1P 0 0 0 0 0 0 0 0 001",
    "1  1111111111111111  1",
    "1  1TTTTTTTTTTTTTT1  1",
    "1  1T G C   C   T1  1",
    "1  1TTTTTTTTTTTTT1  1",
    "1  1111111111111 1  1",
    "1  0 0 E 0 0 C 0 1  1",
    "1  1111111111111111  D",
    "111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 3 — LABERINTO DE PIEDRA
# Objetivo: Encuentra la salida entre los pasillos. 3 cofres obligatorios.
# ─────────────────────────────────────────────────────────────
NIVEL_3 = [
    "11111111111111111111111111",
    "1P 0 0 0 1 0 0 0 0 0 011",
    "1        1             1",
    "111111   1   111111111 1",
    "1    1   1   1         1",
    "1 C  1   1   1   E     1",
    "1    11111   111111111 1",
    "1  E         G     C   1",
    "1111111111   111111111 1",
    "1     C  1   1    S    1",
    "1 E      1   1         D",
    "11111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 4 — CATACUMBAS MALDITAS
# Objetivo: Las sombras ocultan enemigos camuflados por doquier.
# ─────────────────────────────────────────────────────────────
NIVEL_4 = [
    "111111111111111111111111111",
    "1P  0  0 TTTTTTT 0  0   1",
    "1   E    T G C T  E     1",
    "1        TTTTTTT        1",
    "111111111111111111111111 1",
    "1 C   G     TTTTT  S    1",
    "1      111  T E T  11111 1",
    "1      1 1  TTTTT  1     1",
    "1  E   1 1    C    1  C  1",
    "1      111111111111111   1",
    "1  G          E         D",
    "111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 5 — FORTALEZA DE HIELO
# Objetivo: Supera las cámaras selladas. Disparadores en patrulla.
# ─────────────────────────────────────────────────────────────
NIVEL_5 = [
    "1111111111111111111111111111",
    "1P  0  0   0  0   0  0  01",
    "1   11111  1111  11111   1",
    "1   1 S 1  1C 1  1 S 1  1",
    "1   11111  1111  11111  1",
    "1     C    E  E     C   1",
    "1   11111  1111  11111  1",
    "1   1 E 1  1  1  1 C 1  1",
    "1   11111  1111  11111   1",
    "1  0  0  0    0  0  0    D",
    "1111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 6 — MINAS ABANDONADAS
# Objetivo: Explora las galerías. Todo el mapa está en túnel oscuro.
# ─────────────────────────────────────────────────────────────
NIVEL_6 = [
    "11111111111111111111111111111",
    "1P TTTTTTTTTTTTTTTTTTTTTT 1",
    "1  TTTTTTTTTTTTTTTTTTTTTT 1",
    "1  TT1111111111111111TTTT 1",
    "1  TT1 G  C   C  S 1TTTT 1",
    "1  TT1 11111111111 1TTTT 1",
    "1  TT1 1         1 1TTTT 1",
    "1  TT1 1  E  C   1 1TTTT 1",
    "1  TT1 1         1 1TTTT 1",
    "1  TT1 11111111111 1TTTT 1",
    "1  TT1 G  C   E  S 1TTTT D",
    "1  TTTTTTTTTTTTTTTTTTTTTT 1",
    "11111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 7 — TEMPLO ANTIGUO
# Objetivo: Resuelve los 5 cofres sagrados para activar la puerta.
# ─────────────────────────────────────────────────────────────
NIVEL_7 = [
    "111111111111111111111111111111",
    "1P   0   0   0   0   0   001",
    "1   111 111 111 111 111    1",
    "1   1C1 1E1 1C1 1S1 1C1   1",
    "1   111 111 111 111 111   1",
    "1    G    E   C   E   G   1",
    "1   TTTTTTTTTTTTTTTTTTTT  1",
    "1   T  E  G  C  G  S   T 1",
    "1   TTTTTTTTTTTTTTTTTTTT  1",
    "1    C   S    E   C   G   1",
    "1   0  0  0  0  0  0  0   D",
    "111111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 8 — CIUDADELA EN RUINAS
# Objetivo: Avanza por las tres salas y derrota las oleadas.
# ─────────────────────────────────────────────────────────────
NIVEL_8 = [
    "1111111111111111111111111111111",
    "1P  0  0  1111111111 0  0  01",
    "1  E   E  1 S  C  S 1  E    1",
    "1         1         1       1",
    "1  C  11111111111111111  C  1",
    "1     1 G  T T T  G 1       1",
    "1     1    TTTTTTT  1       1",
    "1  S  1 G  T C C T  1  S    1",
    "1     1    TTTTTTT  1       1",
    "1     1 S  T T T  S 1       1",
    "1  C  11111111111111111  C  1",
    "1         1         1       1",
    "1  E   E  1  S  C  S 1  E  D",
    "1111111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 9 — ANTECÁMARA DEL INFIERNO
# Objetivo: El preámbulo del jefe. Maximiza tu equipo antes del final.
# ─────────────────────────────────────────────────────────────
NIVEL_9 = [
    "11111111111111111111111111111111",
    "1P  0  TTTTTTTTTTTTTTTTTTT  01",
    "1      TTTTTTTTTTTTTTTTTTT   1",
    "1  C   TT111111111111111TT   1",
    "1      TT1 S  C  C  S  1TT   1",
    "1  S   TT1             1TT   1",
    "1      TT1  G  E  G  E  1TT  1",
    "1  C   TT1             1TT   1",
    "1      TT1  S  C  C  S  1TT  1",
    "1      TT111111111111111TT   1",
    "1  G   TTTTTTTTTTTTTTTTTTT   1",
    "1  S          C   S   C      1",
    "1  G    E  E  G   E   G  S   D",
    "11111111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# NIVEL 10 — SALA DEL JEFE FINAL (El Liche Matemático)
# Objetivo: ¡Derrota al Liche! Resuelve sus 6 cofres y elimina al jefe.
# El jefe "B" ocupa un espacio 3x3 de tiles (se maneja en jefe.py)
# ─────────────────────────────────────────────────────────────
NIVEL_10_BOSS = [
    "1111111111111111111111111111111111111",
    "1   0   0   0   0   0   0   0   001",
    "1                                  1",
    "1  C    E   S   E   S   E   C      1",
    "1                                  1",
    "1  111111111111111111111111111111   1",
    "1  1                            1  1",
    "1  1   E    G    E    G    E    1  1",
    "1  1                            1  1",
    "1  1         B B B              1  1",
    "1  1         B B B              1  1",
    "1  1         B B B              1  1",
    "1  1                            1  1",
    "1  1   E    G    E    G    E    1  1",
    "1  1                            1  1",
    "1  111111111111111111111111111111   1",
    "1                                  1",
    "1  C    S   E   S   E   S   C      1",
    "1                                  1",
    "1P  0   0   0   0   0   0   0   0  D",
    "1111111111111111111111111111111111111",
]

# ─────────────────────────────────────────────────────────────
# DICCIONARIO PRINCIPAL DE NIVELES
# ─────────────────────────────────────────────────────────────
NIVELES = {
    0:  NIVEL_0,
    1:  NIVEL_1,
    2:  NIVEL_2,
    3:  NIVEL_3,
    4:  NIVEL_4,
    5:  NIVEL_5,
    6:  NIVEL_6,
    7:  NIVEL_7,
    8:  NIVEL_8,
    9:  NIVEL_9,
    10: NIVEL_10_BOSS,
}

# ─────────────────────────────────────────────────────────────
# METADATOS DE NIVELES (para HUD, narración y progresión)
# ─────────────────────────────────────────────────────────────
NIVEL_INFO = {
    0: {
        "nombre": "Pueblo de Inicio",
        "descripcion": "Un pueblo tranquilo donde comienza tu aventura.",
        "objetivo": "Habla con los aldeanos y aprende los controles.",
        "tipo": "tutorial",
        "musica": "pueblo",
        "es_boss": False,
    },
    1: {
        "nombre": "La Primera Cueva",
        "descripcion": "Cavernas húmedas al norte del pueblo.",
        "objetivo": "Elimina los enemigos y abre 2 cofres.",
        "tipo": "cueva",
        "musica": "cueva",
        "es_boss": False,
    },
    2: {
        "nombre": "Túneles Estrechos",
        "descripcion": "Pasajes angostos donde la oscuridad es tu enemigo.",
        "objetivo": "Atraviesa los túneles. Cuidado con los Camuflados.",
        "tipo": "tunel",
        "musica": "cueva",
        "es_boss": False,
    },
    3: {
        "nombre": "Laberinto de Piedra",
        "descripcion": "Un laberinto construido por civilizaciones antiguas.",
        "objetivo": "Encuentra la salida. Abre los 3 cofres obligatorios.",
        "tipo": "laberinto",
        "musica": "ruinas",
        "es_boss": False,
    },
    4: {
        "nombre": "Catacumbas Malditas",
        "descripcion": "Las sombras aquí están vivas. Siente cómo te observan.",
        "objetivo": "Derrota a todos los Camuflados y escapa.",
        "tipo": "catacumba",
        "musica": "oscuro",
        "es_boss": False,
    },
    5: {
        "nombre": "Fortaleza de Hielo",
        "descripcion": "Una fortaleza helada con habitaciones selladas.",
        "objetivo": "Supera las cámaras y esquiva los disparadores.",
        "tipo": "fortaleza",
        "musica": "hielo",
        "es_boss": False,
    },
    6: {
        "nombre": "Minas Abandonadas",
        "descripcion": "Galerías que nunca ven la luz del día.",
        "objetivo": "Navega en completa oscuridad. ¡Conserva tus balas!",
        "tipo": "mina",
        "musica": "oscuro",
        "es_boss": False,
    },
    7: {
        "nombre": "Templo Antiguo",
        "descripcion": "Un templo donde los acertijos matemáticos abren puertas.",
        "objetivo": "Resuelve los 5 cofres sagrados para avanzar.",
        "tipo": "templo",
        "musica": "misterio",
        "es_boss": False,
    },
    8: {
        "nombre": "Ciudadela en Ruinas",
        "descripcion": "Lo que quedó de una gran fortaleza tras la guerra.",
        "objetivo": "Limpia las tres salas de enemigos.",
        "tipo": "ciudadela",
        "musica": "batalla",
        "es_boss": False,
    },
    9: {
        "nombre": "Antecámara del Infierno",
        "descripcion": "La sala previa al jefe final. Todo está más oscuro aquí.",
        "objetivo": "Recarga balas, pociones y prepárate para el jefe final.",
        "tipo": "antecamara",
        "musica": "tension",
        "es_boss": False,
    },
    10: {
        "nombre": "Sala del Liche Matemático",
        "descripcion": "¡EL JEFE FINAL! El Liche Matemático controla esta sala.",
        "objetivo": "Resuelve sus 6 cofres y derrota al Liche para GANAR.",
        "tipo": "boss",
        "musica": "boss",
        "es_boss": True,
    },
}

# ─────────────────────────────────────────────────────────────
# OBJETIVOS GLOBALES DEL JUEGO (para panel de misiones)
# ─────────────────────────────────────────────────────────────
OBJETIVOS_JUEGO = {
    "historia": [
        "📖 Habla con el Anciano en el Pueblo de Inicio.",
        "🗺️ Explora los 10 niveles del mundo.",
        "🔑 Abre al menos 20 cofres resolviendo operaciones.",
        "⚔️ Elimina a 50 enemigos en total.",
        "💀 Derrota al Liche Matemático para salvar el reino.",
    ],
    "secundarios": [
        "🌟 Sube al nivel 5 de experiencia.",
        "🧪 Usa 10 pociones de vida.",
        "🎯 Completa cada nivel sin perder una vida.",
        "🔫 Dispara 200 balas.",
        "👾 Elimina un enemigo de cada tipo (Básico, Camuflado, Disparador).",
    ],
    "logros": [
        "🏆 'Sin rasguños' — Termina un nivel con todas las vidas.",
        "🏆 'Matemático' — Resuelve 10 cofres correctos seguidos.",
        "🏆 'Fantasma' — Termina el nivel 6 (minas) sin ser golpeado.",
        "🏆 'Exterminador' — Elimina todos los enemigos del nivel 9.",
        "🏆 'Héroe del Reino' — Derrota al Liche Matemático.",
    ],
}

# ─────────────────────────────────────────────────────────────
# HISTORIA NARRATIVA (texto mostrado entre niveles)
# ─────────────────────────────────────────────────────────────
NARRATIVA = {
    "intro": (
        "En el reino de Matemia, una oscuridad antigua despertó.\n"
        "El Liche Matemático sellò su conocimiento en cofres mágicos\n"
        "dispersos por todo el mundo.\n\n"
        "Solo quien resuelva sus enigmas podrá detenerlo.\n"
        "Tú eres esa persona. ¡Comienza tu aventura!"
    ),
    1: "Las cavernas susurran acertijos. El primer cofre brilla en la oscuridad...",
    2: "Los túneles se estrechan. Los Camuflados se funden con las sombras.",
    3: "El laberinto fue construido para guardar el conocimiento. Encuentras la salida.",
    4: "Las catacumbas huelen a magia antigua. Las sombras tienen ojos.",
    5: "La fortaleza helada cruje bajo tus pies. Los Disparadores esperan.",
    6: "Las minas te engullen. Solo tu linterna te guía en la oscuridad total.",
    7: "El templo revela sus secretos. Cinco cofres sagrados guardan el paso.",
    8: "La ciudadela cayó hace siglos. Sus guardianes aún obedecen al Liche.",
    9: (
        "Sientes el calor del más allá. Al otro lado de esa puerta...\n"
        "...el Liche Matemático te espera.\n\n"
        "Prepárate. Esta es tu última oportunidad."
    ),
    10: (
        "¡EL LICHE MATEMÁTICO!\n\n"
        "'¿Crees que puedes vencerme, pequeño mortal?\n"
        "¡Resuelve mis enigmas si te atreves!'\n\n"
        "Derrótalo para salvar el reino de Matemia."
    ),
    "victoria": (
        "¡Lo lograste! El Liche Matemático ha sido derrotado.\n\n"
        "Su conocimiento se libera y la oscuridad retrocede.\n"
        "El reino de Matemia celebra al nuevo héroe matemático.\n\n"
        "¡Felicidades, has completado el juego!"
    ),
}

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE DIFICULTAD POR NIVEL
# ─────────────────────────────────────────────────────────────
DIFICULTAD_NIVEL = {
    0:  {"multiplicador_puntos": 1.0, "vida_bonus": 2, "balas_bonus": 10, "ops_tipo": ["suma"]},
    1:  {"multiplicador_puntos": 1.0, "vida_bonus": 0, "balas_bonus": 5,  "ops_tipo": ["suma", "resta"]},
    2:  {"multiplicador_puntos": 1.2, "vida_bonus": 0, "balas_bonus": 5,  "ops_tipo": ["suma", "resta"]},
    3:  {"multiplicador_puntos": 1.4, "vida_bonus": 1, "balas_bonus": 5,  "ops_tipo": ["suma", "resta", "multiplicacion"]},
    4:  {"multiplicador_puntos": 1.6, "vida_bonus": 0, "balas_bonus": 3,  "ops_tipo": ["suma", "resta", "multiplicacion"]},
    5:  {"multiplicador_puntos": 1.8, "vida_bonus": 1, "balas_bonus": 5,  "ops_tipo": ["resta", "multiplicacion"]},
    6:  {"multiplicador_puntos": 2.0, "vida_bonus": 0, "balas_bonus": 3,  "ops_tipo": ["multiplicacion", "division"]},
    7:  {"multiplicador_puntos": 2.2, "vida_bonus": 1, "balas_bonus": 5,  "ops_tipo": ["multiplicacion", "division"]},
    8:  {"multiplicador_puntos": 2.5, "vida_bonus": 0, "balas_bonus": 3,  "ops_tipo": ["division", "potencia"]},
    9:  {"multiplicador_puntos": 2.8, "vida_bonus": 2, "balas_bonus": 10, "ops_tipo": ["potencia", "raiz"]},
    10: {"multiplicador_puntos": 5.0, "vida_bonus": 0, "balas_bonus": 0,  "ops_tipo": ["potencia", "raiz", "mixta"]},
}

# ─────────────────────────────────────────────────────────────
# FUNCIONES DE UTILIDAD
# ─────────────────────────────────────────────────────────────

TOTAL_NIVELES = len(NIVELES)
NIVEL_BOSS = 10


def obtener_nivel(numero):
    """Obtiene el mapa de un nivel por número (0-10)."""
    return NIVELES.get(numero, NIVELES[10])


def obtener_info(numero):
    """Devuelve el diccionario de info del nivel."""
    return NIVEL_INFO.get(numero, NIVEL_INFO[10])


def obtener_dificultad(numero):
    """Devuelve la configuración de dificultad del nivel."""
    return DIFICULTAD_NIVEL.get(numero, DIFICULTAD_NIVEL[10])


def obtener_narrativa(numero):
    """Devuelve el texto narrativo entre niveles."""
    return NARRATIVA.get(numero, "")


def es_nivel_boss(numero):
    """Devuelve True si el nivel es el de jefe final."""
    return numero == NIVEL_BOSS


def contar_elementos(nivel_data, simbolo):
    """Cuenta cuántas veces aparece un símbolo en el nivel."""
    return sum(fila.count(simbolo) for fila in nivel_data)


def lista_niveles():
    """Devuelve información resumida de todos los niveles."""
    info = []
    for i in sorted(NIVELES.keys()):
        nivel = NIVELES[i]
        meta = NIVEL_INFO[i]
        info.append({
            "numero": i,
            "nombre": meta["nombre"],
            "tipo": meta["tipo"],
            "filas": len(nivel),
            "columnas": max(len(f) for f in nivel),
            "cofres": contar_elementos(nivel, "C"),
            "enemigos_basicos": contar_elementos(nivel, "E"),
            "enemigos_camuflados": contar_elementos(nivel, "G"),
            "disparadores": contar_elementos(nivel, "S"),
            "boss": contar_elementos(nivel, "B"),
            "tuneles": contar_elementos(nivel, "T"),
            "puertas": contar_elementos(nivel, "D"),
            "es_boss": meta["es_boss"],
            "objetivo": meta["objetivo"],
        })
    return info


# ─────────────────────────────────────────────────────────────
# DIAGNÓSTICO RÁPIDO (ejecutar directo: python niveles.py)
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("   MUNDO LIBRE MATEMÁTICO — DIAGNÓSTICO DE NIVELES")
    print("=" * 65)
    for nivel in lista_niveles():
        marcador_boss = " 👑 JEFE FINAL" if nivel["es_boss"] else ""
        print(f"\n🗺️  Nivel {nivel['numero']:>2} — {nivel['nombre']}{marcador_boss}")
        print(f"   Tipo      : {nivel['tipo']}")
        print(f"   Tamaño    : {nivel['columnas']}x{nivel['filas']}")
        print(f"   Cofres    : {nivel['cofres']}")
        print(f"   Enemigos  : Básico={nivel['enemigos_basicos']}  "
              f"Camuflado={nivel['enemigos_camuflados']}  "
              f"Disparador={nivel['disparadores']}  "
              f"Boss={nivel['boss']}")
        print(f"   Túneles   : {nivel['tuneles']}")
        print(f"   Puertas   : {nivel['puertas']}")
        print(f"   Objetivo  : {nivel['objetivo']}")
    print("\n" + "=" * 65)
    print(f"   Total de niveles  : {TOTAL_NIVELES}")
    print(f"   Nivel del jefe    : {NIVEL_BOSS}")
    print("=" * 65)
