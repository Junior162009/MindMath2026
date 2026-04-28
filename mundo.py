# mundo.py - MUNDO CON PROGRESIÓN NATURAL
import pygame
import random
from settings import *

class AreaMundo:
    def __init__(self, id_area, nombre, tipo, tamaño, peligrosidad, recursos, es_segura=False):
        self.id = id_area
        self.nombre = nombre
        self.tipo = tipo
        self.tamaño = tamaño
        self.peligrosidad = peligrosidad
        self.recursos = recursos
        self.es_segura = es_segura  # Si es área segura (sin enemigos)
        self.explorada = False
        self.posicion = (0, 0)
        self.conexiones = []
        self.mapa = None
        self.descripcion = self.generar_descripcion()

    def generar_descripcion(self):
        """Genera una descripción única para el área"""
        descripciones = {
            "bosque": [
                "Un denso bosque lleno de vida y misterios.",
                "Árboles antiguos cubren este bosque tranquilo.",
                "El canto de los pájaros llena el aire fresco."
            ],
            "lago": [
                "Un lago cristalino rodeado de naturaleza.",
                "Las aguas tranquilas reflejan el cielo.",
                "Peces saltan en la superficie del lago."
            ],
            "montaña": [
                "Montañas imponentes con vistas espectaculares.",
                "El aire es fresco en estas alturas.",
                "Sendero escarpado que lleva a la cima."
            ],
            "pantano": [
                "Un pantano misterioso con niebla perpetua.",
                "Sonidos extraños provienen de las profundidades.",
                "Debes tener cuidado donde pisas aquí."
            ],
            "pueblo": [
                "Un pueblo acogedor con gente amable.",
                "Hogar de artesanos y comerciantes.",
                "El centro de la comunidad local."
            ],
            "aldea": [
                "Una pequeña aldea en medio del bosque.",
                "Casas sencillas y vida tranquila.",
                "Los aldeanos viven en armonía con la naturaleza."
            ],
            "cueva": [
                "Cueva oscura con eco misterioso.",
                "Minerales brillan en la oscuridad.",
                "Profundidades desconocidas te esperan."
            ],
            "ruinas": [
                "Ruinas de una civilización antigua.",
                "Arquitectura perdida en el tiempo.",
                "Secretos esperan ser descubiertos."
            ],
            "mazmorra": [
                "Mazmorra oscura llena de peligros.",
                "Los ecos de pasos resuenan en la piedra.",
                "Tesoros y trampas te esperan."
            ],
            "castillo": [
                "Imponente castillo con altas murallas.",
                "Sede del poder regional.",
                "Guardado por soldados leales."
            ],
            "reino": [
                "Vastas tierras del reino.",
                "Campos fértiles y caminos seguros.",
                "El corazón de la civilización."
            ],
            "capital": [
                "La gran capital del reino.",
                "Centro de comercio y cultura.",
                "Donde reina el conocimiento y la prosperidad."
            ]
        }
        return random.choice(descripciones.get(self.tipo, ["Un lugar misterioso."]))

    def generar_mapa(self):
        """Genera un mapa procedural para el área según su tipo"""
        ancho, alto = self.tamaño
        mapa = []

        # Generar según el tipo de área
        if self.tipo == "bosque":
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "1"  # Árboles en el borde
                    elif random.random() < 0.25:  # Árboles
                        fila += "1"
                    elif random.random() < 0.05 and not self.es_segura:  # Enemigos
                        fila += "E"
                    elif random.random() < 0.04:  # Cofres
                        fila += "C"
                    elif random.random() < 0.03:  # NPCs
                        fila += "N"
                    elif random.random() < 0.02:  # Puertas
                        fila += "D"
                    else:
                        fila += "0"  # Suelo con hierba
                mapa.append(fila)

        elif self.tipo == "lago":
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "1"
                    elif random.random() < 0.15:  # Rocas/Islas
                        fila += "1"
                    elif random.random() < 0.03 and not self.es_segura:  # Enemigos acuáticos
                        fila += "E"
                    elif random.random() < 0.04:  # Cofres (tesoros hundidos)
                        fila += "C"
                    elif random.random() < 0.02:  # NPCs pescadores
                        fila += "N"
                    elif random.random() < 0.03:  # Puentes/Puertas
                        fila += "D"
                    else:
                        fila += " "  # Agua
                mapa.append(fila)

        elif self.tipo == "montaña":
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "#"  # Pared de montaña
                    elif random.random() < 0.30:  # Rocas
                        fila += "#"
                    elif random.random() < 0.06 and not self.es_segura:  # Enemigos de montaña
                        fila += "E"
                    elif random.random() < 0.05:  # Cofres (minerales)
                        fila += "C"
                    elif random.random() < 0.02:  # NPCs montañeses
                        fila += "N"
                    elif random.random() < 0.04:  # Puertas (entradas a cuevas)
                        fila += "D"
                    else:
                        fila += "0"  # Sendero de montaña
                mapa.append(fila)

        elif self.tipo in ["pueblo", "aldea"]:
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "1"  # Murallas/cercas
                    elif random.random() < 0.20:  # Casas
                        fila += "1"
                    elif random.random() < 0.08:  # Cofres
                        fila += "C"
                    elif random.random() < 0.10:  # NPCs (muchos en pueblos)
                        fila += "N"
                    elif random.random() < 0.01 and not self.es_segura:  # Pocos enemigos en pueblos
                        fila += "E"
                    elif random.random() < 0.05:  # Puertas (entradas/salidas)
                        fila += "D"
                    else:
                        fila += " "  # Calles/Plazas
                mapa.append(fila)

        elif self.tipo in ["cueva", "ruinas", "mazmorra"]:
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "#"  # Paredes sólidas
                    elif random.random() < 0.35:  # Paredes internas
                        fila += "#"
                    elif random.random() < 0.15:  # Enemigos (muchos en masmorras)
                        fila += "E"
                    elif random.random() < 0.08:  # Cofres (tesoros)
                        fila += "C"
                    elif random.random() < 0.01:  # NPCs (raros en masmorras)
                        fila += "N"
                    elif random.random() < 0.04:  # Puertas
                        fila += "D"
                    else:
                        fila += "0"  # Suelo
                mapa.append(fila)

        elif self.tipo in ["castillo", "reino", "capital"]:
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "1"  # Murallas
                    elif random.random() < 0.25:  # Edificios
                        fila += "1"
                    elif random.random() < 0.10:  # Cofres (tesoros reales)
                        fila += "C"
                    elif random.random() < 0.15:  # NPCs (muchos en ciudades)
                        fila += "N"
                    elif random.random() < 0.02 and not self.es_segura:  # Pocos enemigos
                        fila += "E"
                    elif random.random() < 0.06:  # Puertas
                        fila += "D"
                    else:
                        fila += " "  # Calles anchas
                mapa.append(fila)

        else:  # Para otros tipos
            for y in range(alto):
                fila = ""
                for x in range(ancho):
                    if x == 0 or x == ancho-1 or y == 0 or y == alto-1:
                        fila += "1"
                    elif random.random() < 0.20:
                        fila += "1"
                    elif random.random() < 0.07:
                        fila += "C"
                    elif random.random() < 0.05 and not self.es_segura:
                        fila += "E"
                    elif random.random() < 0.03:
                        fila += "N"
                    elif random.random() < 0.04:
                        fila += "D"
                    else:
                        fila += "0"
                mapa.append(fila)

        # Asegurar que hay una entrada para el jugador
        for intento in range(20):
            entrada_x = random.randint(1, ancho-2)
            entrada_y = random.randint(1, alto-2)
            if mapa[entrada_y][entrada_x] in [" ", "0"]:
                fila_lista = list(mapa[entrada_y])
                fila_lista[entrada_x] = "P"
                mapa[entrada_y] = "".join(fila_lista)
                break

        return mapa

class Mundo:
    def __init__(self):
        self.areas = {}
        self.area_actual = None
        self.generar_mundo_progresivo()
        self.progreso = 0  # 0: Naturaleza, 1: Pueblo, 2: Mazmorras, 3: Reino

    def generar_mundo_progresivo(self):
        """Genera un mundo con progresión natural"""

        # FASE 1: NATURALEZA (Áreas iniciales - seguras)
        areas_naturaleza = [
            AreaMundo(
                id_area=1,
                nombre="Bosque del Amanecer",
                tipo="bosque",
                tamaño=(20, 18),
                peligrosidad=2,
                recursos=RECURSOS_AREAS["bosque"],
                es_segura=True  # Área inicial segura
            ),
            AreaMundo(
                id_area=2,
                nombre="Lago Sereno",
                tipo="lago",
                tamaño=(18, 16),
                peligrosidad=1,
                recursos=RECURSOS_AREAS["lago"],
                es_segura=True
            ),
            AreaMundo(
                id_area=3,
                nombre="Colinas Verdes",
                tipo="montaña",
                tamaño=(22, 20),
                peligrosidad=3,
                recursos=RECURSOS_AREAS["montaña"]
            ),
            AreaMundo(
                id_area=4,
                nombre="Bosque Profundo",
                tipo="bosque",
                tamaño=(24, 22),
                peligrosidad=4,
                recursos=["madera", "hierbas", "frutas", "setas"]
            ),
        ]

        # FASE 2: PUEBLOS Y ALDEAS
        areas_pueblos = [
            AreaMundo(
                id_area=5,
                nombre="Aldea del Roble",
                tipo="aldea",
                tamaño=(25, 20),
                peligrosidad=2,
                recursos=RECURSOS_AREAS["aldea"],
                es_segura=True
            ),
            AreaMundo(
                id_area=6,
                nombre="Pueblo Principal",
                tipo="pueblo",
                tamaño=(30, 25),
                peligrosidad=1,
                recursos=RECURSOS_AREAS["pueblo"],
                es_segura=True
            ),
            AreaMundo(
                id_area=7,
                nombre="Mercado del Valle",
                tipo="pueblo",
                tamaño=(28, 22),
                peligrosidad=2,
                recursos=["comida", "herramientas", "telas", "cerámica"]
            ),
        ]

        # FASE 3: MAZMORRAS Y CUEVAS
        areas_mazmorras = [
            AreaMundo(
                id_area=8,
                nombre="Cueva del Eco",
                tipo="cueva",
                tamaño=(35, 30),
                peligrosidad=5,
                recursos=RECURSOS_AREAS["cueva"]
            ),
            AreaMundo(
                id_area=9,
                nombre="Ruinas Antiguas",
                tipo="ruinas",
                tamaño=(40, 35),
                peligrosidad=6,
                recursos=RECURSOS_AREAS["ruinas"]
            ),
            AreaMundo(
                id_area=10,
                nombre="Mazmorra del Olvido",
                tipo="mazmorra",
                tamaño=(45, 40),
                peligrosidad=8,
                recursos=RECURSOS_AREAS["mazmorra"]
            ),
        ]

        # FASE 4: REINO Y CAPITAL
        areas_reino = [
            AreaMundo(
                id_area=11,
                nombre="Castillo Real",
                tipo="castillo",
                tamaño=(50, 45),
                peligrosidad=4,
                recursos=RECURSOS_AREAS["castillo"],
                es_segura=True
            ),
            AreaMundo(
                id_area=12,
                nombre="Capital del Reino",
                tipo="capital",
                tamaño=(60, 50),
                peligrosidad=1,
                recursos=RECURSOS_AREAS["capital"],
                es_segura=True
            ),
        ]

        # Combinar todas las áreas
        todas_areas = areas_naturaleza + areas_pueblos + areas_mazmorras + areas_reino

        # Configurar conexiones progresivas
        conexiones = {
            1: [2, 3],    # Bosque conecta con Lago y Colinas
            2: [1, 4],    # Lago conecta con Bosque y Bosque Profundo
            3: [1, 5],    # Colinas conecta con Bosque y Aldea
            4: [2, 6],    # Bosque Profundo conecta con Lago y Pueblo
            5: [3, 6, 7], # Aldea conecta con Colinas, Pueblo y Mercado
            6: [4, 5, 8], # Pueblo conecta con Bosque, Aldea y Cueva
            7: [5, 8],    # Mercado conecta con Aldea y Cueva
            8: [6, 7, 9], # Cueva conecta con Pueblo, Mercado y Ruinas
            9: [8, 10],   # Ruinas conecta con Cueva y Mazmorra
            10: [9, 11],  # Mazmorra conecta con Ruinas y Castillo
            11: [10, 12], # Castillo conecta con Mazmorra y Capital
            12: [11]      # Capital conecta solo con Castillo
        }

        # Inicializar áreas
        for area in todas_areas:
            area.conexiones = conexiones.get(area.id, [])
            area.mapa = area.generar_mapa()
            self.areas[area.id] = area

        # Empezar en la naturaleza (Bosque del Amanecer)
        self.area_actual = self.areas[1]
        self.area_actual.explorada = True
        self.progreso = 0  # En naturaleza

        print(f"🌍 Mundo progresivo generado con {len(self.areas)} áreas")
        print(f"📍 Comenzando en: {self.area_actual.nombre} ({self.area_actual.tipo})")
        print(f"📜 {self.area_actual.descripcion}")

    def cambiar_area(self, nueva_area_id):
        """Cambia a una nueva área y actualiza progreso"""
        if nueva_area_id in self.areas and nueva_area_id in self.area_actual.conexiones:
            area_anterior = self.area_actual
            self.area_actual = self.areas[nueva_area_id]

            if not self.area_actual.explorada:
                self.area_actual.explorada = True
                print(f"📍 Nueva área descubierta: {self.area_actual.nombre}")
                print(f"📜 {self.area_actual.descripcion}")

            # Actualizar progreso según el tipo de área
            tipo_actual = self.area_actual.tipo
            if tipo_actual in ["pueblo", "aldea"] and self.progreso < 1:
                self.progreso = 1
                print("🎉 ¡Has llegado a la civilización! Fase: Pueblos")
            elif tipo_actual in ["cueva", "ruinas", "mazmorra"] and self.progreso < 2:
                self.progreso = 2
                print("⚔️ ¡Comienza la aventura en las masmorras! Fase: Mazmorras")
            elif tipo_actual in ["castillo", "reino", "capital"] and self.progreso < 3:
                self.progreso = 3
                print("🏰 ¡Has llegado al reino! Fase: Reino")

            return True, area_anterior, self.area_actual
        return False, None, None

    def obtener_fase_actual(self):
        """Devuelve la fase actual del progreso"""
        fases = {
            0: "Naturaleza",
            1: "Pueblos",
            2: "Mazmorras",
            3: "Reino"
        }
        return fases.get(self.progreso, "Desconocido")

    def obtener_areas_por_fase(self, fase):
        """Devuelve las áreas de una fase específica"""
        if fase == 0:
            return [self.areas[i] for i in range(1, 5) if i in self.areas]
        elif fase == 1:
            return [self.areas[i] for i in range(5, 8) if i in self.areas]
        elif fase == 2:
            return [self.areas[i] for i in range(8, 11) if i in self.areas]
        elif fase == 3:
            return [self.areas[i] for i in range(11, 13) if i in self.areas]
        return []

    def obtener_proximo_destino(self):
        """Sugiere el próximo destino para avanzar en la historia"""
        if self.progreso == 0:  # Naturaleza
            for area_id in self.area_actual.conexiones:
                area = self.areas[area_id]
                if area.tipo in ["pueblo", "aldea"]:
                    return area
        elif self.progreso == 1:  # Pueblos
            for area_id in self.area_actual.conexiones:
                area = self.areas[area_id]
                if area.tipo in ["cueva", "ruinas"]:
                    return area
        elif self.progreso == 2:  # Mazmorras
            for area_id in self.area_actual.conexiones:
                area = self.areas[area_id]
                if area.tipo in ["castillo", "reino"]:
                    return area
        return None

    def dibujar_minimapa(self, pantalla, x, y, tamaño):
        """Dibuja un minimapa que muestra el progreso"""
        radio = tamaño // 2
        centro_x = x + radio
        centro_y = y + radio

        # Fondo del minimapa con fase de progreso
        pygame.draw.circle(pantalla, (40, 60, 40), (centro_x, centro_y), radio)
        pygame.draw.circle(pantalla, (30, 50, 30), (centro_x, centro_y), radio, 2)

        # Título con fase actual
        fuente = pygame.font.Font(None, 24)
        fase_texto = f"MAPA - FASE: {self.obtener_fase_actual()}"
        titulo = fuente.render(fase_texto, True, TEXTO_TITULO)
        pantalla.blit(titulo, (x + (tamaño - titulo.get_width()) // 2, y - 30))

        # Organizar áreas por fase (círculos concéntricos)
        fases_posiciones = {
            0: (0.3, 120, (100, 200, 100)),    # Naturaleza: círculo interno, verde
            1: (0.5, 180, (200, 200, 100)),    # Pueblos: círculo medio, amarillo
            2: (0.7, 240, (200, 100, 100)),    # Mazmorras: círculo externo, rojo
            3: (0.9, 300, (100, 100, 200))     # Reino: círculo más externo, azul
        }

        for area in self.areas.values():
            # Determinar posición según fase
            if area.id <= 4:  # Naturaleza
                radio_fase, angulo_offset, color_fase = fases_posiciones[0]
                angulo_base = 90
            elif area.id <= 7:  # Pueblos
                radio_fase, angulo_offset, color_fase = fases_posiciones[1]
                angulo_base = 180
            elif area.id <= 10:  # Mazmorras
                radio_fase, angulo_offset, color_fase = fases_posiciones[2]
                angulo_base = 270
            else:  # Reino
                radio_fase, angulo_offset, color_fase = fases_posiciones[3]
                angulo_base = 0

            # Calcular posición
            dist = radio * radio_fase
            angulo = (angulo_base + (area.id * 30)) % 360

            area_x = centro_x + int(dist * pygame.math.Vector2(1, 0).rotate(angulo).x)
            area_y = centro_y + int(dist * pygame.math.Vector2(1, 0).rotate(angulo).y)

            # Color según estado
            if area.id == self.area_actual.id:
                color = (255, 255, 0)  # Amarillo brillante para área actual
                tamaño_punto = 10
                borde = 3
            elif area.explorada:
                color = color_fase
                tamaño_punto = 8
                borde = 2
            else:
                color = (80, 80, 80)  # Gris oscuro para no exploradas
                tamaño_punto = 6
                borde = 1

            # Dibujar área
            pygame.draw.circle(pantalla, color, (area_x, area_y), tamaño_punto)
            pygame.draw.circle(pantalla, (255, 255, 255), (area_x, area_y), tamaño_punto, borde)

            # Número del área (solo si explorada o actual)
            if area.explorada or area.id == self.area_actual.id:
                num_texto = fuente.render(str(area.id), True, (0, 0, 0))
                pantalla.blit(num_texto, (area_x - num_texto.get_width()//2,
                                        area_y - num_texto.get_height()//2))

        # Leyenda mejorada
        leyenda_y = y + tamaño + 10
        leyendas = [
            ("●", (255, 255, 0), "Área actual"),
            ("●", (100, 200, 100), "Naturaleza"),
            ("●", (200, 200, 100), "Pueblos"),
            ("●", (200, 100, 100), "Mazmorras"),
            ("●", (100, 100, 200), "Reino"),
            ("○", (80, 80, 80), "No explorado")
        ]

        fuente_peq = pygame.font.Font(None, 18)
        for i, (simbolo, color, texto) in enumerate(leyendas):
            leyenda_x = x + i * 120
            if leyenda_x < x + tamaño:
                pygame.draw.circle(pantalla, color, (leyenda_x + 6, leyenda_y + 6), 6)
                texto_render = fuente_peq.render(texto, True, TEXTO_SECUNDARIO)
                pantalla.blit(texto_render, (leyenda_x + 15, leyenda_y))
