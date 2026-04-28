# jefe.py — JEFE FINAL: EL LICHE MATEMÁTICO
# Enemigo enorme que ocupa 3×3 tiles (144×144 px), con fases de combate,
# múltiples ataques y un sistema de vida con barra épica.

import pygame
import math
import random
from settings import TAM, TEXTO_TITULO, TEXTO_INCORRECTO

# ─── Constantes del Jefe ──────────────────────────────────────────────────────
TAM_BOSS        = TAM * 3          # 144 × 144 píxeles
VIDA_BOSS       = 30               # Golpes hasta morir
COLOR_BOSS_1    = (80,  0,  120)   # Fase 1 — Púrpura oscuro
COLOR_BOSS_2    = (160, 0,  60)    # Fase 2 — Rojo carmesí
COLOR_BOSS_3    = (220, 100, 0)    # Fase 3 — Naranja fuego
VEL_BOSS_BASE   = 1.2
RADIO_AGRO      = 600              # Distancia a la que persigue al jugador
TIEMPO_ATAQUE   = 90               # Frames entre ataques normales
TIEMPO_ESPECIAL = 300              # Frames entre ataques especiales

# ─── Proyectil del Jefe ───────────────────────────────────────────────────────
class ProyectilBoss:
    """Una bola de energía oscura disparada por el Liche."""

    def __init__(self, x, y, dx, dy, tipo="normal"):
        self.rect   = pygame.Rect(x - 8, y - 8, 16, 16)
        self.dx     = dx
        self.dy     = dy
        self.tipo   = tipo          # "normal", "rapido", "triple", "espiral"
        self.activo = True
        self.t      = 0             # para movimiento espiral

        if tipo == "rapido":
            self.rect.width = self.rect.height = 10
        elif tipo == "espiral":
            self.angulo_extra = random.uniform(0, math.pi * 2)

    def mover(self):
        if self.tipo == "espiral":
            self.t += 0.05
            radio = 2
            self.rect.x += int(self.dx + radio * math.cos(self.t + self.angulo_extra))
            self.rect.y += int(self.dy + radio * math.sin(self.t + self.angulo_extra))
        else:
            self.rect.x += int(self.dx)
            self.rect.y += int(self.dy)

        # Eliminar si sale de los límites del mapa
        if not (-200 < self.rect.x < 5000 and -200 < self.rect.y < 5000):
            self.activo = False

    def dibujar(self, superficie, cam_x, cam_y):
        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y
        r  = self.rect.width // 2

        colores = {
            "normal":  [(180, 0, 255), (100, 0, 160)],
            "rapido":  [(255, 80,  0), (160, 40,  0)],
            "triple":  [(255, 0, 100), (160,  0,  60)],
            "espiral": [(0, 200, 255), (0, 120, 180)],
        }
        c_out, c_in = colores.get(self.tipo, colores["normal"])

        cx = rx + r
        cy = ry + r
        pygame.draw.circle(superficie, c_out, (cx, cy), r)
        pygame.draw.circle(superficie, c_in,  (cx, cy), max(2, r - 4))
        pygame.draw.circle(superficie, (255, 255, 255), (cx, cy), 3)


# ─── Clase Principal del Jefe ─────────────────────────────────────────────────
class LicheMatematico:
    """
    El Liche Matemático — Jefe Final.

    Fases de combate según la vida restante:
      Fase 1 (vida > 20): Persigue lentamente, dispara ráfagas simples.
      Fase 2 (vida 10-20): Más rápido, dispara en triple dirección.
      Fase 3 (vida < 10): Muy rápido, dispara en espiral + invoca esbirros.

    El Liche también puede volverse temporalmente INVULNERABLE hasta que
    el jugador resuelva el cofre más cercano de la sala.
    """

    def __init__(self, x, y):
        self.rect    = pygame.Rect(x, y, TAM_BOSS, TAM_BOSS)
        self.vida    = VIDA_BOSS
        self.vida_max = VIDA_BOSS
        self.fase    = 1
        self.activo  = True
        self.muerto  = False

        # Movimiento
        self.vel     = VEL_BOSS_BASE
        self.dx      = 0.0
        self.dy      = 0.0

        # Temporizadores
        self.t_ataque   = 0
        self.t_especial = 0
        self.t_inmortal = 0   # Frames de invulnerabilidad temporal
        self.t_flash    = 0   # Parpadeo al recibir daño

        # Proyectiles propios
        self.proyectiles: list[ProyectilBoss] = []

        # Estado visual
        self.angulo_rotacion = 0.0
        self.escala_pulso    = 0.0

        # Sprite generado
        self.sprite_cache = {}
        print("💀 ¡El Liche Matemático ha despertado!")

    # ── Lógica principal ──────────────────────────────────────────────────────
    def actualizar_fase(self):
        """Actualiza la fase según la vida restante."""
        porcentaje = self.vida / self.vida_max
        if porcentaje > 0.66:
            self.fase = 1
            self.vel  = VEL_BOSS_BASE
        elif porcentaje > 0.33:
            self.fase = 2
            self.vel  = VEL_BOSS_BASE * 1.6
        else:
            self.fase = 3
            self.vel  = VEL_BOSS_BASE * 2.2

    def mover(self, paredes, jugador_rect):
        """Persigue al jugador respetando paredes."""
        if not self.activo or self.muerto:
            return

        dx = jugador_rect.centerx - self.rect.centerx
        dy = jugador_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist < RADIO_AGRO and dist > 0:
            ndx = dx / dist * self.vel
            ndy = dy / dist * self.vel

            # Movimiento con colisión
            nuevo = self.rect.move(int(ndx), 0)
            if not any(nuevo.colliderect(p) for p in paredes):
                self.rect = nuevo
            nuevo = self.rect.move(0, int(ndy))
            if not any(nuevo.colliderect(p) for p in paredes):
                self.rect = nuevo

        # Pulso visual
        self.angulo_rotacion = (self.angulo_rotacion + 1.5) % 360
        self.escala_pulso = math.sin(pygame.time.get_ticks() * 0.003) * 4

        # Reducir temporizadores
        if self.t_inmortal > 0:
            self.t_inmortal -= 1
        if self.t_flash > 0:
            self.t_flash -= 1

    def atacar(self, jugador_rect):
        """Genera proyectiles según la fase actual."""
        if not self.activo or self.muerto:
            return

        self.t_ataque   += 1
        self.t_especial += 1

        cx = self.rect.centerx
        cy = self.rect.centery
        jx = jugador_rect.centerx
        jy = jugador_rect.centery
        dist = max(1, math.hypot(jx - cx, jy - cy))
        ndx  = (jx - cx) / dist
        ndy  = (jy - cy) / dist

        # ── Ataque básico: disparo directo ──────────────────────────────────
        if self.t_ataque >= TIEMPO_ATAQUE:
            self.t_ataque = 0
            vel = 4 + self.fase
            if self.fase == 1:
                self._disparar(cx, cy, ndx * vel, ndy * vel, "normal")
            elif self.fase == 2:
                # Triple disparo en abanico
                for angulo_offset in [-25, 0, 25]:
                    rad = math.radians(angulo_offset)
                    rdx = ndx * math.cos(rad) - ndy * math.sin(rad)
                    rdy = ndx * math.sin(rad) + ndy * math.cos(rad)
                    self._disparar(cx, cy, rdx * vel, rdy * vel, "triple")
            elif self.fase == 3:
                # Círculo completo de proyectiles en espiral
                for i in range(8):
                    ang = math.radians(i * 45)
                    self._disparar(cx, cy,
                                   math.cos(ang) * vel,
                                   math.sin(ang) * vel,
                                   "espiral")

        # ── Ataque especial ─────────────────────────────────────────────────
        if self.t_especial >= TIEMPO_ESPECIAL:
            self.t_especial = 0
            if self.fase >= 2:
                # Lluvia de proyectiles rápidos
                for i in range(12):
                    ang = math.radians(i * 30)
                    self._disparar(cx, cy,
                                   math.cos(ang) * 7,
                                   math.sin(ang) * 7,
                                   "rapido")

        # Mover proyectiles existentes
        for p in self.proyectiles[:]:
            p.mover()
            if not p.activo:
                self.proyectiles.remove(p)

    def _disparar(self, x, y, dx, dy, tipo):
        self.proyectiles.append(ProyectilBoss(x, y, dx, dy, tipo))

    def recibir_dano(self):
        """Procesa un impacto de bala del jugador."""
        if self.t_inmortal > 0 or self.muerto:
            return False  # Invulnerable ahora mismo

        self.vida -= 1
        self.t_flash = 12
        self.actualizar_fase()

        # Activar escudo temporal en fase 2 y 3
        if self.fase >= 2 and random.random() < 0.20:
            self.t_inmortal = 90
            print("🛡️  El Liche activa su escudo mágico!")

        if self.vida <= 0:
            self.morir()
            return True

        return True

    def morir(self):
        """Marca al Liche como muerto y activa animación de muerte."""
        self.muerto = True
        self.activo = False
        print("💀 ¡EL LICHE MATEMÁTICO HA SIDO DERROTADO!")

    def esta_invulnerable(self):
        return self.t_inmortal > 0

    # ── Dibujado ──────────────────────────────────────────────────────────────
    def dibujar(self, superficie, cam_x, cam_y):
        """Dibuja el Liche y sus proyectiles."""
        # Proyectiles
        for p in self.proyectiles:
            p.dibujar(superficie, cam_x, cam_y)

        if self.muerto:
            self._dibujar_muerte(superficie, cam_x, cam_y)
            return

        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y
        cx = rx + TAM_BOSS // 2
        cy = ry + TAM_BOSS // 2
        r  = TAM_BOSS // 2

        # Aura exterior giratoria
        aura_r = int(r + 20 + self.escala_pulso)
        aura_surf = pygame.Surface((aura_r * 2 + 4, aura_r * 2 + 4), pygame.SRCALPHA)
        aura_cx = aura_r + 2
        aura_cy = aura_r + 2
        for i in range(6):
            ang = math.radians(self.angulo_rotacion + i * 60)
            px = int(aura_cx + aura_r * 0.85 * math.cos(ang))
            py = int(aura_cy + aura_r * 0.85 * math.sin(ang))
            pygame.draw.circle(aura_surf,
                               (180, 0, 255, 120) if self.t_inmortal <= 0 else (255, 215, 0, 180),
                               (px, py), 10)
        superficie.blit(aura_surf, (cx - aura_r - 2, cy - aura_r - 2))

        # Cuerpo principal
        color_cuerpo = {1: COLOR_BOSS_1, 2: COLOR_BOSS_2, 3: COLOR_BOSS_3}[self.fase]
        if self.t_flash > 0 and self.t_flash % 4 < 2:
            color_cuerpo = (255, 255, 255)

        # Escudo dorado si invulnerable
        if self.t_inmortal > 0:
            pygame.draw.circle(superficie, (255, 215, 0), (cx, cy), r + 14, 5)

        pygame.draw.circle(superficie, color_cuerpo, (cx, cy), r)
        pygame.draw.circle(superficie, (0, 0, 0), (cx, cy), r, 4)

        # Corona de huesos
        for i in range(8):
            ang = math.radians(i * 45 - self.angulo_rotacion * 0.5)
            bx  = cx + int((r - 6) * math.cos(ang))
            by  = cy + int((r - 6) * math.sin(ang))
            pygame.draw.circle(superficie, (230, 220, 200), (bx, by), 6)
            pygame.draw.circle(superficie, (0, 0, 0), (bx, by), 6, 2)

        # Ojos brillantes (sigue al jugador visualmente)
        ojo_r = 14
        for ox, oy in [(-22, -15), (22, -15)]:
            pygame.draw.circle(superficie, (255, 50, 0), (cx + ox, cy + oy), ojo_r)
            pygame.draw.circle(superficie, (255, 200, 0), (cx + ox, cy + oy), 8)
            pygame.draw.circle(superficie, (0, 0, 0), (cx + ox, cy + oy), 5)

        # Boca con dientes
        pygame.draw.arc(superficie, (0, 0, 0),
                        (cx - 30, cy + 10, 60, 30), math.pi, 0, 4)
        for i in range(5):
            tx = cx - 20 + i * 10
            pygame.draw.polygon(superficie, (230, 220, 200), [
                (tx, cy + 18), (tx + 4, cy + 18), (tx + 2, cy + 32)
            ])

        # Texto de fase sobre el jefe
        fuente = pygame.font.Font(None, 22)
        fase_str = f"FASE {self.fase}" + (" 🛡" if self.t_inmortal > 0 else "")
        txt = fuente.render(fase_str, True, (255, 215, 0))
        superficie.blit(txt, (cx - txt.get_width() // 2, ry - 20))

        # Barra de vida épica
        self._dibujar_barra_vida(superficie, rx, ry)

    def _dibujar_barra_vida(self, superficie, rx, ry):
        """Barra de vida grande sobre el jefe."""
        ancho_barra = TAM_BOSS + 20
        alto_barra  = 14
        bx = rx - 10
        by = ry - 40

        # Fondo
        pygame.draw.rect(superficie, (40, 0, 0), (bx, by, ancho_barra, alto_barra), border_radius=6)

        # Vida actual
        porcentaje = max(0, self.vida / self.vida_max)
        ancho_vida = int(porcentaje * ancho_barra)
        color_vida = (
            (0, 220, 80)    if porcentaje > 0.66 else
            (220, 220, 0)   if porcentaje > 0.33 else
            (220, 30, 30)
        )
        if ancho_vida > 0:
            pygame.draw.rect(superficie, color_vida,
                             (bx, by, ancho_vida, alto_barra), border_radius=6)

        # Borde
        pygame.draw.rect(superficie, (255, 215, 0),
                         (bx, by, ancho_barra, alto_barra), 2, border_radius=6)

        # Texto
        fuente = pygame.font.Font(None, 20)
        txt = fuente.render(f"LICHE: {self.vida}/{self.vida_max}", True, (255, 255, 255))
        superficie.blit(txt, (bx + (ancho_barra - txt.get_width()) // 2, by + 1))

    def _dibujar_muerte(self, superficie, cam_x, cam_y):
        """Animación de muerte — el Liche se desvanece."""
        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y
        cx = rx + TAM_BOSS // 2
        cy = ry + TAM_BOSS // 2

        surf = pygame.Surface((TAM_BOSS * 2, TAM_BOSS * 2), pygame.SRCALPHA)
        for i in range(12):
            ang = math.radians(i * 30 + pygame.time.get_ticks() * 0.1)
            px  = TAM_BOSS + int(TAM_BOSS * 0.6 * math.cos(ang))
            py  = TAM_BOSS + int(TAM_BOSS * 0.6 * math.sin(ang))
            pygame.draw.circle(surf, (180, 0, 255, 100), (px, py), 12)

        superficie.blit(surf, (cx - TAM_BOSS, cy - TAM_BOSS))

        fuente = pygame.font.Font(None, 36)
        txt = fuente.render("¡DERROTADO!", True, (255, 215, 0))
        superficie.blit(txt, (cx - txt.get_width() // 2, cy - 20))

    # ── HUD global del jefe (se dibuja en la parte superior) ─────────────────
    def dibujar_hud_boss(self, pantalla, ancho_pantalla):
        """Barra de vida enorme en la parte inferior de la pantalla."""
        margen = 40
        ancho  = ancho_pantalla - margen * 2
        alto   = 28
        x      = margen
        y      = 20

        # Fondo
        pygame.draw.rect(pantalla, (20, 0, 30), (x - 2, y - 2, ancho + 4, alto + 4), border_radius=8)
        pygame.draw.rect(pantalla, (40, 0, 60), (x, y, ancho, alto), border_radius=6)

        # Vida
        porcentaje = max(0, self.vida / self.vida_max)
        ancho_vida = int(porcentaje * ancho)
        color = (
            (50, 200, 50)  if porcentaje > 0.66 else
            (200, 200, 0)  if porcentaje > 0.33 else
            (200, 30, 30)
        )
        if ancho_vida > 0:
            pygame.draw.rect(pantalla, color, (x, y, ancho_vida, alto), border_radius=6)

        # Marcadores de fase
        for frac in [0.33, 0.66]:
            fx = x + int(frac * ancho)
            pygame.draw.line(pantalla, (255, 215, 0), (fx, y), (fx, y + alto), 3)

        # Borde dorado
        pygame.draw.rect(pantalla, (255, 215, 0), (x - 2, y - 2, ancho + 4, alto + 4), 3, border_radius=8)

        # Texto centrado
        fuente = pygame.font.Font(None, 26)
        estado = "🛡️ INVULNERABLE" if self.t_inmortal > 0 else f"FASE {self.fase}"
        txt = fuente.render(
            f"💀 LICHE MATEMÁTICO  —  {self.vida}/{self.vida_max}  —  {estado}",
            True, (255, 255, 255)
        )
        pantalla.blit(txt, (x + (ancho - txt.get_width()) // 2, y + 5))
