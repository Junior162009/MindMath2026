# main.py - VERSIÓN CORREGIDA Y OPTIMIZADA
import pygame
import sys
import math
import random
from settings import *
from jugador import Jugador
from mapa import Mapa
from ui import FranjaTexto, Pergamino
from puerta import Puerta
from cofre import Cofre
from enemigo import EnemigoBasico, EnemigoCamuflado, EnemigoDisparador
from bala import Bala, BalaEnemiga
from sistema_respuestas import SistemaRespuestas
from npc import NPC
from misiones import SistemaMisiones
from mundo import Mundo
from tienda import Tienda
from progresion import ProgresionHistoria

class Juego:
    def __init__(self):
        pygame.init()

        # Configurar pantalla
        info = pygame.display.Info()
        if PANTALLA_COMPLETA:
            self.pantalla = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.ANCHO = info.current_w
            self.ALTO = info.current_h
        else:
            self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
            self.ANCHO = ANCHO
            self.ALTO = ALTO

        pygame.display.set_caption("Matemáticas en un Mundo Libre")
        self.reloj = pygame.time.Clock()

        # Mouse
        pygame.mouse.set_visible(MOSTRAR_CURSOR)
        self.mouse_pos = (0, 0)
        self.click_izquierdo = False
        self.tiempo_entre_disparos = TIEMPO_ENTRE_DISPAROS
        self.tiempo_disparo = 0

        # Cargar recursos
        self.cargar_recursos()

        # Sistema de mundo
        self.mundo = Mundo()
        self.area_actual = self.mundo.area_actual

        # Inicializar sistemas
        self.sistema_respuestas = SistemaRespuestas(self.franja_img)
        self.sistema_misiones = SistemaMisiones()
        self.pergamino = Pergamino(self.pergamino_img)

        # Sistema de tienda
        self.tienda = Tienda()

        self.progresion = ProgresionHistoria()

        # Estado del jugador
        self.jugador = Jugador()
        self.vidas = VIDAS_INICIALES
        self.puntuacion = 0

        # Disparos enemigos
        self.tiempo_disparo_enemigos = 0
        self.tiempo_entre_disparos_enemigos = TIEMPO_ENTRE_DISPAROS_ENEMIGOS

        # Crear mapa del área actual
        self.cargar_area_actual()

        # Zoom y cámara
        self.zoom = ZOOM_POR_DEFECTO
        self.cam_x = 0
        self.cam_y = 0

        # Estado del juego
        self.ejecutando = True
        self.mostrando_mapa = False
        self.mostrando_misiones = False
        self.hablando_con_npc = None
        self.dialogo_actual = None
        self.mostrando_inventario = False
        self.mostrando_tienda = False
        self.nivel_completado = False

        # Balas
        self.balas = []
        self.balas_enemigas = []

        # Áreas de la pantalla
        self.calcular_areas_pantalla()

        # Fuentes precargadas (OPTIMIZACIÓN)
        self.cargar_fuentes()

        print(f"🌍 Mundo generado: {len(self.mundo.areas)} áreas disponibles")
        print(f"📍 Comenzando en: {self.area_actual.nombre}")
        print(f"🎯 Misiones disponibles: {len(self.sistema_misiones.misiones_disponibles)}")
        print(f"💰 Puntos iniciales: {self.jugador.puntos}")

    def cargar_fuentes(self):
        """Precarga todas las fuentes para mejor rendimiento"""
        self.fuentes = {
            'titulo': pygame.font.Font(None, TAM_FUENTE_TITULO),
            'subtitulo': pygame.font.Font(None, TAM_FUENTE_SUBTITULO),
            'normal': pygame.font.Font(None, TAM_FUENTE_NORMAL),
            'pequena': pygame.font.Font(None, TAM_FUENTE_PEQUEÑA),
            'muy_pequena': pygame.font.Font(None, TAM_FUENTE_MUY_PEQUEÑA),
        }

    def cargar_recursos(self):
        """Carga todos los recursos del juego"""
        print("Cargando recursos...")

        # Franja
        try:
            self.franja_img = pygame.image.load("assets/ui/franja.png").convert_alpha()
            franja_ancho = self.ANCHO // 1.5
            franja_alto = 80
            self.franja_img = pygame.transform.scale(self.franja_img, (franja_ancho, franja_alto))
            print("✓ franja.png cargado")
        except FileNotFoundError:
            print("✗ franja.png no encontrado, creando temporal")
            self.franja_img = pygame.Surface((self.ANCHO//1.5, 80), pygame.SRCALPHA)
            self.franja_img.fill((0, 0, 0, 200))
            pygame.draw.rect(self.franja_img, (139, 69, 19), self.franja_img.get_rect(), 3)
            pygame.draw.rect(self.franja_img, (205, 133, 63),
                           (5, 5, self.franja_img.get_width()-10, self.franja_img.get_height()-10), 2)

        # Suelo
        try:
            self.suelo_img = pygame.image.load("assets/tiles/suelo.png").convert()
            self.suelo_img = pygame.transform.scale(self.suelo_img, (TAM, TAM))
            print("✓ suelo.png cargado")
        except FileNotFoundError:
            print("✗ suelo.png no encontrado, creando temporal")
            self.suelo_img = pygame.Surface((TAM, TAM))
            self.suelo_img.fill((100, 100, 100))

        # Pared
        try:
            self.pared_img = pygame.image.load("assets/tiles/pared.png").convert()
            self.pared_img = pygame.transform.scale(self.pared_img, (TAM, TAM))
            print("✓ pared.png cargado")
        except FileNotFoundError:
            print("✗ pared.png no encontrado, creando temporal")
            self.pared_img = pygame.Surface((TAM, TAM))
            self.pared_img.fill((150, 75, 0))

        # Corazón
        try:
            self.corazon_img = pygame.image.load("assets/ui/corazon.png").convert_alpha()
            self.corazon_img = pygame.transform.scale(self.corazon_img, (30, 30))
            print("✓ corazon.png cargado")
        except FileNotFoundError:
            print("✗ corazon.png no encontrado, creando temporal")
            self.corazon_img = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.polygon(self.corazon_img, (255, 0, 0), [
                (15, 5), (20, 10), (25, 8), (25, 15),
                (20, 25), (15, 28), (10, 25), (5, 15),
                (5, 8), (10, 10)
            ])

        # Pergamino
        try:
            self.pergamino_img = pygame.image.load("assets/ui/pergamino.png").convert_alpha()
            self.pergamino_img = pygame.transform.scale(self.pergamino_img, (300, 160))
            print("✓ pergamino.png cargado")
        except FileNotFoundError:
            print("✗ pergamino.png no encontrado, creando temporal")
            self.pergamino_img = pygame.Surface((300, 160), pygame.SRCALPHA)
            self.pergamino_img.fill((240, 220, 180))
            pygame.draw.rect(self.pergamino_img, (200, 180, 140), self.pergamino_img.get_rect(), 5)

        print("✓ Todos los recursos cargados")

    def cargar_area_actual(self):
        """Carga el área actual del mundo"""
        print(f"Cargando área: {self.area_actual.nombre}")

        # Obtener mapa del área
        mapa_data = self.area_actual.mapa

        # Crear mapa
        self.mapa = Mapa(mapa_data, self.suelo_img, self.pared_img)

        # Limpiar listas de objetos
        self.puertas = []
        self.cofres = []
        self.enemigos = []
        self.npcs = []
        self.balas = []
        self.balas_enemigas = []

        # Procesar mapa
        for y, fila in enumerate(mapa_data):
            for x, tile in enumerate(fila):
                pos_x = x * TAM
                pos_y = y * TAM

                if tile == "P":
                    self.jugador.rect.topleft = (pos_x, pos_y)
                    self.cam_x = pos_x - self.ANCHO // 2
                    self.cam_y = pos_y - self.ALTO // 2

                elif tile == "D":
                    self.puertas.append(Puerta(pos_x, pos_y))
                elif tile == "C":
                    self.cofres.append(Cofre(pos_x, pos_y))
                elif tile == "E":
                    # Crear enemigos según peligrosidad del área
                    if self.area_actual.peligrosidad <= 3:
                        self.enemigos.append(EnemigoBasico(pos_x, pos_y))
                    elif self.area_actual.peligrosidad <= 6:
                        if random.random() < 0.7:
                            self.enemigos.append(EnemigoBasico(pos_x, pos_y))
                        else:
                            self.enemigos.append(EnemigoCamuflado(pos_x, pos_y))
                    else:
                        rand = random.random()
                        if rand < 0.4:
                            self.enemigos.append(EnemigoBasico(pos_x, pos_y))
                        elif rand < 0.7:
                            self.enemigos.append(EnemigoCamuflado(pos_x, pos_y))
                        else:
                            self.enemigos.append(EnemigoDisparador(pos_x, pos_y))
                elif tile == "N":
                    # Crear NPCs según área
                    if self.area_actual.id == 1:  # Aldea
                        npc_tipo = random.choice(["profesor", "aldeano", "comerciante"])
                        npc_nombre = random.choice(NPC_NOMBRES)
                        dialogo = self.crear_dialogo_npc(npc_tipo)

                        # Asignar misiones según tipo de NPC
                        misiones = []
                        if npc_tipo == "profesor":
                            misiones = [1, 5]
                        elif npc_tipo == "comerciante":
                            misiones = [4]
                        elif npc_tipo == "aldeano":
                            misiones = [2]

                        self.npcs.append(NPC(pos_x, pos_y, npc_tipo, npc_nombre, dialogo, misiones))

        # Crear franja (debe crearse después de cargar franja_img)
        self.franja = FranjaTexto(self.franja_img)

        # Mostrar mensaje de área con descripción
        mensaje = f"{self.area_actual.nombre} - {self.area_actual.descripcion}"
        self.franja.mostrar(mensaje, duracion=3.0)

        # Mensaje de progresión según fase
        fase = self.mundo.obtener_fase_actual()
        if fase == "Naturaleza" and not self.area_actual.explorada:
            self.pergamino.mostrar("¡Explora la naturaleza! Encuentra el camino al pueblo.", 4.0)
        elif fase == "Pueblos" and not self.area_actual.explorada:
            self.pergamino.mostrar("¡Bienvenido a la civilización! Habla con los NPCs para misiones.", 4.0)
        elif fase == "Mazmorras" and not self.area_actual.explorada:
            self.pergamino.mostrar("¡Cuidado! Las masmorras son peligrosas. Prepárate bien.", 4.0)
        elif fase == "Reino" and not self.area_actual.explorada:
            self.pergamino.mostrar("¡Felicidades! Has llegado al reino. Tu aventura continúa...", 4.0)

        # Registrar exploración
        self.jugador.agregar_area_explorada(self.area_actual.id)

    def crear_dialogo_npc(self, tipo):
        """Crea diálogos para NPCs según su tipo"""
        dialogos = {
            "profesor": [
                "¡Hola, joven aventurero! Las matemáticas son la clave para el éxito.",
                "¿Te gustaría aprender algo nuevo hoy?",
                "Tengo algunos problemas que necesitan solución. ¿Puedes ayudarme?"
            ],
            "aldeano": [
                "¡Bienvenido a nuestra aldea!",
                "Ten cuidado en el bosque, hay criaturas peligrosas.",
                "Si necesitas suministros, visita al comerciante."
            ],
            "comerciante": [
                "¡Bienvenido a mi tienda!",
                "Tengo balas, pociones y otros suministros.",
                "¿En qué puedo ayudarte hoy?"
            ],
            "explorador": [
                "He explorado muchas áreas de este mundo.",
                "Si quieres aventuras, visita las cuevas al norte.",
                "Cada área tiene sus propios secretos por descubrir."
            ],
            "guerrero": [
                "¡Saludos, viajero!",
                "Los enemigos son fuertes aquí. Prepárate bien.",
                "Necesitamos ayuda para limpiar esta área."
            ],
            "mago": [
                "El conocimiento es poder.",
                "Las matemáticas son magia en su forma más pura.",
                "Resuelve mis acertijos y te recompensaré."
            ]
        }
        return dialogos.get(tipo, ["Hola, ¿cómo estás?"])

    def calcular_areas_pantalla(self):
        """Calcula las áreas de la pantalla para UI"""
        # Menú superior (10% de la altura)
        self.menu_rect = pygame.Rect(0, 0, self.ANCHO, int(self.ALTO * 0.1))

        # Área de juego principal (70% del ancho, 70% del alto restante)
        self.juego_rect = pygame.Rect(0, self.menu_rect.height,
                                     int(self.ANCHO * PORCENTAJE_ANCHO_JUEGO),
                                     int((self.ALTO - self.menu_rect.height) * PORCENTAJE_ALTO_JUEGO))

        # Inventario (debajo del área de juego)
        self.inventario_rect = pygame.Rect(0, self.juego_rect.bottom,
                                          self.juego_rect.width,
                                          self.ALTO - self.juego_rect.bottom)

        # Panel derecho (misiones, mapa, stats) - 30% del ancho
        self.panel_rect = pygame.Rect(self.juego_rect.right, self.menu_rect.height,
                                      self.ANCHO - self.juego_rect.width,
                                      self.ALTO - self.menu_rect.height)

    def manejar_eventos(self):
        """Maneja eventos del juego"""
        self.click_izquierdo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False

            elif evento.type == pygame.MOUSEMOTION:
                self.mouse_pos = evento.pos

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.click_izquierdo = True

            elif evento.type == pygame.KEYDOWN:
                if evento.key == TECLA_SALIR:
                    self.ejecutando = False

                elif evento.key == TECLA_MAPA:
                    self.mostrando_mapa = not self.mostrando_mapa
                    if self.mostrando_mapa:
                        self.franja.mostrar("Mapa mundial activado (M para cerrar)")

                elif evento.key == TECLA_MISIONES:
                    self.mostrando_misiones = not self.mostrando_misiones

                elif evento.key == TECLA_INVENTARIO:
                    self.mostrando_inventario = not self.mostrando_inventario

                elif evento.key == TECLA_TIENDA:
                    self.mostrando_tienda = not self.mostrando_tienda

                elif evento.key == TECLA_INTERACTUAR:
                    self.interactuar()

                elif evento.key == TECLA_RECARGAR:
                    self.recargar_balas()

                elif evento.key == TECLA_SIGUIENTE_DIALOGO and self.hablando_con_npc:
                    self.avanzar_dialogo()

                # Sistema de respuestas
                if self.sistema_respuestas.activo:
                    self.sistema_respuestas.manejar_evento(evento, self.jugador, self.franja)

    def interactuar(self):
        """Maneja interacciones con el mundo"""
        if self.sistema_respuestas.activo:
            return

        # Interactuar con NPCs
        for npc in self.npcs:
            if self.jugador.rect.colliderect(npc.rect):
                self.hablando_con_npc = npc
                self.dialogo_actual = npc.hablar(self.jugador, self.sistema_misiones)
                self.franja.mostrar(f"Hablando con {npc.nombre} ({npc.tipo})")
                return

        # Interactuar con cofres
        for cofre in self.cofres:
            if self.jugador.rect.colliderect(cofre.rect):
                if not cofre.abierto:
                    cofre.abrir()
                    self.sistema_respuestas.activar(cofre, self.jugador)

                    # Actualizar misión de cofres
                    resultados = self.sistema_misiones.actualizar_mision_cofre()
                    for resultado in resultados:
                        self.franja.mostrar(resultado, duracion=2.0)
                return

        # Interactuar con puertas
        for puerta in self.puertas:
            if self.jugador.rect.colliderect(puerta.rect):
                self.mostrar_opciones_puerta()
                return

    def avanzar_dialogo(self):
        """Avanza al siguiente diálogo del NPC"""
        if self.hablando_con_npc:
            nuevo_dialogo = self.hablando_con_npc.siguiente_dialogo()
            if nuevo_dialogo:
                self.dialogo_actual = nuevo_dialogo
            else:
                self.hablando_con_npc = None
                self.dialogo_actual = None

    def recargar_balas(self):
        """Recarga las balas del jugador"""
        balas_necesarias = BALAS_MAXIMAS - self.jugador.inventario["balas"]
        if balas_necesarias > 0:
            # Usar balas extra si tiene
            if self.jugador.inventario["balas_extra"] > 0:
                balas_a_recargar = min(balas_necesarias, BALAS_RECARGA)
                self.jugador.inventario["balas"] += balas_a_recargar
                self.jugador.inventario["balas_extra"] -= 1
                self.franja.mostrar(f"¡Recargado! +{balas_a_recargar} balas", duracion=1.5)
            else:
                self.franja.mostrar("No tienes balas extra para recargar", duracion=1.5)
        else:
            self.franja.mostrar("Ya tienes todas las balas", duracion=1.0)

    def mostrar_opciones_puerta(self):
        """Muestra opciones disponibles en una puerta"""
        areas_conectadas = self.mundo.obtener_areas_conectadas()
        if areas_conectadas:
            mensaje = "Puerta: Viajar a -> "
            mensaje += ", ".join([f"{area.id}.{area.nombre}" for area in areas_conectadas])
            self.franja.mostrar(mensaje, duracion=3.0)
        else:
            self.franja.mostrar("Esta puerta no lleva a ningún lugar", duracion=1.5)

    def actualizar(self):
        """Actualiza toda la lógica del juego"""
        # Actualizar UI
        self.pergamino.actualizar()
        self.franja.actualizar()
        self.jugador.actualizar_efectos()

        # Sistema de respuestas
        self.sistema_respuestas.actualizar()
        if self.sistema_respuestas.activo:
            return

        # Disparar si hay click
        if self.click_izquierdo and not self.sistema_respuestas.activo:
            self.disparar()

        # Actualizar cámara
        self.actualizar_camara()

        # Mover jugador
        self.jugador.mover(self.mapa.paredes)

        # Mover enemigos
        for enemigo in self.enemigos[:]:
            enemigo_tile_x = enemigo.rect.centerx // TAM
            enemigo_tile_y = enemigo.rect.centery // TAM
            en_tunel = self.mapa.es_tunel(enemigo_tile_x, enemigo_tile_y)

            velocidad_original = enemigo.velocidad
            if en_tunel:
                enemigo.velocidad = velocidad_original * 0.8

            enemigo.mover(self.mapa.paredes, self.jugador.rect)
            enemigo.velocidad = velocidad_original

            # Colisión con jugador
            if self.jugador.rect.colliderect(enemigo.rect):
                dano = DANO_ENEMIGO_TUNEL if en_tunel else DANO_ENEMIGO_NORMAL
                # Aplicar defensa si tiene efecto
                if self.jugador.efecto_defensa > 0:
                    dano = int(dano * (1 - self.jugador.efecto_defensa))

                self.vidas -= dano
                self.franja.mostrar(f"¡Golpeado por {enemigo.tipo}! -{dano} vidas", duracion=1.0)
                self.enemigos.remove(enemigo)

                if self.vidas <= 0:
                    self.game_over()

        # Mover balas del jugador
        for bala in self.balas[:]:
            bala.mover()

            # Verificar colisión con paredes
            for pared in self.mapa.paredes:
                if bala.rect.colliderect(pared):
                    if bala in self.balas:
                        self.balas.remove(bala)
                    break

            # Verificar colisión con enemigos
            for enemigo in self.enemigos[:]:
                if bala.rect.colliderect(enemigo.rect):
                    # Aplicar fuerza si tiene efecto
                    dano_extra = 1.0
                    if self.jugador.efecto_fuerza > 0:
                        dano_extra += self.jugador.efecto_fuerza

                    enemigo.recibir_dano()
                    if enemigo.vida <= 0:
                        # Calcular puntos y experiencia
                        puntos = 0
                        experiencia = 0
                        if enemigo.tipo == "Básico":
                            puntos = PUNTOS_ENEMIGO_BASICO
                            experiencia = EXPERIENCIA_ENEMIGO_BASICO
                        elif enemigo.tipo == "Camuflado":
                            puntos = PUNTOS_ENEMIGO_CAMUFLADO
                            experiencia = EXPERIENCIA_ENEMIGO_CAMUFLADO
                        elif enemigo.tipo == "Disparador":
                            puntos = PUNTOS_ENEMIGO_DISPARADOR
                            experiencia = EXPERIENCIA_ENEMIGO_DISPARADOR

                        # Bonus por túnel
                        if self.mapa.es_tunel(enemigo.rect.centerx // TAM, enemigo.rect.centery // TAM):
                            puntos += BONUS_TUNEL_ENEMIGO

                        self.jugador.puntos += puntos
                        self.jugador.enemigos_eliminados += 1

                        # Agregar experiencia
                        if self.jugador.agregar_experiencia(experiencia):
                            self.franja.mostrar(f"¡Subiste al nivel {self.jugador.nivel}!", duracion=2.0)

                        self.franja.mostrar(f"¡{enemigo.tipo} eliminado! +{puntos} puntos", duracion=1.0)
                        self.enemigos.remove(enemigo)

                        # Actualizar misiones de matar
                        resultados = self.sistema_misiones.actualizar_mision_matando(enemigo.tipo)
                        for resultado in resultados:
                            self.franja.mostrar(resultado, duracion=2.0)

                    if bala in self.balas:
                        self.balas.remove(bala)
                    break

        # Enemigos disparan
        self.disparar_enemigos()

        # Mover balas enemigas
        for bala in self.balas_enemigas[:]:
            bala.mover()

            # Colisión con paredes
            for pared in self.mapa.paredes:
                if bala.rect.colliderect(pared):
                    if bala in self.balas_enemigas:
                        self.balas_enemigas.remove(bala)
                    break

            # Colisión con jugador
            if bala.rect.colliderect(self.jugador.rect):
                en_tunel = self.mapa.es_tunel(self.jugador.rect.centerx // TAM, self.jugador.rect.centery // TAM)

                if bala.tipo == "Disparador":
                    dano = DANO_BALA_ENEMIGA_TUNEL if en_tunel else DANO_BALA_ENEMIGA_FUEGO
                else:
                    dano = DANO_ENEMIGO_TUNEL if en_tunel else DANO_BALA_ENEMIGA_NORMAL

                # Aplicar defensa si tiene efecto
                if self.jugador.efecto_defensa > 0:
                    dano = int(dano * (1 - self.jugador.efecto_defensa))

                self.vidas -= dano
                self.balas_enemigas.remove(bala)

                if self.vidas <= 0:
                    self.game_over()
                else:
                    self.franja.mostrar(f"¡Bala enemiga! -{dano} vidas", duracion=1.0)
                break
        # Verificar progresión de la historia
        resultados_progresion = self.progresion.verificar_progreso(self.jugador, self.mundo)
        for resultado in resultados_progresion:
            self.franja.mostrar(resultado, duracion=3.0)
            self.pergamino.mostrar("¡Nueva misión de historia disponible!", 3.0)

    def actualizar_camara(self):
        """Actualiza la posición de la cámara"""
        target_x = self.jugador.rect.centerx - self.juego_rect.width // (2 * self.zoom)
        target_y = self.jugador.rect.centery - self.juego_rect.height // (2 * self.zoom)

        self.cam_x += (target_x - self.cam_x) * 0.1
        self.cam_y += (target_y - self.cam_y) * 0.1

        # Limitar cámara
        ancho_mapa = len(self.mapa.nivel[0]) * TAM
        alto_mapa = len(self.mapa.nivel) * TAM
        max_cam_x = max(0, ancho_mapa - self.juego_rect.width / self.zoom)
        max_cam_y = max(0, alto_mapa - self.juego_rect.height / self.zoom)

        self.cam_x = max(0, min(self.cam_x, max_cam_x))
        self.cam_y = max(0, min(self.cam_y, max_cam_y))

        self.cam_x = int(self.cam_x)
        self.cam_y = int(self.cam_y)

    def disparar(self):
        """El jugador dispara una bala"""
        if self.tiempo_disparo <= 0 and self.jugador.inventario["balas"] > 0:
            mouse_x, mouse_y = self.mouse_pos

            # Convertir coordenadas del mouse considerando zoom
            if self.zoom != 1.0:
                offset_x = (self.ANCHO * (self.zoom - 1)) // 2
                offset_y = (self.ALTO * (self.zoom - 1)) // 2
                mouse_x_real = int((mouse_x + offset_x) / self.zoom) + self.cam_x
                mouse_y_real = int((mouse_y + offset_y) / self.zoom) + self.cam_y
            else:
                mouse_x_real = mouse_x + self.cam_x
                mouse_y_real = mouse_y + self.cam_y

            nueva_bala = Bala(
                self.jugador.rect.centerx,
                self.jugador.rect.centery,
                mouse_x_real,
                mouse_y_real,
                VELOCIDAD_BALA_DEFAULT
            )

            self.balas.append(nueva_bala)
            self.jugador.inventario["balas"] -= 1
            self.tiempo_disparo = self.tiempo_entre_disparos

            # Advertencia de pocas balas
            if self.jugador.inventario["balas"] <= 3:
                self.franja.mostrar(f"¡Pocas balas! {self.jugador.inventario['balas']} restantes", duracion=1.0)
        else:
            if self.tiempo_disparo > 0:
                self.tiempo_disparo -= 1

            if self.jugador.inventario["balas"] <= 0 and self.click_izquierdo:
                self.franja.mostrar("¡Sin balas! Presiona R para recargar", duracion=1.5)

    def disparar_enemigos(self):
        """Los enemigos disparan al jugador"""
        if self.tiempo_disparo_enemigos <= 0:
            for enemigo in self.enemigos:
                if hasattr(enemigo, 'puede_disparar') and enemigo.puede_disparar:
                    distancia_x = abs(enemigo.rect.centerx - self.jugador.rect.centerx)
                    distancia_y = abs(enemigo.rect.centery - self.jugador.rect.centery)
                    distancia = math.sqrt(distancia_x**2 + distancia_y**2)

                    if distancia < 300:
                        # En túneles, los enemigos son menos precisos
                        enemigo_tile_x = enemigo.rect.centerx // TAM
                        enemigo_tile_y = enemigo.rect.centery // TAM

                        if self.mapa.es_tunel(enemigo_tile_x, enemigo_tile_y):
                            offset_x = random.randint(-30, 30)
                            offset_y = random.randint(-30, 30)
                        else:
                            offset_x = random.randint(-10, 10)
                            offset_y = random.randint(-10, 10)

                        target_x = self.jugador.rect.centerx + offset_x
                        target_y = self.jugador.rect.centery + offset_y

                        # Crear bala enemiga
                        self.balas_enemigas.append(BalaEnemiga(
                            enemigo.rect.centerx,
                            enemigo.rect.centery,
                            target_x,
                            target_y,
                            enemigo.tipo,
                            VELOCIDAD_BALA_ENEMIGA
                        ))

            # Resetear el temporizador
            self.tiempo_disparo_enemigos = self.tiempo_entre_disparos_enemigos
        else:
            # Reducir el temporizador
            self.tiempo_disparo_enemigos -= 1

    def dibujar(self):
        """Dibuja todos los elementos del juego"""
        # Limpiar pantalla
        self.pantalla.fill(NEGRO)

        # Dibujar áreas de UI
        self.dibujar_areas_fondo()

        # Dibujar juego
        self.dibujar_juego()

        # Dibujar UI
        self.dibujar_menu_superior()

        if self.mostrando_mapa:
            self.dibujar_mapa_mundial()

        if self.mostrando_misiones:
            self.dibujar_panel_misiones()

        if self.mostrando_inventario:
            self.dibujar_inventario()

        if self.mostrando_tienda:
            self.dibujar_tienda()

        if self.hablando_con_npc:
            self.dibujar_dialogo()

        # Dibujar sistemas superpuestos
        self.sistema_respuestas.dibujar(self.pantalla)
        self.franja.dibujar(self.pantalla)
        self.pergamino.dibujar(self.pantalla)

        # Actualizar pantalla
        pygame.display.flip()

    def dibujar_areas_fondo(self):
        """Dibuja las áreas de fondo de la UI"""
        # Área de juego
        pygame.draw.rect(self.pantalla, COLOR_FONDO_PANEL, self.juego_rect)

        # Menú superior
        pygame.draw.rect(self.pantalla, COLOR_FONDO_MENU, self.menu_rect)

        # Inventario
        pygame.draw.rect(self.pantalla, COLOR_FONDO_INVENTARIO, self.inventario_rect)

        # Panel derecho
        pygame.draw.rect(self.pantalla, COLOR_FONDO_PANEL, self.panel_rect)

        # Bordes
        pygame.draw.rect(self.pantalla, COLOR_BORDE, self.menu_rect, GROSOR_BORDE)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, self.juego_rect, GROSOR_BORDE)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, self.inventario_rect, GROSOR_BORDE)
        pygame.draw.rect(self.pantalla, COLOR_BORDE, self.panel_rect, GROSOR_BORDE)

    def dibujar_juego(self):
        """Dibuja el área de juego principal"""
        # Crear superficie temporal para el juego
        juego_surface = pygame.Surface((self.juego_rect.width, self.juego_rect.height))
        juego_surface.fill(COLOR_FONDO_PANEL)

        # Verificar si está en túnel
        jugador_tile_x = self.jugador.rect.centerx // TAM
        jugador_tile_y = self.jugador.rect.centery // TAM
        en_tunel = self.mapa.es_tunel(jugador_tile_x, jugador_tile_y)

        # Dibujar mapa
        self.mapa.dibujar_suelo(juego_surface, self.cam_x, self.cam_y,
                               (self.jugador.rect.centerx, self.jugador.rect.centery), en_tunel)

        # Dibujar enemigos
        for enemigo in self.enemigos:
            enemigo.dibujar(juego_surface, self.cam_x, self.cam_y, self.suelo_img)

        # Dibujar paredes
        self.mapa.dibujar_paredes(juego_surface, self.cam_x, self.cam_y,
                                 (self.jugador.rect.centerx, self.jugador.rect.centery), en_tunel)

        # Dibujar objetos
        for puerta in self.puertas:
            puerta.dibujar(juego_surface, self.cam_x, self.cam_y)
        for cofre in self.cofres:
            cofre.dibujar(juego_surface, self.cam_x, self.cam_y)
        for npc in self.npcs:
            npc.dibujar(juego_surface, self.cam_x, self.cam_y)

        # Dibujar balas
        for bala in self.balas_enemigas + self.balas:
            bala.dibujar(juego_surface, self.cam_x, self.cam_y)

        # Dibujar jugador
        self.jugador.dibujar(juego_surface, self.cam_x, self.cam_y)

        # Efecto de túnel
        if MODO_OSCURO and en_tunel:
            self.dibujar_efecto_tunel(juego_surface)

        # Aplicar zoom si es necesario
        if self.zoom != 1.0:
            nuevo_ancho = int(self.juego_rect.width * self.zoom)
            nuevo_alto = int(self.juego_rect.height * self.zoom)
            juego_escalado = pygame.transform.scale(juego_surface, (nuevo_ancho, nuevo_alto))

            # Centrar
            offset_x = (nuevo_ancho - self.juego_rect.width) // 2
            offset_y = (nuevo_alto - self.juego_rect.height) // 2

            self.pantalla.blit(juego_escalado,
                             (self.juego_rect.x - offset_x, self.juego_rect.y - offset_y))
        else:
            self.pantalla.blit(juego_surface, self.juego_rect.topleft)

    def dibujar_efecto_tunel(self, superficie):
        """Dibuja el efecto de oscuridad en túneles"""
        jugador_x = self.jugador.rect.centerx - self.cam_x
        jugador_y = self.jugador.rect.centery - self.cam_y
        radio = LUZ_RADIO_TUNEL

        # Crear máscara de oscuridad
        oscuridad = pygame.Surface((self.juego_rect.width, self.juego_rect.height), pygame.SRCALPHA)
        oscuridad.fill((0, 0, 0, OSCURIDAD_TUNEL_ALPHA))

        # Crear círculo de visión
        mascara = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(mascara, (0, 0, 0, 0), (radio, radio), radio)

        # Aplicar máscara
        oscuridad.blit(mascara,
                      (jugador_x - radio, jugador_y - radio),
                      special_flags=pygame.BLEND_RGBA_MIN)

        superficie.blit(oscuridad, (0, 0))

    def dibujar_menu_superior(self):
        """Dibuja el menú superior"""
        fuente = self.fuentes['subtitulo']
        fuente_normal = self.fuentes['normal']

        # Título del juego
        titulo = fuente.render("MUNDO LIBRE MATEMÁTICO", True, TEXTO_TITULO)
        self.pantalla.blit(titulo, (20, 10))

        # Información del jugador
        info_texto = [
            f"Nivel: {self.jugador.nivel}",
            f"Puntos: {self.jugador.puntos}",
            f"EXP: {self.jugador.experiencia}/{self.jugador.experiencia_necesaria}",
            f"Área: {self.area_actual.nombre}"
        ]

        x_pos = self.ANCHO - 300
        for i, texto in enumerate(info_texto):
            texto_render = fuente_normal.render(texto, True, TEXTO_SECUNDARIO)
            self.pantalla.blit(texto_render, (x_pos, 15 + i * 25))

        # Vidas
        vida_texto = fuente_normal.render("Vidas:", True, TEXTO_VIDAS)
        self.pantalla.blit(vida_texto, (self.ANCHO // 2 - 100, 15))

        if self.corazon_img:
            for i in range(self.vidas):
                self.pantalla.blit(self.corazon_img,
                                 (self.ANCHO // 2 - 50 + i * 35, 10))

        # Balas
        balas_texto = fuente_normal.render(f"Balas: {self.jugador.inventario['balas']}/{BALAS_MAXIMAS}",
                                          True, TEXTO_BALAS)
        self.pantalla.blit(balas_texto, (self.ANCHO // 2 + 100, 15))

    def dibujar_mapa_mundial(self):
        """Dibuja el mapa mundial"""
        # Fondo semitransparente
        fondo = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))
        self.pantalla.blit(fondo, (0, 0))

        # Panel del mapa
        mapa_ancho = 600
        mapa_alto = 600
        mapa_x = (self.ANCHO - mapa_ancho) // 2
        mapa_y = (self.ALTO - mapa_alto) // 2

        pygame.draw.rect(self.pantalla, COLOR_FONDO_PANEL,
                        (mapa_x, mapa_y, mapa_ancho, mapa_alto))
        pygame.draw.rect(self.pantalla, TEXTO_TITULO,
                        (mapa_x, mapa_y, mapa_ancho, mapa_alto), 3)

        # Título
        fuente = self.fuentes['titulo']
        titulo = fuente.render("MAPA MUNDIAL", True, TEXTO_TITULO)
        self.pantalla.blit(titulo, (mapa_x + (mapa_ancho - titulo.get_width()) // 2, mapa_y + 20))

        # Dibujar mapa
        self.mundo.dibujar_minimapa(self.pantalla, mapa_x + 50, mapa_y + 80, 500)

        # Información del área actual
        fuente_info = self.fuentes['normal']
        info_textos = [
            f"Área actual: {self.area_actual.nombre}",
            f"Tipo: {self.area_actual.tipo}",
            f"Peligrosidad: {self.area_actual.peligrosidad}/10",
            f"Recursos: {', '.join(self.area_actual.recursos[:3])}",
            f"Explorada: {'Sí' if self.area_actual.explorada else 'No'}"
        ]

        y_pos = mapa_y + 400
        for texto in info_textos:
            texto_render = fuente_info.render(texto, True, TEXTO_SECUNDARIO)
            self.pantalla.blit(texto_render, (mapa_x + 50, y_pos))
            y_pos += 30

        # Instrucciones
        instrucciones = fuente_info.render("Presiona M para cerrar el mapa", True, TEXTO_SECUNDARIO)
        self.pantalla.blit(instrucciones, (mapa_x + (mapa_ancho - instrucciones.get_width()) // 2,
                                         mapa_y + mapa_alto - 40))

    def dibujar_panel_misiones(self):
        """Dibuja el panel de misiones"""
        # Fondo semitransparente
        fondo = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))
        self.pantalla.blit(fondo, (0, 0))

        # Panel de misiones
        panel_ancho = 700
        panel_alto = 500
        panel_x = (self.ANCHO - panel_ancho) // 2
        panel_y = (self.ALTO - panel_alto) // 2

        pygame.draw.rect(self.pantalla, COLOR_FONDO_PANEL,
                        (panel_x, panel_y, panel_ancho, panel_alto))
        pygame.draw.rect(self.pantalla, TEXTO_MISION_TITULO,
                        (panel_x, panel_y, panel_ancho, panel_alto), 3)

        # Título
        fuente = self.fuentes['titulo']
        titulo = fuente.render("MISIONES", True, TEXTO_MISION_TITULO)
        self.pantalla.blit(titulo, (panel_x + (panel_ancho - titulo.get_width()) // 2, panel_y + 20))

        fuente_normal = self.fuentes['normal']
        fuente_peq = self.fuentes['pequena']

        # Misiones activas
        y_pos = panel_y + 70
        activas_titulo = fuente_normal.render("MISIONES ACTIVAS:", True, TEXTO_MISION_TITULO)
        self.pantalla.blit(activas_titulo, (panel_x + 30, y_pos))
        y_pos += 40

        misiones_activas = self.sistema_misiones.obtener_misiones_activas()
        if misiones_activas:
            for mision in misiones_activas:
                texto = fuente_normal.render(f"• {mision['titulo']}", True, TEXTO_MISION_DESC)
                self.pantalla.blit(texto, (panel_x + 50, y_pos))

                progreso = fuente_peq.render(f"  {mision['progreso']}", True, TEXTO_MISION_PROG)
                self.pantalla.blit(progreso, (panel_x + 60, y_pos + 25))

                y_pos += 60
        else:
            texto = fuente_normal.render("No tienes misiones activas", True, TEXTO_SECUNDARIO)
            self.pantalla.blit(texto, (panel_x + 50, y_pos))
            y_pos += 40

        # Misiones disponibles
        y_pos += 20
        disponibles_titulo = fuente_normal.render("MISIONES DISPONIBLES:", True, TEXTO_MISION_TITULO)
        self.pantalla.blit(disponibles_titulo, (panel_x + 30, y_pos))
        y_pos += 40

        misiones_disponibles = self.sistema_misiones.obtener_misiones_disponibles()
        if misiones_disponibles:
            for mision in misiones_disponibles[:3]:  # Mostrar solo 3
                texto = fuente_peq.render(f"• {mision['titulo']}", True, TEXTO_SECUNDARIO)
                self.pantalla.blit(texto, (panel_x + 50, y_pos))

                desc = fuente_peq.render(f"  {mision['descripcion']}", True, TEXTO_MISION_DESC)
                self.pantalla.blit(desc, (panel_x + 60, y_pos + 20))

                npc_info = fuente_peq.render(f"  NPC: {mision['npc']}", True, TEXTO_SECUNDARIO)
                self.pantalla.blit(npc_info, (panel_x + 60, y_pos + 40))

                y_pos += 80
        else:
            texto = fuente_normal.render("No hay misiones disponibles", True, TEXTO_SECUNDARIO)
            self.pantalla.blit(texto, (panel_x + 50, y_pos))

        # Instrucciones
        instrucciones = fuente_normal.render("Presiona Q para cerrar", True, TEXTO_SECUNDARIO)
        self.pantalla.blit(instrucciones, (panel_x + (panel_ancho - instrucciones.get_width()) // 2,
                                         panel_y + panel_alto - 40))

    def dibujar_inventario(self):
        """Dibuja el inventario del jugador"""
        # Fondo semitransparente
        fondo = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))
        self.pantalla.blit(fondo, (0, 0))

        # Panel de inventario
        panel_ancho = 600
        panel_alto = 500
        panel_x = (self.ANCHO - panel_ancho) // 2
        panel_y = (self.ALTO - panel_alto) // 2

        pygame.draw.rect(self.pantalla, COLOR_FONDO_INVENTARIO,
                        (panel_x, panel_y, panel_ancho, panel_alto))
        pygame.draw.rect(self.pantalla, TEXTO_INVENTARIO,
                        (panel_x, panel_y, panel_ancho, panel_alto), 3)

        # Título
        fuente = self.fuentes['titulo']
        titulo = fuente.render("INVENTARIO", True, TEXTO_INVENTARIO)
        self.pantalla.blit(titulo, (panel_x + (panel_ancho - titulo.get_width()) // 2, panel_y + 20))

        fuente_normal = self.fuentes['normal']
        fuente_peq = self.fuentes['pequena']

        # Items del inventario
        y_pos = panel_y + 70
        items_totales = sum(self.jugador.inventario.values())

        capacidad = fuente_normal.render(f"Capacidad: {items_totales}/{INVENTARIO_MAXIMO}",
                                        True, TEXTO_ITEM)
        self.pantalla.blit(capacidad, (panel_x + 30, y_pos))
        y_pos += 40

        # Listar items con cantidad > 0
        columnas = 2
        col_ancho = panel_ancho // columnas
        col_x = [panel_x + 30, panel_x + 30 + col_ancho]

        items_listados = 0
        for item, cantidad in self.jugador.inventario.items():
            if cantidad > 0:
                col = items_listados % columnas
                fila = items_listados // columnas

                x = col_x[col]
                y = y_pos + (fila * 60)

                # Nombre y cantidad
                item_texto = fuente_normal.render(f"{item.replace('_', ' ').title()}: {cantidad}",
                                                 True, TEXTO_ITEM)
                self.pantalla.blit(item_texto, (x, y))

                # Descripción breve
                desc = ""
                if item == "pocion_vida":
                    desc = "Restaura 1 vida"
                elif item == "balas_extra":
                    desc = "+10 balas al recargar"
                elif item == "pocion_velocidad":
                    desc = "+2 velocidad por 30s"
                elif item == "pocion_fuerza":
                    desc = "+50% daño por 30s"
                elif item == "pocion_defensa":
                    desc = "-50% daño recibido por 30s"

                if desc:
                    desc_texto = fuente_peq.render(desc, True, TEXTO_SECUNDARIO)
                    self.pantalla.blit(desc_texto, (x + 10, y + 25))

                items_listados += 1

        # Instrucciones
        instrucciones = fuente_normal.render("Presiona I para cerrar | E para usar item seleccionado",
                                           True, TEXTO_SECUNDARIO)
        self.pantalla.blit(instrucciones, (panel_x + (panel_ancho - instrucciones.get_width()) // 2,
                                         panel_y + panel_alto - 40))

    def dibujar_tienda(self):
        """Dibuja la interfaz de la tienda"""
        # Fondo semitransparente
        fondo = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))
        self.pantalla.blit(fondo, (0, 0))

        # Panel de tienda
        panel_ancho = 700
        panel_alto = 500
        panel_x = (self.ANCHO - panel_ancho) // 2
        panel_y = (self.ALTO - panel_alto) // 2

        pygame.draw.rect(self.pantalla, COLOR_FONDO_PANEL,
                        (panel_x, panel_y, panel_ancho, panel_alto))
        pygame.draw.rect(self.pantalla, TEXTO_TITULO,
                        (panel_x, panel_y, panel_ancho, panel_alto), 3)

        # Título
        fuente = self.fuentes['titulo']
        titulo = fuente.render("TIENDA", True, TEXTO_TITULO)
        self.pantalla.blit(titulo, (panel_x + (panel_ancho - titulo.get_width()) // 2, panel_y + 20))

        # Puntos del jugador
        fuente_normal = self.fuentes['normal']
        puntos_texto = fuente_normal.render(f"Tus puntos: {self.jugador.puntos}", True, TEXTO_PUNTOS)
        self.pantalla.blit(puntos_texto, (panel_x + 30, panel_y + 70))

        # Items para comprar
        y_pos = panel_y + 110
        comprar_titulo = fuente_normal.render("COMPRAR:", True, TEXTO_ITEM)
        self.pantalla.blit(comprar_titulo, (panel_x + 30, y_pos))
        y_pos += 40

        items_compra = self.tienda.obtener_items_compra()
        for i, item in enumerate(items_compra[:5]):  # Mostrar solo 5 items
            item_texto = fuente_normal.render(f"{i+1}. {item['nombre']} - {item['precio']} pts",
                                            True, TEXTO_ITEM)
            self.pantalla.blit(item_texto, (panel_x + 50, y_pos))

            efecto_texto = fuente_normal.render(f"   {item['efecto']}", True, TEXTO_SECUNDARIO)
            self.pantalla.blit(efecto_texto, (panel_x + 70, y_pos + 25))

            y_pos += 60

        # Instrucciones
        instrucciones = fuente_normal.render("Presiona T para cerrar | 1-5 para comprar | V para vender",
                                           True, TEXTO_SECUNDARIO)
        self.pantalla.blit(instrucciones, (panel_x + (panel_ancho - instrucciones.get_width()) // 2,
                                         panel_y + panel_alto - 40))

    def dibujar_dialogo(self):
        """Dibuja el diálogo con NPC"""
        if not self.hablando_con_npc or not self.dialogo_actual:
            return

        # Panel de diálogo
        dialogo_ancho = self.ANCHO - 200
        dialogo_alto = 150
        dialogo_x = 100
        dialogo_y = self.ALTO - dialogo_alto - 50

        pygame.draw.rect(self.pantalla, COLOR_FONDO_DIALOGO,
                        (dialogo_x, dialogo_y, dialogo_ancho, dialogo_alto))
        pygame.draw.rect(self.pantalla, TEXTO_NPC_NOMBRE,
                        (dialogo_x, dialogo_y, dialogo_ancho, dialogo_alto), 3)

        # Nombre del NPC
        fuente = self.fuentes['subtitulo']
        nombre_texto = fuente.render(f"{self.hablando_con_npc.nombre} ({self.hablando_con_npc.tipo})",
                                   True, TEXTO_NPC_NOMBRE)
        self.pantalla.blit(nombre_texto, (dialogo_x + 20, dialogo_y + 20))

        # Diálogo
        fuente_normal = self.fuentes['normal']
        palabras = self.dialogo_actual.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = linea_actual + " " + palabra if linea_actual else palabra
            if fuente_normal.size(prueba)[0] < dialogo_ancho - 40:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        y_pos = dialogo_y + 60
        for i, linea in enumerate(lineas[:3]):  # Máximo 3 líneas
            linea_texto = fuente_normal.render(linea, True, TEXTO_NPC_DIALOGO)
            self.pantalla.blit(linea_texto, (dialogo_x + 20, y_pos + i * 30))

        # Instrucción
        fuente_peq = self.fuentes['pequena']
        instruccion = fuente_peq.render("Presiona ESPACIO para continuar", True, TEXTO_SECUNDARIO)
        self.pantalla.blit(instruccion, (dialogo_x + dialogo_ancho - instruccion.get_width() - 20,
                                       dialogo_y + dialogo_alto - 30))

    def game_over(self):
        """Maneja el fin del juego"""
        self.franja.mostrar("¡GAME OVER! Presiona F para reiniciar", duracion=5.0)
        self.nivel_completado = True

    def ejecutar(self):
        """Bucle principal del juego"""
        while self.ejecutando:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()

# EJECUTAR EL JUEGO
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
