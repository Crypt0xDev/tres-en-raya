# 🤖 GitHub Actions Workflows

Este directorio contiene los workflows automatizados para CI/CD del proyecto Tres en Raya.

## ✅ Workflows Disponibles

### 🧪 [Python Tests](test.yml)
- **Trigger:** Push/PR a `main` o `develop`
- **Función:** Ejecuta tests principales con Python 3.11
- **Incluye:** 
  - Tests de dominio
  - Tests de arquitectura Screaming
  - Tests de integración CI
  - Cobertura de código

### 🧪 [Multi-Python Tests](multi-python-test.yml) 
- **Trigger:** Manual (`workflow_dispatch`)
- **Función:** Ejecuta tests en múltiples versiones de Python (3.9-3.12)
- **Objetivo:** Compatibilidad multiplataforma

### 🧪 [Test Pull Requests](test-pr.yml)
- **Trigger:** Pull Requests a `main`
- **Función:** Validación rápida de PRs
- **Tests:** Core functionality + arquitectura

### 🔒 [Security Audit](security.yml)
- **Trigger:** Diario (2 AM UTC), Push, PR
- **Función:** Escaneo de seguridad completo
- **Herramientas:**
  - `pip-audit` - Vulnerabilidades en dependencias
  - `safety` - Base de datos de seguridad Python
  - `bandit` - Análisis de código estático

### 🚀 [Deploy to GitHub Pages](deploy.yml)
- **Trigger:** Push a `main`, Manual
- **Función:** Despliega aplicación web a GitHub Pages
- **Incluye:** Archivos estáticos, landing page, app

## 🎯 Arquitectura de Testing

Los workflows están diseñados para validar:

```
✅ Screaming Architecture Compliance
├── 🎯 Dominio independiente de frameworks  
├── 🔄 Flujo de dependencias correcto
├── 🧪 Use cases como orquestadores
└── 📦 Entidades con lógica de negocio

✅ Funcionalidad Core
├── 🎮 Lógica del juego tres en raya
├── 🤖 Sistema de IA funcionando
├── 📊 Estadísticas y puntuación
└── 🌐 Interfaz web Flask

✅ Calidad de Código
├── 🔍 Tests unitarios y de integración
├── 📈 Cobertura de código
├── 🔒 Análisis de seguridad
└── 🧹 Linting y formato
```

## 🔧 Configuración Local

Para ejecutar los mismos tests que GitHub Actions:

```bash
# Instalar dependencias
pip install -r infrastructure/development/requirements-ci.txt

# Tests principales
python tests/test_ci_integration.py
python -m pytest tests/test_game_logic.py tests/test_helpers.py -v

# Tests de arquitectura
python -m pytest tests/test_screaming_architecture_validation.py -v

# Análisis de seguridad
bandit -r game/ delivery_mechanisms/ application/ -ll
safety check
pip-audit
```

## 📊 Estado de los Workflows

| Workflow | Estado | Descripción |
|----------|--------|-------------|
| Python Tests | ✅ | Tests principales funcionando |
| Multi-Python | ✅ | Compatibilidad multiplataforma |  
| Security Audit | ✅ | Escaneo de vulnerabilidades |
| Deploy Pages | ✅ | Despliegue automático |
| Test PRs | ✅ | Validación de pull requests |

## 🚨 Troubleshooting

### Error: Module not found
- Verificar que `PYTHONPATH` incluye la raíz del proyecto
- Comprobar que `conftest.py` está configurado correctamente

### Error: Requirements not found  
- Los workflows usan `infrastructure/development/requirements-ci.txt`
- Verificar que el archivo existe y tiene las dependencias correctas

### Tests fallando en CI pero no localmente
- Diferencias en versión de Python
- Verificar imports absolutos vs relativos
- Revisar configuración de `pytest.ini`

## 🎯 Filosofía de Testing

Los workflows siguen los principios de **Screaming Architecture**:

1. **Domain-Centric:** Tests que validan el dominio del juego
2. **Technology Agnostic:** Tests independientes de frameworks
3. **Fast Feedback:** Tests rápidos para desarrollo ágil
4. **Security First:** Escaneo continuo de vulnerabilidades
5. **Quality Gates:** No deploy sin tests pasando