"""
AIStrategy - Estrategias de Inteligencia Artificial para Tres en Raya.

Este módulo define las diferentes estrategias que puede usar la IA
para tomar decisiones durante el juego.
"""

from typing import List, Optional, Tuple, Dict, Any
from enum import Enum
from abc import ABC, abstractmethod
import random

from game.entities import Board, Position, CellState, Player, PlayerSymbol
from .victory_conditions import VictoryConditions


class StrategyType(Enum):
    """Tipos de estrategia de IA disponibles."""
    RANDOM = "random"
    DEFENSIVE = "defensive" 
    AGGRESSIVE = "aggressive"
    MINIMAX = "minimax"
    STRATEGIC = "strategic"


class DecisionWeight(Enum):
    """Pesos para la toma de decisiones estratégicas."""
    CRITICAL = 1000    # Movimientos que ganan o evitan perder
    HIGH = 100         # Movimientos muy buenos
    MEDIUM = 50        # Movimientos moderadamente buenos  
    LOW = 10          # Movimientos poco importantes
    MINIMAL = 1       # Movimientos de último recurso


class AIStrategyBase(ABC):
    """
    Clase base abstracta para estrategias de IA.
    
    Define la interfaz común que deben implementar todas las estrategias
    de inteligencia artificial en el juego.
    """
    
    def __init__(self, victory_conditions: VictoryConditions):
        """
        Inicializa la estrategia base.
        
        Args:
            victory_conditions: Instancia para verificar condiciones de victoria
        """
        self.victory_conditions = victory_conditions
    
    @abstractmethod
    def select_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """
        Selecciona el mejor movimiento según esta estrategia.
        
        Args:
            board: Estado actual del tablero
            ai_player: Jugador IA que debe mover
            
        Returns:
            Posición seleccionada o None si no hay movimientos válidos
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Obtiene el nombre descriptivo de la estrategia.
        
        Returns:
            Nombre de la estrategia
        """
        pass


class RandomStrategy(AIStrategyBase):
    """Estrategia aleatoria - selecciona movimientos al azar."""
    
    def select_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """Selecciona una posición aleatoria disponible."""
        available_positions = board.get_empty_positions()
        
        if not available_positions:
            return None
        
        return random.choice(available_positions)
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia."""
        return "Aleatoria"


class DefensiveStrategy(AIStrategyBase):
    """Estrategia defensiva - prioriza bloquear al oponente."""
    
    def select_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """Selecciona movimiento priorizando la defensa."""
        if not ai_player.symbol:
            return None
        
        available_positions = board.get_empty_positions()
        if not available_positions:
            return None
        
        ai_state = CellState.PLAYER_X if ai_player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        opponent_state = CellState.PLAYER_O if ai_state == CellState.PLAYER_X else CellState.PLAYER_X
        
        # 1. Si puede ganar, ganar
        winning_moves = self.victory_conditions.get_threats(board, ai_state)
        if winning_moves:
            return winning_moves[0]
        
        # 2. Si el oponente puede ganar, bloquear
        blocking_moves = self.victory_conditions.get_threats(board, opponent_state)
        if blocking_moves:
            return blocking_moves[0]
        
        # 3. Tomar el centro si está disponible
        center = Position(1, 1)
        if center in available_positions:
            return center
        
        # 4. Tomar una esquina
        corners = [Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)]
        available_corners = [pos for pos in corners if pos in available_positions]
        if available_corners:
            return random.choice(available_corners)
        
        # 5. Cualquier posición disponible
        return random.choice(available_positions)
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia."""
        return "Defensiva"


class AggressiveStrategy(AIStrategyBase):
    """Estrategia agresiva - prioriza crear amenazas y forks."""
    
    def select_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """Selecciona movimiento priorizando el ataque."""
        if not ai_player.symbol:
            return None
        
        available_positions = board.get_empty_positions()
        if not available_positions:
            return None
        
        ai_state = CellState.PLAYER_X if ai_player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        opponent_state = CellState.PLAYER_O if ai_state == CellState.PLAYER_X else CellState.PLAYER_X
        
        # 1. Si puede ganar, ganar
        winning_moves = self.victory_conditions.get_threats(board, ai_state)
        if winning_moves:
            return winning_moves[0]
        
        # 2. Crear fork si es posible
        fork_positions = self.victory_conditions.get_fork_positions(board, ai_state)
        if fork_positions:
            return fork_positions[0]
        
        # 3. Si el oponente puede ganar, bloquear
        blocking_moves = self.victory_conditions.get_threats(board, opponent_state)
        if blocking_moves:
            return blocking_moves[0]
        
        # 4. Crear amenazas (posiciones que fuerzan al oponente a defenderse)
        threat_creating_moves = self._find_threat_creating_moves(board, ai_state, available_positions)
        if threat_creating_moves:
            return threat_creating_moves[0]
        
        # 5. Tomar el centro si está disponible
        center = Position(1, 1)
        if center in available_positions:
            return center
        
        # 6. Tomar esquinas
        corners = [Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)]
        available_corners = [pos for pos in corners if pos in available_positions]
        if available_corners:
            return random.choice(available_corners)
        
        # 7. Cualquier posición disponible
        return random.choice(available_positions)
    
    def _find_threat_creating_moves(self, board: Board, ai_state: CellState, available_positions: List[Position]) -> List[Position]:
        """Encuentra movimientos que crean amenazas."""
        threat_moves = []
        
        for position in available_positions:
            # Simular movimiento
            temp_board = self._copy_board(board)
            from game.entities import Move
            move = Move(position=position, player=ai_state)
            
            try:
                temp_board.place_move(move)
                
                # Contar amenazas después del movimiento
                threats_after = self.victory_conditions.get_threats(temp_board, ai_state)
                
                # Si crea al menos una amenaza, es bueno
                if len(threats_after) >= 1:
                    threat_moves.append(position)
                    
            except Exception:
                continue
        
        return threat_moves
    
    def _copy_board(self, board: Board) -> Board:
        """Crea una copia del tablero."""
        new_board = Board()
        new_board.reset()
        
        board_list = board.to_list()
        for row in range(3):
            for col in range(3):
                cell_value = board_list[row][col]
                if cell_value != ' ':
                    cell_state = CellState.PLAYER_X if cell_value == 'X' else CellState.PLAYER_O
                    position = Position(row, col)
                    from game.entities import Move
                    move = Move(position=position, player=cell_state)
                    new_board.place_move(move)
        
        return new_board
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia."""
        return "Agresiva"


class MinimaxStrategy(AIStrategyBase):
    """Estrategia minimax - algoritmo óptimo para tres en raya."""
    
    def select_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """Selecciona el mejor movimiento usando minimax."""
        if not ai_player.symbol:
            return None
        
        available_positions = board.get_empty_positions()
        if not available_positions:
            return None
        
        ai_state = CellState.PLAYER_X if ai_player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        opponent_state = CellState.PLAYER_O if ai_state == CellState.PLAYER_X else CellState.PLAYER_X
        
        best_score = float('-inf')
        best_move = available_positions[0]
        
        for position in available_positions:
            # Simular movimiento
            temp_board = self._copy_board(board)
            from game.entities import Move
            move = Move(position=position, player=ai_state)
            temp_board.place_move(move)
            
            # Evaluar con minimax
            score = self._minimax(temp_board, 0, False, ai_state, opponent_state)
            
            if score > best_score:
                best_score = score
                best_move = position
        
        return best_move
    
    def _minimax(self, board: Board, depth: int, is_maximizing: bool, ai_state: CellState, opponent_state: CellState) -> float:
        """Algoritmo minimax recursivo."""
        # Verificar condiciones de parada
        winner = self.victory_conditions.get_winner(board)
        
        if winner == ai_state:
            return 10 - depth  # IA gana (preferir victoria rápida)
        elif winner == opponent_state:
            return depth - 10  # Oponente gana (preferir derrota tardía)
        elif board.is_full():
            return 0  # Empate
        
        available_positions = board.get_empty_positions()
        
        if is_maximizing:
            best_score = float('-inf')
            for position in available_positions:
                # Simular movimiento de IA
                temp_board = self._copy_board(board)
                from game.entities import Move
                move = Move(position=position, player=ai_state)
                temp_board.place_move(move)
                
                score = self._minimax(temp_board, depth + 1, False, ai_state, opponent_state)
                best_score = max(score, best_score)
            
            return best_score
        else:
            best_score = float('inf')
            for position in available_positions:
                # Simular movimiento del oponente
                temp_board = self._copy_board(board)
                from game.entities import Move
                move = Move(position=position, player=opponent_state)
                temp_board.place_move(move)
                
                score = self._minimax(temp_board, depth + 1, True, ai_state, opponent_state)
                best_score = min(score, best_score)
            
            return best_score
    
    def _copy_board(self, board: Board) -> Board:
        """Crea una copia del tablero."""
        new_board = Board()
        new_board.reset()
        
        board_list = board.to_list()
        for row in range(3):
            for col in range(3):
                cell_value = board_list[row][col]
                if cell_value != ' ':
                    cell_state = CellState.PLAYER_X if cell_value == 'X' else CellState.PLAYER_O
                    position = Position(row, col)
                    from game.entities import Move
                    move = Move(position=position, player=cell_state)
                    new_board.place_move(move)
        
        return new_board
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia."""
        return "Minimax (Óptima)"


class StrategicStrategy(AIStrategyBase):
    """Estrategia estratégica - combina múltiples heurísticas con pesos."""
    
    def select_move(self, board: Board, ai_player: Player) -> Optional[Position]:
        """Selecciona movimiento usando análisis estratégico con pesos."""
        if not ai_player.symbol:
            return None
        
        available_positions = board.get_empty_positions()
        if not available_positions:
            return None
        
        ai_state = CellState.PLAYER_X if ai_player.symbol == PlayerSymbol.X else CellState.PLAYER_O
        opponent_state = CellState.PLAYER_O if ai_state == CellState.PLAYER_X else CellState.PLAYER_X
        
        # Evaluar cada posición disponible
        position_scores = {}
        
        for position in available_positions:
            score = self._evaluate_position(board, position, ai_state, opponent_state)
            position_scores[position] = score
        
        # Seleccionar la posición con mayor puntuación
        best_position = max(position_scores.keys(), key=lambda pos: position_scores[pos])
        return best_position
    
    def _evaluate_position(self, board: Board, position: Position, ai_state: CellState, opponent_state: CellState) -> int:
        """Evalúa una posición usando múltiples criterios."""
        score = 0
        
        # Simular movimiento
        temp_board = self._copy_board(board)
        from game.entities import Move
        move = Move(position=position, player=ai_state)
        
        try:
            temp_board.place_move(move)
        except Exception:
            return -1000  # Movimiento inválido
        
        # 1. Verificar si es movimiento ganador
        if self.victory_conditions.get_winner(temp_board) == ai_state:
            score += DecisionWeight.CRITICAL.value
        
        # 2. Verificar si bloquea victoria del oponente
        original_opponent_threats = self.victory_conditions.get_threats(board, opponent_state)
        if position in original_opponent_threats:
            score += DecisionWeight.CRITICAL.value
        
        # 3. Verificar si crea fork
        if self.victory_conditions.is_fork_opportunity(board, position, ai_state):
            score += DecisionWeight.HIGH.value
        
        # 4. Contar amenazas creadas
        threats_after = self.victory_conditions.get_threats(temp_board, ai_state)
        score += len(threats_after) * DecisionWeight.MEDIUM.value
        
        # 5. Posiciones estratégicas del tablero
        score += self._get_positional_value(position)
        
        # 6. Control del centro y esquinas
        score += self._get_control_value(position, board)
        
        # 7. Análisis de potencial futuro
        control_analysis = self.victory_conditions.analyze_board_control(temp_board)
        score += control_analysis.get("control_advantage", 0) * DecisionWeight.LOW.value
        
        return score
    
    def _get_positional_value(self, position: Position) -> int:
        """Obtiene el valor posicional de una ubicación en el tablero."""
        # Centro tiene mayor valor
        if position.row == 1 and position.col == 1:
            return DecisionWeight.MEDIUM.value
        
        # Esquinas tienen valor medio
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        if (position.row, position.col) in corners:
            return DecisionWeight.LOW.value
        
        # Lados tienen menor valor
        return DecisionWeight.MINIMAL.value
    
    def _get_control_value(self, position: Position, board: Board) -> int:
        """Evalúa el valor de control que proporciona una posición."""
        control_value = 0
        
        # Valor por líneas que la posición puede formar parte
        lines_count = self._count_lines_through_position(position)
        control_value += lines_count * DecisionWeight.MINIMAL.value
        
        # Bonificación si es la primera marca en una línea
        if self._is_first_in_potential_lines(board, position):
            control_value += DecisionWeight.LOW.value
        
        return control_value
    
    def _count_lines_through_position(self, position: Position) -> int:
        """Cuenta cuántas líneas ganadoras pasan por una posición."""
        from .victory_conditions import VictoryConditions
        
        count = 0
        pos_tuple = (position.row, position.col)
        
        for line in VictoryConditions.WINNING_LINES:
            if pos_tuple in line:
                count += 1
        
        return count
    
    def _is_first_in_potential_lines(self, board: Board, position: Position) -> bool:
        """Verifica si la posición sería la primera marca en líneas potenciales."""
        from .victory_conditions import VictoryConditions
        
        board_state = board.to_list()
        pos_tuple = (position.row, position.col)
        
        for line in VictoryConditions.WINNING_LINES:
            if pos_tuple in line:
                line_values = [board_state[row][col] for row, col in line]
                # Si toda la línea está vacía, esta sería la primera marca
                if all(val == ' ' for val in line_values):
                    return True
        
        return False
    
    def _copy_board(self, board: Board) -> Board:
        """Crea una copia del tablero."""
        new_board = Board()
        new_board.reset()
        
        board_list = board.to_list()
        for row in range(3):
            for col in range(3):
                cell_value = board_list[row][col]
                if cell_value != ' ':
                    cell_state = CellState.PLAYER_X if cell_value == 'X' else CellState.PLAYER_O
                    position = Position(row, col)
                    from game.entities import Move
                    move = Move(position=position, player=cell_state)
                    new_board.place_move(move)
        
        return new_board
    
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia."""
        return "Estratégica Avanzada"


class AIStrategyFactory:
    """
    Factory para crear estrategias de IA.
    
    Encapsula la lógica de creación de diferentes estrategias,
    siguiendo el patrón Factory del dominio.
    """
    
    @staticmethod
    def create_strategy(strategy_type: StrategyType, victory_conditions: VictoryConditions) -> AIStrategyBase:
        """
        Crea una instancia de estrategia según el tipo especificado.
        
        Args:
            strategy_type: Tipo de estrategia a crear
            victory_conditions: Instancia de condiciones de victoria
            
        Returns:
            Instancia de la estrategia solicitada
            
        Raises:
            ValueError: Si el tipo de estrategia no es válido
        """
        strategy_map = {
            StrategyType.RANDOM: RandomStrategy,
            StrategyType.DEFENSIVE: DefensiveStrategy,
            StrategyType.AGGRESSIVE: AggressiveStrategy,
            StrategyType.MINIMAX: MinimaxStrategy,
            StrategyType.STRATEGIC: StrategicStrategy,
        }
        
        strategy_class = strategy_map.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Tipo de estrategia no válido: {strategy_type}")
        
        return strategy_class(victory_conditions)
    
    @staticmethod
    def get_available_strategies() -> List[StrategyType]:
        """
        Obtiene la lista de estrategias disponibles.
        
        Returns:
            Lista de tipos de estrategia disponibles
        """
        return list(StrategyType)
    
    @staticmethod
    def get_strategy_description(strategy_type: StrategyType) -> str:
        """
        Obtiene la descripción de una estrategia.
        
        Args:
            strategy_type: Tipo de estrategia
            
        Returns:
            Descripción textual de la estrategia
        """
        descriptions = {
            StrategyType.RANDOM: "Selecciona movimientos completamente al azar. Ideal para principiantes.",
            StrategyType.DEFENSIVE: "Prioriza bloquear al oponente y defender posiciones. Estrategia conservadora.",
            StrategyType.AGGRESSIVE: "Busca crear amenazas y forks. Estrategia ofensiva.",
            StrategyType.MINIMAX: "Algoritmo óptimo que nunca pierde. La estrategia más fuerte.",
            StrategyType.STRATEGIC: "Combina múltiples heurísticas con análisis posicional avanzado."
        }
        
        return descriptions.get(strategy_type, "Descripción no disponible.")