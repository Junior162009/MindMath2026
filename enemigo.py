# enemigo.py
import pygame
import math
import random

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
TAM = 40
VEL_BASICO = 2
VEL_CAMUFLAJE = 1.5
VEL_DISPARADOR = 1

class EnemigoBasico:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.dx = VEL_BASICO
        self.color = (255, 50, 50)  # Rojo oscuro
        self.tipo = "Básico"
        self.puntos = 20
        self.vida = 1
        self.vida_maxima = 1
        self.velocidad = VEL_BASICO
        self.puede_disparar = False
        self.tiempo_invulnerable = 0
    
    def mover(self, paredes, jugador_rect=None):
        self.rect.x += self.dx
        
        # Reducir tiempo de invulnerabilidad
        if self.tiempo_invulnerable > 0:
            self.tiempo_invulnerable -= 1
        
        for pared in paredes:
            if self.rect.colliderect(pared):
                self.dx *= -1
                self.rect.x += self.dx
                break
    
    def recibir_dano(self):
        """Recibe daño de una bala"""
        if self.tiempo_invulnerable <= 0:
            self.vida -= 1
            self.tiempo_invulnerable = 10  # Invulnerable por 10 frames
            return True
        return False
    
    def dibujar(self, pantalla, cam_x=0, cam_y=0, suelo_img=None):
        rect_cam = pygame.Rect(
            self.rect.x - cam_x,
            self.rect.y - cam_y,
            self.rect.width,
            self.rect.height
        )
        
        # Si está invulnerable, parpadea
        if self.tiempo_invulnerable > 0 and self.tiempo_invulnerable % 4 < 2:
            return  # No dibujar durante el parpadeo
        
        # Cuerpo del enemigo
        pygame.draw.rect(pantalla, self.color, rect_cam)
        pygame.draw.rect(pantalla, (200, 30, 30), rect_cam, 2)
        
        # Ojos
        pygame.draw.circle(pantalla, (255, 255, 255), 
                          (rect_cam.centerx - 8, rect_cam.centery), 6)
        pygame.draw.circle(pantalla, (255, 255, 255), 
                          (rect_cam.centerx + 8, rect_cam.centery), 6)
        pygame.draw.circle(pantalla, (0, 0, 0), 
                          (rect_cam.centerx - 8, rect_cam.centery), 3)
        pygame.draw.circle(pantalla, (0, 0, 0), 
                          (rect_cam.centerx + 8, rect_cam.centery), 3)
        
        # Boca
        pygame.draw.line(pantalla, (0, 0, 0),
                        (rect_cam.centerx - 6, rect_cam.centery + 8),
                        (rect_cam.centerx + 6, rect_cam.centery + 8), 2)
        
        # Barra de vida (solo si tiene más de 1 vida máxima)
        if self.vida_maxima > 1:
            self.dibujar_barra_vida(pantalla, rect_cam)
    
    def dibujar_barra_vida(self, pantalla, rect_cam):
        """Dibuja la barra de vida del enemigo"""
        barra_width = 30
        barra_height = 4
        barra_x = rect_cam.centerx - barra_width // 2
        barra_y = rect_cam.top - 8
        
        # Fondo de la barra
        pygame.draw.rect(pantalla, (50, 50, 50), 
                        (barra_x, barra_y, barra_width, barra_height))
        
        # Vida actual
        vida_width = int((self.vida / self.vida_maxima) * barra_width)
        color_vida = (0, 255, 0) if self.vida > self.vida_maxima * 0.5 else (255, 255, 0) if self.vida > self.vida_maxima * 0.25 else (255, 0, 0)
        pygame.draw.rect(pantalla, color_vida, 
                        (barra_x, barra_y, vida_width, barra_height))

class EnemigoCamuflado:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.dx = VEL_CAMUFLAJE
        self.color = (50, 150, 50)  # Verde oscuro
        self.tipo = "Camuflado"
        self.puntos = 30
        self.vida = 2
        self.vida_maxima = 2
        self.velocidad = VEL_CAMUFLAJE
        self.puede_disparar = False
        self.visible = True
        self.tiempo_camuflaje = 0
        self.duracion_camuflaje = 120  # 2 segundos a 60 FPS
        self.tiempo_invulnerable = 0
    
    def mover(self, paredes, jugador_rect=None):
        # Cambiar entre visible y camuflado
        self.tiempo_camuflaje += 1
        if self.tiempo_camuflaje >= self.duracion_camuflaje:
            self.visible = not self.visible
            self.tiempo_camuflaje = 0
        
        # Reducir tiempo de invulnerabilidad
        if self.tiempo_invulnerable > 0:
            self.tiempo_invulnerable -= 1
        
        self.rect.x += self.dx
        
        for pared in paredes:
            if self.rect.colliderect(pared):
                self.dx *= -1
                self.rect.x += self.dx
                break
    
    def recibir_dano(self):
        """Recibe daño de una bala"""
        if self.tiempo_invulnerable <= 0:
            self.vida -= 1
            self.tiempo_invulnerable = 10  # Invulnerable por 10 frames
            return True
        return False
    
    def dibujar(self, pantalla, cam_x=0, cam_y=0, suelo_img=None):
        if not self.visible and suelo_img:
            # Cuando está camuflado, dibujar el suelo en su lugar
            rect_cam = pygame.Rect(
                self.rect.x - cam_x,
                self.rect.y - cam_y,
                self.rect.width,
                self.rect.height
            )
            
            # Escalar la imagen del suelo para que coincida
            suelo_escalado = pygame.transform.scale(suelo_img, (TAM, TAM))
            pantalla.blit(suelo_escalado, rect_cam)
            
            # Borde sutil para indicar que hay algo
            pygame.draw.rect(pantalla, (100, 100, 100, 100), rect_cam, 1)
            
            # Barra de vida incluso cuando está camuflado
            self.dibujar_barra_vida(pantalla, rect_cam)
        else:
            rect_cam = pygame.Rect(
                self.rect.x - cam_x,
                self.rect.y - cam_y,
                self.rect.width,
                self.rect.height
            )
            
            # Si está invulnerable, parpadea
            if self.tiempo_invulnerable > 0 and self.tiempo_invulnerable % 4 < 2:
                return  # No dibujar durante el parpadeo
            
            # Cuerpo del enemigo camuflado (verde)
            pygame.draw.rect(pantalla, self.color, rect_cam)
            pygame.draw.rect(pantalla, (30, 100, 30), rect_cam, 2)
            
            # Ojos verdes
            pygame.draw.circle(pantalla, (200, 255, 200), 
                              (rect_cam.centerx - 8, rect_cam.centery), 6)
            pygame.draw.circle(pantalla, (200, 255, 200), 
                              (rect_cam.centerx + 8, rect_cam.centery), 6)
            pygame.draw.circle(pantalla, (0, 50, 0), 
                              (rect_cam.centerx - 8, rect_cam.centery), 3)
            pygame.draw.circle(pantalla, (0, 50, 0), 
                              (rect_cam.centerx + 8, rect_cam.centery), 3)
            
            # Boca
            pygame.draw.line(pantalla, (0, 50, 0),
                            (rect_cam.centerx - 6, rect_cam.centery + 8),
                            (rect_cam.centerx + 6, rect_cam.centery + 8), 2)
            
            # Barra de vida
            self.dibujar_barra_vida(pantalla, rect_cam)
    
    def dibujar_barra_vida(self, pantalla, rect_cam):
        """Dibuja la barra de vida del enemigo"""
        barra_width = 30
        barra_height = 4
        barra_x = rect_cam.centerx - barra_width // 2
        barra_y = rect_cam.top - 8
        
        # Fondo de la barra
        pygame.draw.rect(pantalla, (50, 50, 50), 
                        (barra_x, barra_y, barra_width, barra_height))
        
        # Vida actual
        vida_width = int((self.vida / self.vida_maxima) * barra_width)
        color_vida = (0, 255, 0) if self.vida > self.vida_maxima * 0.5 else (255, 255, 0) if self.vida > self.vida_maxima * 0.25 else (255, 0, 0)
        pygame.draw.rect(pantalla, color_vida, 
                        (barra_x, barra_y, vida_width, barra_height))

class EnemigoDisparador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAM, TAM)
        self.dx = VEL_DISPARADOR
        self.color = (50, 100, 255)  # Azul
        self.tipo = "Disparador"
        self.puntos = 50
        self.vida = 3
        self.vida_maxima = 3
        self.velocidad = VEL_DISPARADOR
        self.puede_disparar = True
        self.direccion_disparo = "derecha"
        self.tiempo_invulnerable = 0
    
    def mover(self, paredes, jugador_rect=None):
        # Seguir al jugador si está cerca
        if jugador_rect:
            distancia_x = jugador_rect.centerx - self.rect.centerx
            distancia_y = jugador_rect.centery - self.rect.centery
            
            # Reducir tiempo de invulnerabilidad
            if self.tiempo_invulnerable > 0:
                self.tiempo_invulnerable -= 1
            
            # Solo moverse si el jugador está dentro de cierto rango
            if abs(distancia_x) < 400 and abs(distancia_y) < 300:
                # Actualizar dirección de disparo
                self.direccion_disparo = "derecha" if distancia_x > 0 else "izquierda"
                
                # Moverse hacia el jugador lentamente
                if abs(distancia_x) > 50:  # No acercarse demasiado
                    if distancia_x > 0:
                        self.rect.x += self.velocidad
                    else:
                        self.rect.x -= self.velocidad
                
                if abs(distancia_y) > 50:
                    if distancia_y > 0:
                        self.rect.y += self.velocidad
                    else:
                        self.rect.y -= self.velocidad
            else:
                # Movimiento normal si el jugador está lejos
                self.rect.x += self.dx
        
        # Colisión con paredes
        for pared in paredes:
            if self.rect.colliderect(pared):
                self.dx *= -1
                self.rect.x += self.dx
                break
    
    def recibir_dano(self):
        """Recibe daño de una bala"""
        if self.tiempo_invulnerable <= 0:
            self.vida -= 1
            self.tiempo_invulnerable = 10  # Invulnerable por 10 frames
            return True
        return False
    
    def dibujar(self, pantalla, cam_x=0, cam_y=0, suelo_img=None):
        rect_cam = pygame.Rect(
            self.rect.x - cam_x,
            self.rect.y - cam_y,
            self.rect.width,
            self.rect.height
        )
        
        # Si está invulnerable, parpadea
        if self.tiempo_invulnerable > 0 and self.tiempo_invulnerable % 4 < 2:
            return  # No dibujar durante el parpadeo
        
        # Cuerpo del enemigo disparador (azul)
        pygame.draw.rect(pantalla, self.color, rect_cam)
        pygame.draw.rect(pantalla, (30, 70, 200), rect_cam, 2)
        
        # Ojos azules
        pygame.draw.circle(pantalla, (200, 200, 255), 
                          (rect_cam.centerx - 8, rect_cam.centery), 6)
        pygame.draw.circle(pantalla, (200, 200, 255), 
                          (rect_cam.centerx + 8, rect_cam.centery), 6)
        pygame.draw.circle(pantalla, (0, 0, 100), 
                          (rect_cam.centerx - 8, rect_cam.centery), 3)
        pygame.draw.circle(pantalla, (0, 0, 100), 
                          (rect_cam.centerx + 8, rect_cam.centery), 3)
        
        # Boca
        pygame.draw.line(pantalla, (0, 0, 100),
                        (rect_cam.centerx - 6, rect_cam.centery + 8),
                        (rect_cam.centerx + 6, rect_cam.centery + 8), 2)
        
        # Indicador de cañón de disparo
        if self.direccion_disparo == "derecha":
            pygame.draw.rect(pantalla, (255, 100, 0),
                            (rect_cam.right - 2, rect_cam.centery - 3, 8, 6))
        else:
            pygame.draw.rect(pantalla, (255, 100, 0),
                            (rect_cam.left - 6, rect_cam.centery - 3, 8, 6))
        
        # Barra de vida
        self.dibujar_barra_vida(pantalla, rect_cam)
    
    def dibujar_barra_vida(self, pantalla, rect_cam):
        """Dibuja la barra de vida del enemigo"""
        barra_width = 30
        barra_height = 4
        barra_x = rect_cam.centerx - barra_width // 2
        barra_y = rect_cam.top - 8
        
        # Fondo de la barra
        pygame.draw.rect(pantalla, (50, 50, 50), 
                        (barra_x, barra_y, barra_width, barra_height))
        
        # Vida actual
        vida_width = int((self.vida / self.vida_maxima) * barra_width)
        color_vida = (0, 255, 0) if self.vida > self.vida_maxima * 0.5 else (255, 255, 0) if self.vida > self.vida_maxima * 0.25 else (255, 0, 0)
        pygame.draw.rect(pantalla, color_vida, 
                        (barra_x, barra_y, vida_width, barra_height))
