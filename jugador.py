# jugador.py - VERSIÓN ORIGINAL
import pygame
from settings import *

class Jugador:
    def __init__(self):
        self.vel = 4
        self.rect = pygame.Rect(100, 100, TAM, TAM)
        self.direccion = "derecha"

        # Sistema de progreso
        self.operaciones = []
        self.puntos = 0
        self.nivel = 1
        self.experiencia = 0
        self.experiencia_necesaria = EXPERIENCIA_NIVEL_BASE

        # Inventario mejorado
        self.inventario = {
            "balas": BALAS_INICIALES,
            "pocion_vida": 3,
            "llave": 1,
            "mapa": 0,
            "balas_extra": 0,
            "llave_especial": 0,
            "pocion_velocidad": 0,
            "pocion_fuerza": 0,
            "pocion_defensa": 0,
            "mapa_mundial": 0,
            "brujula": 0,
            "antidoto": 0
        }

        # Estadísticas
        self.enemigos_eliminados = 0
        self.cofres_abiertos = 0
        self.areas_exploradas = []
        self.misiones_completadas = 0

        # Efectos temporales
        self.efecto_velocidad = 0
        self.tiempo_efecto_velocidad = 0
        self.efecto_fuerza = 0
        self.tiempo_efecto_fuerza = 0
        self.efecto_defensa = 0
        self.tiempo_efecto_defensa = 0

        # Cargar sprite ORIGINAL
        try:
            img = pygame.image.load("assets/sprites/jugador.png").convert_alpha()
            self.sprite = pygame.transform.scale(img, (TAM, TAM))
            print("✓ Sprite original cargado para jugador")
        except FileNotFoundError:
            print("✗ No se encontró assets/sprites/jugador.png, creando sprite temporal")
            self.sprite = self.crear_sprite_temporal()

        self.sprite_original = self.sprite

    def crear_sprite_temporal(self):
        """Crea un sprite temporal verde simple"""
        sprite = pygame.Surface((TAM, TAM), pygame.SRCALPHA)
        # Círculo verde para el cuerpo
        pygame.draw.circle(sprite, (0, 200, 0), (TAM//2, TAM//2), TAM//2 - 4)

        # Ojos
        pygame.draw.circle(sprite, (255, 255, 255), (TAM//2 - 6, TAM//2 - 5), 4)
        pygame.draw.circle(sprite, (255, 255, 255), (TAM//2 + 6, TAM//2 - 5), 4)
        pygame.draw.circle(sprite, (0, 0, 0), (TAM//2 - 6, TAM//2 - 5), 2)
        pygame.draw.circle(sprite, (0, 0, 0), (TAM//2 + 6, TAM//2 - 5), 2)

        # Boca (sonrisa)
        pygame.draw.arc(sprite, (0, 0, 0),
                       (TAM//2 - 8, TAM//2 + 2, 16, 10),
                       0, 3.14, 2)

        return sprite

    def mover(self, paredes=None):
        if paredes is None:
            paredes = []

        teclas = pygame.key.get_pressed()
        dx = dy = 0

        # Velocidad base + efecto temporal
        velocidad_actual = self.vel + self.efecto_velocidad

        if teclas[pygame.K_a]:  # Izquierda
            dx = -velocidad_actual
            self.direccion = "izquierda"
        if teclas[pygame.K_d]:  # Derecha
            dx = velocidad_actual
            self.direccion = "derecha"
        if teclas[pygame.K_w]:  # Arriba
            dy = -velocidad_actual
        if teclas[pygame.K_s]:  # Abajo
            dy = velocidad_actual

        # Aplicar flip según dirección
        if self.direccion == "izquierda":
            self.sprite = pygame.transform.flip(self.sprite_original, True, False)
        else:
            self.sprite = self.sprite_original

        # Movimiento con colisiones
        nuevo_x = self.rect.move(dx, 0)
        if not any(nuevo_x.colliderect(p) for p in paredes):
            self.rect = nuevo_x

        nuevo_y = self.rect.move(0, dy)
        if not any(nuevo_y.colliderect(p) for p in paredes):
            self.rect = nuevo_y

    def agregar_item(self, item, cantidad=1):
        """Agrega un item al inventario"""
        if item in self.inventario:
            self.inventario[item] += cantidad
        else:
            self.inventario[item] = cantidad
        return True

    def usar_item(self, item, cantidad=1):
        """Usa un item del inventario"""
        if item in self.inventario and self.inventario[item] >= cantidad:
            self.inventario[item] -= cantidad

            # Aplicar efectos según el item
            if item == "pocion_vida":
                pass  # La curación se maneja en el juego principal
            elif item == "pocion_velocidad":
                self.efecto_velocidad = POCION_VELOCIDAD_BONUS
                self.tiempo_efecto_velocidad = pygame.time.get_ticks() + POCION_VELOCIDAD_DURACION
            elif item == "pocion_fuerza":
                self.efecto_fuerza = 0.5  # +50% daño
                self.tiempo_efecto_fuerza = pygame.time.get_ticks() + POCION_VELOCIDAD_DURACION
            elif item == "pocion_defensa":
                self.efecto_defensa = 0.5  # -50% daño recibido
                self.tiempo_efecto_defensa = pygame.time.get_ticks() + POCION_VELOCIDAD_DURACION

            return True
        return False

    def actualizar_efectos(self):
        """Actualiza los efectos temporales"""
        tiempo_actual = pygame.time.get_ticks()

        if self.efecto_velocidad > 0 and tiempo_actual > self.tiempo_efecto_velocidad:
            self.efecto_velocidad = 0

        if self.efecto_fuerza > 0 and tiempo_actual > self.tiempo_efecto_fuerza:
            self.efecto_fuerza = 0

        if self.efecto_defensa > 0 and tiempo_actual > self.tiempo_efecto_defensa:
            self.efecto_defensa = 0

    def agregar_experiencia(self, xp):
        """Agrega experiencia y sube de nivel"""
        self.experiencia += xp
        subio_nivel = False

        while self.experiencia >= self.experiencia_necesaria:
            self.experiencia -= self.experiencia_necesaria
            self.nivel += 1
            self.vel += 0.5  # Mejora de velocidad por nivel
            self.experiencia_necesaria = self.nivel * EXPERIENCIA_NIVEL_BASE
            subio_nivel = True

            # Otorgar recompensa por subir de nivel
            self.puntos += 50
            self.inventario["pocion_vida"] += 2
            self.inventario["balas"] += 10

        return subio_nivel

    def agregar_area_explorada(self, area_id):
        """Agrega un área explorada"""
        if area_id not in self.areas_exploradas:
            self.areas_exploradas.append(area_id)
            return True
        return False

    def obtener_estadisticas(self):
        """Devuelve un diccionario con las estadísticas del jugador"""
        return {
            "nivel": self.nivel,
            "experiencia": f"{self.experiencia}/{self.experiencia_necesaria}",
            "puntos": self.puntos,
            "vidas": VIDAS_INICIALES,
            "enemigos_eliminados": self.enemigos_eliminados,
            "cofres_abiertos": self.cofres_abiertos,
            "areas_exploradas": len(self.areas_exploradas),
            "misiones_completadas": self.misiones_completadas,
            "operaciones_resueltas": len(self.operaciones)
        }

    def dibujar(self, pantalla, cam_x=0, cam_y=0):
        # Dibujar el sprite
        pantalla.blit(self.sprite, (self.rect.x - cam_x, self.rect.y - cam_y))

        # Dibujar efecto visual si tiene poción activa
        tiempo_actual = pygame.time.get_ticks()
        if self.efecto_velocidad > 0 and tiempo_actual < self.tiempo_efecto_velocidad:
            pygame.draw.circle(pantalla, (100, 100, 255, 100),
                             (self.rect.centerx - cam_x, self.rect.centery - cam_y),
                             TAM//2 + 5, 2)

        if self.efecto_fuerza > 0 and tiempo_actual < self.tiempo_efecto_fuerza:
            pygame.draw.circle(pantalla, (255, 100, 100, 100),
                             (self.rect.centerx - cam_x, self.rect.centery - cam_y),
                             TAM//2 + 3, 2)
