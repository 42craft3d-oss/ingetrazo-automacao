# Automatización para IngeTrazo

Automatización cinemática por componente para IngeTrazo 0.5.7 o posterior con API de extensiones 2.

Cada pieza puede tener varios bloques de movimiento. La vista previa se dibuja en el viewport sin guardar transforms animados en el modelo; **Detener** siempre restaura la posición inicial.

> Idiomas: [Português](README.md) · [English](README.en.md) · [Español](README.es.md)

## Características

- Rotación alrededor de X, Y, Z o de un eje libre definido por dos puntos.
- Movimiento lineal entre A y B, con velocidad en mm/s, sentido y repetición.
- Modos lineales: **Acumular**, **Solo ida** e **Ida y vuelta**.
- Retraso por bloque, bloqueos de parámetros y varios bloques por componente.
- Reproducir, reproducción inversa, pausa, detener, paso atrás/adelante y reloj de tiempo transcurrido.
- La configuración se guarda en el documento `.igz` y se restaura al volver a abrirlo.
- Interfaz en portugués, inglés y español según el idioma de IngeTrazo.

## Instalación

1. Cierre IngeTrazo.
2. En IngeTrazo, abra **Extensiones → Abrir carpeta de plugins**.
3. Copie la carpeta completa `automacao` de este paquete a esa carpeta de plugins.
4. Reinicie IngeTrazo.

No copie `automacao-debug.log`, `__pycache__` ni archivos `.backup_*`.

## Inicio rápido

1. Abra **Automatización** y seleccione una pieza.
2. Haga clic en **Añadir bloque** y elija Rotación o Desplazamiento lineal.
3. Elija X, Y o Z. Para un eje libre, haga clic en **Definir eje del movimiento** y marque A y B en el viewport. Al seleccionar B, **2 puntos** se selecciona automáticamente.
4. Ajuste velocidad, sentido, modo, distancia/ángulo y repetición.
5. Use Reproducir para ejecutar todos los componentes guardados. El reloj muestra el tiempo de la vista previa; Detener lo reinicia.

### Modos de desplazamiento lineal

| Modo | Resultado por repetición |
| --- | --- |
| **Acumular** | Continúa avanzando en el sentido seleccionado en cada repetición. |
| **Solo ida** | Se mueve de A a B y vuelve a A para la siguiente repetición. |
| **Ida y vuelta** | Se mueve de A a B y regresa a A. |

## Límites

- Es una vista previa cinemática: no calcula colisiones, engranaje, física ni restricciones entre piezas.
- Pruebe de nuevo después de actualizar IngeTrazo porque la extensión usa la API del viewport.
- El eje de dos puntos necesita dos puntos distintos de la misma pieza seleccionada.

## Licencia

MIT. Consulte [LICENSE](LICENSE).
