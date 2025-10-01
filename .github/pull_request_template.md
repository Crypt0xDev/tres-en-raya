## 📋 Descripción

<!-- Describe brevemente qué cambios incluye este Pull Request y cómo afecta al dominio del juego -->

## 🎯 Tipo de Cambio

- [ ] 🐛 Bug fix (arreglo que no rompe Screaming Architecture)
- [ ] ✨ Nueva característica del dominio (nueva funcionalidad del juego)
- [ ] 🤖 Mejora de IA (estrategias, dificultades, comportamiento)
- [ ] 🏆 Sistema de torneos (ranking, competencias, estadísticas)
- [ ] 🌐 Mejoras web (interfaz, UX, responsividad)
- [ ] 💥 Breaking change (cambio que afecta contratos del dominio)
- [ ] 📚 Documentación (README, arquitectura, API docs)
- [ ] 🎨 Mejoras de estilo/formato (CSS, UI, no afecta lógica)
- [ ] ♻️ Refactoring (mejora código manteniendo funcionalidad)
- [ ] ⚡ Optimización de performance (algoritmos, carga)
- [ ] 🧪 Tests (unitarios, integración, E2E, arquitectura)
- [ ] 🔧 Configuración (CI/CD, deploy, desarrollo)

## 🏗️ Impacto en Screaming Architecture

<!-- Marca las capas afectadas por este PR -->

- [ ] 🎯 **Dominio** (`game/`) - Entidades, reglas, servicios, casos de uso
- [ ] 🚀 **Delivery** (`delivery_mechanisms/`) - Interfaz web Flask
- [ ] 📋 **Application** (`application/`) - Coordinadores y entry points  
- [ ] � **Persistence** (`persistence/`) - Almacenamiento de datos
- [ ] ⚙️ **Infrastructure** (`infrastructure/`) - Configuración y herramientas
- [ ] 🧪 **Tests** (`tests/`) - Validación y calidad

## 🔗 Issue Relacionado

<!-- ¿Este PR resuelve algún issue? Usa 'Fixes #123' o 'Closes #123' -->

Fixes #

## 🧪 Validación y Testing

<!-- Describe las pruebas ejecutadas para verificar tus cambios -->

### ✅ Tests Automatizados
- [ ] **Dominio**: Tests de entidades, reglas y casos de uso pasan
- [ ] **Arquitectura**: Tests de Screaming Architecture compliance pasan  
- [ ] **Integración**: Tests de integración entre capas funcionan
- [ ] **CI/CD**: Tests de GitHub Actions pasan localmente
- [ ] **Web**: Tests de interfaz Flask funcionan correctamente

### 🎯 Funcionalidad del Juego
- [ ] **Lógica básica**: Tablero, movimientos, detección de ganador
- [ ] **IA**: Comportamiento de diferentes dificultades (Easy/Medium/Hard)
- [ ] **Estadísticas**: Tracking de partidas y puntuaciones  
- [ ] **Sesiones**: Gestión correcta de estados de juego
- [ ] **Validaciones**: Manejo correcto de inputs inválidos

### 🌐 Interfaz Web
- [ ] **Funcionalidad**: Juego completo funciona en navegador
- [ ] **Responsividad**: Se ve bien en móviles y desktop
- [ ] **UX**: Interfaz intuitiva y fluida
- [ ] **Performance**: Carga rápida y sin lag
- [ ] **Compatibilidad**: Funciona en Chrome, Firefox, Safari, Edge

### 🧪 Comandos Ejecutados
```bash
# Tests que he ejecutado:
python tests/test_ci_integration.py                    # ✅/❌
python -m pytest tests/test_screaming_architecture_validation.py  # ✅/❌  
python run_web_server.py  # Manual testing            # ✅/❌
```

## 📸 Evidencia Visual (si aplica)

<!-- Para cambios de UI/UX incluye capturas antes/después -->
<!-- Para nuevas funcionalidades incluye GIFs/videos del comportamiento -->

## 📋 Checklist de Calidad

### 🏗️ Screaming Architecture Compliance
- [ ] **Dominio puro**: No he añadido dependencias de frameworks al dominio (`game/`)
- [ ] **Flujo correcto**: Las dependencias apuntan hacia el dominio, no al revés
- [ ] **Use cases**: Los casos de uso actúan como orquestadores puros
- [ ] **Entidades**: La lógica de negocio está en las entidades del dominio
- [ ] **Interfaces**: Los contratos son agnósticos a tecnología

### 💻 Calidad del Código  
- [ ] Mi código sigue las convenciones del proyecto (PEP 8, typing hints)
- [ ] He realizado auto-revisión del código antes del PR
- [ ] Código complejo está documentado con docstrings descriptivos
- [ ] He actualizado README.md si añadí funcionalidades visibles al usuario
- [ ] No hay imports no utilizados ni código comentado/debug
- [ ] Variables y funciones tienen nombres expresivos del dominio

### 🧪 Testing y Validación
- [ ] He añadido/actualizado tests para los cambios realizados
- [ ] Todos los tests existentes siguen pasando (`47 passed`)
- [ ] He ejecutado tests de arquitectura: `pytest tests/test_screaming_architecture_validation.py`
- [ ] He probado la funcionalidad manualmente en el navegador
- [ ] Los workflows de GitHub Actions pasarán con mis cambios

## 🔄 Detalle de Cambios

### 🎯 Dominio (`game/`)
<!-- Cambios en entidades, reglas, servicios o casos de uso -->

**Entidades modificadas:**
- [ ] `Board` - 
- [ ] `Player` - 
- [ ] `GameSession` - 

**Nuevas reglas/servicios:**
- [ ] 

**Casos de uso afectados:**
- [ ] 

### 🌐 Interfaz Web (`delivery_mechanisms/web_ui/`)
<!-- Cambios en Flask adapter, templates, CSS, JS -->

**Rutas/endpoints:**
- [ ] 

**Templates/UI:**
- [ ] 

**Estilos:**
- [ ] 

### � Coordinación (`application/`)
<!-- Cambios en entry points o coordinadores -->

### 💾 Persistencia (`persistence/`)
<!-- Cambios en repositorios o almacenamiento -->

### ⚙️ Infraestructura (`infrastructure/`)
<!-- Cambios en configuración, CI/CD, dependencias -->

### 🧪 Tests (`tests/`)
<!-- Nuevos tests o modificaciones -->

**Tests añadidos:**
- [ ] 

**Tests modificados:** 
- [ ] 

## � Impacto en Deployment

- [ ] **GitHub Pages**: Cambios compatibles con despliegue estático
- [ ] **Flask Local**: Servidor de desarrollo sigue funcionando
- [ ] **Performance**: No impacto negativo en tiempos de respuesta
- [ ] **Dependencies**: No nuevas dependencias o todas están en requirements.txt

## 📝 Notas para Revisores

<!-- Información importante que los reviewers deben saber -->
<!-- Decisiones de diseño, trade-offs, áreas que necesitan atención especial -->

**¿Qué revisar especialmente?**
- [ ] 

**¿Hay algún trade-off o decisión controversial?**
- [ ] 

**¿Este cambio prepara el terreno para algo más grande?**
- [ ]