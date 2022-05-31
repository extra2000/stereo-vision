import os
import logging

import numpy as np
import cv2

logger = logging.getLogger(__name__)


class StereoVision:
    """Stereo Vision
    """

    def __init__(self):
        """Implement Stereo Vision
        """
        self.cfg = None


    @staticmethod
    def get_disparity_map(leftimage, rightimage, **kwargs):
        """
        Combine stereo image into a single image which represents disparity map.

        Parameters
        ----------
        leftimage : str
            Left image filename.
        rightimage : str
            Right image filename.
        min_disparity : int
            Minimum disparity. Default is -16.
        max_disparity : int
            Number of disparities. Default is 16.
        win_size : int
            Window size. Default is 2.
        block_size : int
            Block size. Default is 1.
        disp12_max_diff : int
            Maximum allowed difference. Default is -1.
        uniqueness_ratio : int
            Uniqueness ratio. Default is 15.
        speckle_window_size : int
            Speckle window size. Default is 200.
        speckle_range : int
            Speckle range. Default is 64.
        sgbm_mode : str
            SGBM mode. Available choices are 'hh', '3way', or 'sgbm'. Default is '3way'.

        Returns
        -------
        cv2.image
            Disparity map with the same dimension as input image.
        """

        img_left = cv2.pyrDown(cv2.imread(leftimage, cv2.IMREAD_GRAYSCALE))
        img_right = cv2.pyrDown(cv2.imread(rightimage, cv2.IMREAD_GRAYSCALE))

        # Setting parameters for StereoSGBM algorithm
        min_disparity = kwargs.get('min_disparity', -16)
        max_disparity = kwargs.get('max_disparity', 16)
        win_size = kwargs.get('win_size', 2)
        block_size = kwargs.get('block_size', 1)
        disp12_max_diff = kwargs.get('disp12_max_diff', -1)
        uniqueness_ratio = kwargs.get('uniqueness_ratio', 15)
        speckle_window_size = kwargs.get('speckle_window_size', 200)
        speckle_range = kwargs.get('speckle_range', 64)

        param_sgbm_mode = kwargs.get('sgbm_mode', '3way')

        if param_sgbm_mode == 'hh':
            sgbm_mode = cv2.STEREO_SGBM_MODE_HH
        elif param_sgbm_mode == '3way':
            sgbm_mode = cv2.STEREO_SGBM_MODE_SGBM_3WAY
        elif param_sgbm_mode == 'sgbm':
            sgbm_mode = cv2.STEREO_SGBM_MODE_SGBM
        else:
            raise ValueError(param_sgbm_mode)

        num_disparities = max_disparity - min_disparity

        # Creating an object of StereoSGBM algorithm
        stereo = cv2.StereoSGBM_create(
            minDisparity=min_disparity,
            numDisparities=num_disparities,
            blockSize=block_size,
            disp12MaxDiff=disp12_max_diff,
            uniquenessRatio=uniqueness_ratio,
            speckleWindowSize=speckle_window_size,
            speckleRange=speckle_range,
            P1=8*3*win_size**2,
            P2=32*3*win_size**2,
            mode=sgbm_mode
        )

        # Calculating disparity using the StereoSGBM algorithm
        disparity_map = stereo.compute(img_left, img_right).astype(np.float32)

        return cv2.pyrUp(disparity_map)


    @staticmethod
    def get_point_cloud(leftimage, disparity_map, **kwargs):
        """
        Generate point cloud based on disparity map

        Parameters
        ----------
        leftimage : str
            Left image filename.
        disparity_map : cv2.image
            Disparity map

        Returns
        -------
        np.array
            Point cloud data.
        np.array
            Colors for the point cloud.
        """

        colors = cv2.imread(leftimage, cv2.COLOR_BGR2RGB)

        h, w = disparity_map.shape[:2]
        f = (50 * 1000) / 16.7
        Q = np.float32([
            [1,  0, 0, -0.5*w],
            [0, -1, 0,  0.5*h],
            [0,  0, 0, -f],
            [0,  0, 1,  0]
        ])
        points = cv2.reprojectImageTo3D(disparity_map, Q)
        mask = disparity_map > disparity_map.min()
        out_points = points[mask]
        out_colors = colors[mask]

        return out_points, out_colors


    @staticmethod
    def write_disparity_map(filename, outimage):
        """Write disparity map to image file

        Parameters
        ----------
        filename : str
            Filename to write output image.
        outimage : cv2.image
            Output image.
        """

        normimg = np.abs(cv2.normalize(outimage, 0, 255, cv2.NORM_MINMAX)*255).astype(np.uint8)
        cv2.imwrite(filename, normimg)


    @staticmethod
    def write_point_cloud(plyfile, points, colors):
        """Write point clouds to PLY file

        Parameters
        ----------
        plyfile : str
            PLY filename
        points : np.array
            Points.
        colors : np.array
            Colors for the points.
        """

        verts = points.reshape(-1, 3)
        colors = colors.reshape(-1, 3)
        verts = np.hstack([verts, colors])
        with open(plyfile, 'wb') as f:
            # write PLY header
            f.write(('ply\n').encode('utf-8'))
            f.write(('format ascii 1.0\n').encode('utf-8'))
            f.write(('element vertex {}\n'.format(len(verts))).encode('utf-8'))
            f.write(('property float x\n').encode('utf-8'))
            f.write(('property float y\n').encode('utf-8'))
            f.write(('property float z\n').encode('utf-8'))
            f.write(('property uchar red\n').encode('utf-8'))
            f.write(('property uchar green\n').encode('utf-8'))
            f.write(('property uchar blue\n').encode('utf-8'))
            f.write(('end_header\n').encode('utf-8'))
            # write point clouds including colors
            np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')
