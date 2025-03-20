# Section Cutter Blender Script

This Blender Python script creates a “cutter” object from a 2D polygon that is extended along the Z-axis. It then applies a boolean modifier (using the INTERSECT operation with the EXACT solver) to all mesh objects in the scene (excluding the cutter itself). The result is that only the parts of the objects that intersect with the cutter volume remain.

## Features
- **Cutter Creation from Polygon**:
The create_cutter_from_polygon function takes a list of 2D (x, y) coordinates and extends them into a closed volume along the Z-axis.
- **Boolean Modifier Application**:
The apply_boolean_modifier function adds a boolean modifier to a given object, using the cutter object for an INTERSECT operation with the EXACT solver for higher precision.
- **Batch Processing**:
The apply_boolean_to_all_scene_objects function loops through all mesh objects in the scene (excluding the cutter) and applies the boolean modifier.
- **Customizable Parameters**:
Easily adjust the polygon coordinates, Z-axis extension values, and boolean settings to suit your needs.

## Requirements
- Blender 2.8 or later.
- Familiarity with Blender’s Scripting workspace.

## Usage
 1. **Open Blender** and switch to the **Scripting** workspace.
 2. **Copy and paste** the script into a new text block in the Blender Text Editor.
 3. **Customize the polygon** by modifying the points list as desired.
 4. **Run the script.**
The script will create the cutter object from the provided polygon and then apply the boolean modifier to all mesh objects in the scene (excluding the cutter).

## Example

The sample code uses a rectangle defined by the following points:

```python
points = [
    (-5000, 2500),
    (0, 2500),
    (0, -2500),
    (-5000, -2500),
]
```

This cutter is then applied to every mesh object in the scene via the apply_boolean_to_all_scene_objects function.

## **Additional Notes**
- **Texture Mapping & Materials**:
This script focuses on geometry. When applying boolean operations, material and UV mapping information may be lost or require manual reassignment. Consider baking textures or reassigning materials post-operation if needed.
- **Non-Destructive Workflow**:
The boolean modifiers are added but not automatically applied. You can preview the results and manually apply the modifiers if desired.
- **Cutter Visibility**:
The cutter object is set to wireframe in the viewport and hidden in renders to avoid interfering with your final output.

## Limitations
- **Mesh Matching Issues**:
After performing the boolean operation, some meshes may not match perfectly along the cut edges. This can result in unexpected geometry artifacts, such as gaps or misaligned vertices.
- **Post-Processing Required**:
To improve results, consider applying additional cleanup operations, such as merging by distance, remeshing, or manually adjusting the affected areas.
- **Complex Geometry Considerations**:
Boolean operations can be less reliable when dealing with highly detailed or non-manifold geometry. Ensuring clean topology before applying the script can help minimize errors.

## License

Feel free to modify and use this script in your projects as needed.

---
