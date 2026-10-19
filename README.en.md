# Automation for IngeTrazo

Kinematic component automation for IngeTrazo 0.5.7 or later with Extensions API 2.

Each part can contain several motion blocks. The preview is drawn in the viewport without saving animated transforms to the model; **Stop** always restores the initial position.

> Languages: [Português](README.md) · [English](README.en.md) · [Español](README.es.md)

## Highlights

- Rotation around X, Y, Z, or a free axis defined by two points.
- Linear movement between A and B, with speed in mm/s, direction, and repeat.
- Linear modes: **Accumulate**, **One way**, and **Back and forth**.
- Per-block delay, parameter locks, and several blocks per component.
- Play, Reverse play, Pause, Stop, step backward/forward, and an elapsed-time clock.
- Settings are saved in the `.igz` document and restored when it is reopened.
- Portuguese, English, and Spanish interface, following the IngeTrazo language.

## Installation

1. Close IngeTrazo.
2. In IngeTrazo, open **Extensions → Open plugins folder**.
3. Copy the complete `automacao` folder from this package into that plugins folder.
4. Restart IngeTrazo.

Do not copy `automacao-debug.log`, `__pycache__`, or `.backup_*` files.

## Quick start

1. Open **Automation** and select a part.
2. Click **Add block** and choose Rotation or Linear motion.
3. Choose X, Y, or Z. For a free axis, click **Set motion axis** and pick A and B in the viewport. When B is selected, **2 points** is automatically selected.
4. Set speed, direction, mode, distance/angle, and repeat.
5. Use Play to run every saved component. The clock displays preview time; Stop resets it.

### Linear motion modes

| Mode | Result per repeat |
| --- | --- |
| **Accumulate** | Keeps advancing in the selected direction on each repeat. |
| **One way** | Moves from A to B, then resets to A for the next repeat. |
| **Back and forth** | Moves from A to B and returns to A. |

## Limits

- This is a kinematic preview: it does not calculate collisions, gear meshing, physics, or part constraints.
- Test again after updating IngeTrazo because the extension uses the viewport API.
- The two-point axis requires two different points on the same selected part.

## License

MIT. See [LICENSE](LICENSE).
