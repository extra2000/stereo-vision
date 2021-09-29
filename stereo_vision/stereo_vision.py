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
            Minimum disparity. Default is 0.
        num_disparities : int
            Number of disparities. Default is 300.
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

        img_left = cv2.imread(leftimage, 0)
        img_right = cv2.imread(rightimage, 0)

        # Setting parameters for StereoSGBM algorithm
        min_disparity = kwargs.get('min_disparity', 0)
        num_disparities = kwargs.get('num_disparities', 300)
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

        # Creating an object of StereoSGBM algorithm
        stereo = cv2.StereoSGBM_create(
            minDisparity=min_disparity,
            numDisparities=num_disparities,
            blockSize=block_size,
            disp12MaxDiff=disp12_max_diff,
            uniquenessRatio=uniqueness_ratio,
            speckleWindowSize=speckle_window_size,
            speckleRange=speckle_range,
            mode=sgbm_mode
        )

        # Calculating disparity using the StereoSGBM algorithm
        disparity_map = stereo.compute(img_left, img_right).astype(np.float32)

        return disparity_map


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
