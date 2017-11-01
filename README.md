# Reconstruction from depth

Converts an image into 3d mesh using depth map of the image.

## Requirements

* Opencv - Required for reading image
* Numpy  - Required for storing image & for matrix operations

## Usage:

```sh
$ python depthTo3d.py <input-image> <input-depth> <output-ply-file> <fx> <fy> <cx> <cy>

```

### Example:
```sh
$ python depthTo3d.py sofa.jpg sofa_depth.png s.ply 1148.93617021 1150.38461538 750 500

```
