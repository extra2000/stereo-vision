# Changelog

## [1.1.0](https://github.com/extra2000/stereo-vision/compare/v1.0.0...v1.1.0) (2022-06-08)


### Features

* add point cloud ([fc598ef](https://github.com/extra2000/stereo-vision/commit/fc598efb6af8ae49bba714bc2ebc44d2dd07a926))
* **disparity:** add `--win-size` argument ([ec02c3d](https://github.com/extra2000/stereo-vision/commit/ec02c3d6d45bfe29ac676745c8ffa88abf8bd803))


### Performance Improvements

* downscale image before compute Stereo SGBM ([44f64d9](https://github.com/extra2000/stereo-vision/commit/44f64d9d6c304f8b4b616c4c42499864402c9950))


### Code Refactoring

* **disparity:** replace `num_disparities` with `max_disparity` and adjust default disparity range ([a006d85](https://github.com/extra2000/stereo-vision/commit/a006d85d0cf9e95f65b05e804d7c1785bb6bdf69))
* **imread:** read images as grayscale ([806dc5a](https://github.com/extra2000/stereo-vision/commit/806dc5a386c0c1658cc65cdd31699f61501bfc3d))

## 1.0.0 (2021-09-29)


### Features

* initial commit ([fbf3931](https://github.com/extra2000/stereo-vision/commit/fbf39317cf11387fda69aa5b5e6fdd39c297b42a))


### Documentations

* **README:** update `README.md` ([7d85fa3](https://github.com/extra2000/stereo-vision/commit/7d85fa31df4629205bcbf1bf26dccacb94a90cb0))


### Continuous Integrations

* add AppVeyor and `semantic-release` ([8788494](https://github.com/extra2000/stereo-vision/commit/878849466d7cec09391d6ba7e3cff662089952ee))
