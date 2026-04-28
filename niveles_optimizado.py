# Niveles Optimizado

# Este archivo contiene los niveles optimizados del juego MindMath2026

from typing import List, Dict

class Nivel:
    def __init__(self, numero: int, dificultad: str, preguntas: List[str], meta: Dict[str, str]) -> None:
        self.numero = numero
        self.dificultad = dificultad
        self.preguntas = preguntas
        self.meta = meta

    def mostrar_nivel(self) -> None:
        print(f"Nivel: {self.numero} - Dificultad: {self.dificultad}")
        # Aquí se pueden agregar más detalles sobre el nivel

niveles = [
    Nivel(1, 'Fácil', ['¿Cuánto es 1 + 1?', '¿Cuánto es 2 + 2?'], {'objetivo': 'Completar 5 preguntas'}),
    Nivel(2, 'Medio', ['¿Cuánto es 3 + 5?', '¿Cuánto es 4 x 2?'], {'objetivo': 'Completar 7 preguntas'}),
    Nivel(3, 'Difícil', ['¿Cuánto es 12 / 4?', '¿Cuánto es 15 - 3?'], {'objetivo': 'Responder correctamente 5 preguntas'}),
    # Agregar más niveles equilibrados hasta el 10
]

# Funciones de soporte

def obtener_nivel_por_numero(numero: int) -> Nivel:
    for nivel in niveles:
        if nivel.numero == numero:
            return nivel
    raise ValueError('Nivel no encontrado')
