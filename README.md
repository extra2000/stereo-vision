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
