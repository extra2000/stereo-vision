# stereo-vision

| License | Versioning | Build |
| ------- | ---------- | ----- |
| [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) | [![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release) | [![Build status](https://ci.appveyor.com/api/projects/status/cilnfjwa52c0bllu/branch/master?svg=true)](https://ci.appveyor.com/project/nikAizuddin/stereo-vision/branch/master) |


Stereo Vision project.


## Podman

Build image:
```
podman build -t extra2000/stereovision .
```


### Example usage

Create output directory:
```
mkdir -pv results
```

For SELinux, label work files as `container_file_t` to allow to be mounted into container:
```
chcon -v -t container_file_t left-image.jpg right-image.jpg out.jpg results
```

How to run:
```
podman run -it --rm -v ./left-image.jpg:/opt/workdir/left-image.jpg:ro -v ./right-image.jpg:/opt/workdir/right-image.jpg:ro -v ./results:/opt/workdir/results:rw localhost/extra2000/stereovision stereovision generate-disparity-image left-image.jpg right-image.jpg results/out.jpg
```


## PIP

Installations:
```
python3 -m pip install .
```

Example usage:
```
stereovision generate-disparity-image left-image.jpg right-image.jpg out.jpg
```


## How to Calculate Camera Matrix Focal Length?

Let,
  g = camera matrix focal length in unit pixel
  f = optical focal length in unit mm

Assume a Pixel 4A phone camera which has 1.40 micro meter pixel pitch and 4.38 mm focal length. The value of g would be:

g = (4.38 * 1000) / 1.40
  = ~3128.6 pixels

Note: 1mm = 1000 micro meter. The optical focal length f needed to be converted to micro meter.


## How to find out pixel pitch for Blender

scale = scene.render.resolution_percentage / 100
pixels_in_u_per_mm = resolution_x_in_px * scale / sensor_width_in_mm
pixels_in_v_per_mm = resolution_y_in_px * scale * aspect_ratio / sensor_height_in_mm
pixel_size_in_u_direction = 1/pixels_in_u_per_mm
pixel_size_in_v_direction = 1/pixels_in_v_per_mm
