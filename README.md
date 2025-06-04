# NumberLink Solver

Implementación de un solucionador automático para el juego NumberLink/FreeFlow usando backtracking con optimizaciones.

## Descripción

Este proyecto implementa:
1. **Interfaz gráfica** para jugar NumberLink manualmente
2. **Solver automático** basado en backtracking con heurísticas
3. **Generador de tableros** aleatorios con diferentes dificultades
4. **Suite de pruebas** y herramientas de análisis

## Estructura del Proyecto

```
.
├── board.py          # Modelo del tablero y operaciones básicas
├── solver.py         # Algoritmo de resolución automática
├── ui.py            # Interfaz gráfica con Tkinter
├── loader.py        # Cargador de archivos de tablero
├── main.py          # Punto de entrada principal
├── test_cases.py    # Casos de prueba
├── statistics.py    # Análisis de rendimiento
├── board_generator.py # Generador de tableros aleatorios
└── example          # Tablero de ejemplo 7x7
```

## Instalación

### Requisitos
- Python 3.7+
- tkinter (incluido en la mayoría de instalaciones de Python)
- matplotlib (opcional, para gráficos de estadísticas)

### Instalación de dependencias opcionales
```bash
pip install matplotlib
```

## Uso

### Ejecutar la aplicación principal
```bash
python main.py
```

### Ejecutar casos de prueba
```bash
python test_cases.py
```

### Generar tableros aleatorios
```bash
python board_generator.py
```

### Analizar rendimiento
```bash
python statistics.py
```

## Formato de Archivo de Tablero

Los tableros se especifican en archivos de texto con el siguiente formato:

```
n,m
fila,columna,numero
fila,columna,numero
...
```

Donde:
- `n,m`: dimensiones del tablero (filas, columnas)
- `fila,columna,numero`: posición y valor de cada número en el tablero (índices desde 1)

### Ejemplo:
```
5,5
1,1,1
1,5,2
3,3,3
5,1,1
5,5,2
```

## Características del Solver

### Algoritmo
- **Backtracking** con búsqueda en profundidad (DFS)
- **Heurísticas** para optimizar el orden de exploración:
  - Resolver primero pares más restrictivos
  - Preferir caminos por los bordes
  - Evitar crear celdas aisladas

### Optimizaciones
1. **Ordenamiento inteligente de pares**: Los pares con menos opciones se resuelven primero
2. **Detección temprana**: Identifica estados sin solución antes de explorarlos completamente
3. **Poda del espacio de búsqueda**: Elimina caminos que claramente no llevan a solución
4. **Límite de tiempo**: Evita que el solver se quede atascado en tableros muy complejos

### Complejidad
- **Peor caso**: O(4^(L*K)) donde L es la longitud promedio de camino y K es el número de pares
- **Práctica**: Mucho mejor gracias a las heurísticas y podas

## Interfaz de Usuario

### Características
- **Modo manual**: Dibuja caminos con el mouse
- **Modo automático**: Resuelve el tablero con un clic
- **Animación**: Opción para ver la solución paso a paso
- **Validación en tiempo real**: Verifica que los caminos sean válidos
- **Detección de victoria**: Notifica cuando el tablero está completo

### Controles
- **Click y arrastrar**: Dibujar caminos entre números
- **Click en número conectado**: Eliminar su camino
- **Botón "Resolver"**: Activar solver automático
- **Botón "Limpiar"**: Eliminar todos los caminos

## Rendimiento

### Tableros de prueba incluidos:
- **3x3 simple**: < 0.01s
- **5x5 complejo**: < 0.1s
- **7x7 (ejemplo)**: < 1s
- **10x10**: 1-10s (dependiendo de la complejidad)

## Limitaciones

1. Solo soporta tableros cuadrados (n×n)
2. El rendimiento degrada exponencialmente para tableros muy grandes (>10×10)
3. No garantiza encontrar la solución más corta, solo una solución válida

## Extensiones Futuras

1. **Soporte para tableros rectangulares**
2. **Múltiples algoritmos de resolución** (A*, algoritmos genéticos)
3. **Editor de tableros** integrado
4. **Modo competitivo** con tiempo límite
5. **Exportación de soluciones** a diferentes formatos

## Autores

- Daniel Sandoval
- Juan Sebastián Mondragón

Pontificia Universidad Javeriana
Análisis de Algoritmos - 2025