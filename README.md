# Copy Transform to Clipboard (Blender Addon)

A small Blender 4.0+ addon that copies the active object's transform to your system clipboard, either as plain Blender values or pre-converted to **Unreal Engine** format, ready to paste into the UE editor.

## Features

- Copy **Location**, **Rotation**, and **Scale** (individually toggleable)
- **Plain copy** : raw Blender values, easy to paste into scripts, docs, or chat
- **Unreal copy** :  converts units (m → cm), remaps axes (Y-up → X-forward), and outputs UE-style fields
- Works with both Euler and Quaternion rotation modes
- Lives in the 3D Viewport sidebar (N-panel) for quick access

## Output formats

**Plain** (unchanged Blender values):
```
Location: (1.000000, 2.000000, 0.500000)
Rotation (Euler): (0.000000, 0.000000, 0.000000)
Scale: (1.000000, 1.000000, 1.000000)
```

**Unreal Engine**:
```
(X=-200.000000,Y=100.000000,Z=50.000000)
(Roll=0.000000,Pitch=0.000000,Yaw=0.000000)
(X=1.000000,Y=1.000000,Z=1.000000)
```

## Blender → Unreal conversion

| Blender | Unreal |
|---------|--------|
| +X | +Y |
| +Y | -X |
| +Z | +Z |
| meters | centimeters |

Formulas used:

```
UE_X = -Blender_Y * 100
UE_Y =  Blender_X * 100
UE_Z =  Blender_Z * 100
```

Rotation is converted from radians to degrees and remapped to UE's Roll/Pitch/Yaw convention. Scale is axis-remapped (X ↔ Y) without unit conversion.

## Installation

1. Download `copy_transform_clipboard.py` from this repo.
2. Open Blender **4.0** or newer.
3. Go to **Edit → Preferences → Add-ons**.
4. Click **Install…**, select the `.py` file, and confirm.
5. Enable the checkbox next to **Copy Transform to Clipboard**.
6. (Optional) Click the dropdown arrow next to the addon and choose **Save Preferences** so it stays enabled after restart.

## Usage

1. Select an object in the 3D Viewport.
2. Press **N** to open the sidebar.
3. Click the **Transform Copy** tab.
4. Tick the channels you want: **Location**, **Rotation**, **Scale**.
5. Click one of the buttons:
   - **Copy to Clipboard** : plain Blender values
   - **Copy to Clipboard (Unreal)** : UE-formatted values
6. The transform is now on your system clipboard. Paste it anywhere with `Ctrl+V` (or `Cmd+V` on macOS).

### Example workflow

You're blocking out a level in Blender, exporting a mesh to UE, and want the actor to land at the exact same world position.

1. In Blender, select your object.
2. Open the **Transform Copy** panel.
3. Enable only **Location**.
4. Click **Copy to Clipboard (Unreal)**.
5. In UE, select your actor, go to the **Details** panel → **Transform** → **Location**, click the field, and paste.

## Notes & caveats

- The addon reads only the **active object**. Multi-object batch copying is not supported (yet).
- Rotation conversion is a best-effort remap. Depending on your UE project settings and import pipeline (FBX vs Datasmith), you may need to flip a sign. If rotation looks wrong, open an issue with the input and expected output.
- Numbers use 6 decimal places. To change precision, edit the `:.6f` format strings in the script.
- Tested on Blender 4.0. Should work on 4.1+ but has not been verified.

## Compatibility

- **Blender:** 4.0 or newer
- **OS:** Windows, macOS, Linux (clipboard API is cross-platform)

## File structure

```
copy_transform_clipboard.py   # the addon (single file)
README.md                     # this file
```

## License

MIT : do whatever you want with it.

## Contributing

PRs welcome. If you hit a conversion edge case (odd axis orientation, non-uniform scale, parented objects, etc.), open an issue with:
- The Blender object's transform
- What the addon output
- What Unreal expected