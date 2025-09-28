# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto **Tres en Raya**! 🎉

Esta guía te ayudará a empezar y te dará toda la información necesaria para hacer contribuciones exitosas.

## 📋 Tabla de Contenidos

- [🏁 Empezando](#-empezando)
- [🎯 Tipos de Contribuciones](#-tipos-de-contribuciones)
- [🔧 Configuración del Entorno](#-configuración-del-entorno)
- [📝 Proceso de Desarrollo](#-proceso-de-desarrollo)
- [🧪 Pruebas](#-pruebas)
- [📖 Estándares de Código](#-estándares-de-código)
- [🚀 Envío de Pull Requests](#-envío-de-pull-requests)
- [🏷️ Sistema de Labels](#️-sistema-de-labels)

## 🏁 Empezando

### 📚 **Para Principiantes**
- Busca issues con la etiqueta `good-first-issue`
- Lee toda la documentación del proyecto
- Únete a las discusiones en GitHub

### 🎓 **Para Estudiantes**
- Perfecto para aprender sobre algoritmos de juegos
- Implementación del algoritmo Minimax
- Arquitectura de aplicaciones web

### 👨‍💻 **Para Desarrolladores Experimentados**
- Mejoras de UI/UX
- Optimizaciones de rendimiento
- Nuevas funcionalidades avanzadas

## 🎯 Tipos de Contribuciones

### 🐛 **Bug Reports**
- Usa el [template de bug report](../../issues/new?template=bug_report.yml)
- Incluye pasos para reproducir el error
- Proporciona información del sistema

### ✨ **Nuevas Características**
- Usa el [template de feature request](../../issues/new?template=feature_request.yml)
- Explica el problema que resuelve
- Proporciona detalles de implementación

### 📚 **Documentación**
- Mejoras al README.md
- Comentarios en el código
- Guías de usuario
- Tutoriales

### 🎨 **Mejoras de UI/UX**
- Diseño responsive
- Accesibilidad
- Animaciones
- Themes

## 🔧 Configuración del Entorno

### **Prerrequisitos**
- Python 3.9+
- Git
- Editor de código (VS Code recomendado)

### **Setup Completo**

```bash
# 1. Fork y clonar el repositorio
git clone https://github.com/TU-USUARIO/tres-en-raya.git
cd tres-en-raya

# 2. Configurar upstream
git remote add upstream https://github.com/Crypt0xDev/tres-en-raya.git

# 3. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 4. Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 isort

# 5. Verificar que todo funciona
python -m pytest tests/
```

## 📝 Proceso de Desarrollo

### **1. Crear una Rama**
```bash
git checkout -b feature/mi-nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
# o  
git checkout -b docs/mejora-documentacion
```

### **2. Convenciones de Nombres**
- `feature/` - nuevas características
- `fix/` - corrección de bugs
- `docs/` - cambios de documentación
- `style/` - cambios de formato
- `refactor/` - refactoring de código
- `test/` - añadir/corregir tests

### **3. Hacer Cambios**
- Escribe código limpio y legible
- Añade comentarios cuando sea necesario
- Sigue las convenciones del proyecto

### **4. Commit Messages**
Usa [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add sound effects to game moves
fix: resolve AI freeze on hard difficulty  
docs: update installation instructions
style: format code with black
test: add tests for minimax algorithm
```

## 🧪 Pruebas

### **Ejecutar Pruebas**
```bash
# Todas las pruebas
python -m pytest

# Con cobertura
python -m pytest --cov=src

# Pruebas específicas
python -m pytest tests/test_game_logic.py

# Modo verbose
python -m pytest -v
```

### **Escribir Pruebas**
- Cada nueva función debe tener tests
- Usa nombres descriptivos
- Cubre casos edge
- Mantén alta cobertura (>80%)

### **Ejemplo de Test**
```python
def test_minimax_chooses_winning_move():
    """Test que la IA elige un movimiento ganador cuando está disponible."""
    game_state = ["X", "X", "", "O", "O", "", "", "", ""]
    ai = GameAI(difficulty="hard")
    move = ai.get_best_move(game_state)
    assert move == 2  # Posición ganadora
```

## 📖 Estándares de Código

### **Python**
- Usa [Black](https://black.readthedocs.io/) para formateo
- Sigue [PEP 8](https://pep8.org/)
- Usa type hints cuando sea posible
- Docstrings para funciones públicas

```python
def calculate_best_move(board: List[str], difficulty: str) -> int:
    """
    Calcula el mejor movimiento para la IA.
    
    Args:
        board: Estado actual del tablero
        difficulty: Nivel de dificultad ("easy", "medium", "hard")
        
    Returns:
        Índice de la mejor posición (0-8)
    """
    # Implementación...
    pass
```

### **JavaScript**
- Usa ES6+ features
- Nombres descriptivos de variables
- Comentarios para lógica compleja
- Consistencia con el código existente

### **HTML/CSS**
- HTML semántico
- CSS responsivo
- Accesibilidad (ARIA labels)
- Compatibilidad con navegadores modernos

### **Formateo Automático**
```bash
# Python
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# JavaScript (si tienes Prettier instalado)
npx prettier --write *.js
```

## 🚀 Envío de Pull Requests

### **Antes de Enviar**
- [ ] ✅ Todas las pruebas pasan
- [ ] 📝 Código formateado correctamente
- [ ] 📚 Documentación actualizada
- [ ] 🧪 Tests añadidos para nuevas funcionalidades
- [ ] 🔄 Rebase con main actualizado

### **Proceso de PR**

1. **Actualizar tu fork**
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

2. **Rebase tu rama**
```bash
git checkout feature/mi-funcionalidad
git rebase main
```

3. **Crear PR**
- Usa el template de PR
- Título descriptivo
- Descripción detallada
- Screenshots si hay cambios visuales
- Referencia issues relacionados

4. **Responder a Reviews**
- Responde a todos los comentarios
- Haz cambios solicitados
- Push nuevos commits

### **Ejemplo de Commit History Limpio**
```
feat: implement AI difficulty selector UI
test: add tests for difficulty switching  
docs: update README with AI difficulty info
fix: resolve selector styling on mobile
```

## 🏷️ Sistema de Labels

### **Priority**
- `priority: high` 🔴 - Crítico
- `priority: medium` 🟡 - Importante  
- `priority: low` 🟢 - Cuando sea posible

### **Type**
- `bug` 🐛 - Error en el código
- `enhancement` ✨ - Nueva funcionalidad
- `documentation` 📚 - Cambios de docs
- `question` ❓ - Pregunta o discusión

### **Status**
- `good-first-issue` 🆕 - Perfecto para principiantes
- `help-wanted` 🤝 - Se necesita ayuda
- `wip` 🚧 - Work in progress
- `review-needed` 👀 - Necesita revisión

### **Areas**
- `ai` 🤖 - Inteligencia artificial
- `ui` 🎨 - Interfaz de usuario
- `performance` ⚡ - Optimización
- `mobile` 📱 - Compatibilidad móvil
- `accessibility` 🔊 - Accesibilidad

## 💡 Ideas de Contribución

### **🎮 Gameplay**
- Nuevos modos de juego (4x4, diferentes reglas)
- Sistema de torneos
- Replay de partidas
- Modo espectador

### **🤖 IA Improvements**
- Algoritmos alternativos (Alpha-Beta pruning)
- IA con personalidades diferentes
- Análisis de movimientos
- Hints para jugadores

### **🎨 UI/UX**  
- Themes personalizables
- Modo oscuro/claro
- Animaciones avanzadas
- Efectos de sonido

### **📱 Mobile & Accessibility**
- PWA (Progressive Web App)
- Soporte para screen readers
- Navegación por teclado
- Gestos táctiles

### **📊 Analytics & Features**
- Estadísticas de juego
- Sistema de logros
- Perfiles de usuario
- Leaderboards

### **🌐 Multiplayer**
- Salas privadas
- Chat en vivo
- Sistema de ranking
- Matchmaking

## 🆘 ¿Necesitas Ayuda?

### **Canales de Comunicación**
- 🐛 **Bugs:** [GitHub Issues](../../issues)
- ❓ **Preguntas:** [GitHub Discussions](../../discussions)
- 💬 **Chat:** Comments en PRs/Issues

### **Recursos Útiles**
- 📖 [Documentación del Proyecto](../README.md)
- 🎮 [Demo en Vivo](https://crypt0xdev.github.io/tres-en-raya/)
- 📚 [Guías de Git](https://git-scm.com/docs)
- 🐍 [Python Style Guide](https://pep8.org/)

---

## 🙏 ¡Gracias por Contribuir!

Cada contribución, sin importar su tamaño, hace que este proyecto sea mejor. ¡Esperamos trabajar contigo! 🚀

---

<div align="center">

*¿Tienes preguntas? No dudes en [abrir un issue](../../issues/new?template=question.yml) o iniciar una [discusión](../../discussions)*

</div>