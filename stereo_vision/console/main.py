"""Entry-point for stereovision executable.
"""

import os
import sys
import logging
import logging.handlers
import argparse
from functools import partial

from stereo_vision import StereoVision, __version__

logger = logging.getLogger(__name__)


def main():
    try:
        _app()
    except KeyboardInterrupt as e:
        logger.exception('Received keyboard interrupt. Exiting.', exc_info=False)
    except Exception as e:
        logger.error('Exception type: {}'.format(type(e)))
        logger.error(str(e))
        logger.exception(str(e), exc_info=True)
        sys.exit(1)


def _app():
    args, parser = _parse_args()

    _init_logger()

    logger.info('Stereo Vision CLI version {}'.format(__version__))

    stereovision = StereoVision()

    command = {
        'generate-disparity-image': partial(_get_disparity_map, stereovision, args),
        'generate-point-cloud': partial(_get_point_cloud, stereovision, args),
    }

    choice = command.get(args.command, lambda: parser.print_help())
    choice()


def _get_disparity_map(stereovision, args):
    disparity_map = stereovision.get_disparity_map(
        args.leftimage,
        args.rightimage,
        min_disparity=vars(args)['min_disparity'],
        max_disparity=vars(args)['max_disparity'],
        win_size=vars(args)['win_size'],
        block_size=vars(args)['block_size'],
        disp12_max_diff=vars(args)['disp12_max_diff'],
        uniqueness_ratio=vars(args)['uniqueness_ratio'],
        speckle_window_size=vars(args)['speckle_window_size'],
        speckle_range=vars(args)['speckle_range'],
        sgbm_mode=vars(args)['sgbm_mode']
    )
    stereovision.write_disparity_map(args.outimage, disparity_map)


def _get_point_cloud(stereovision, args):
    disparity_map = stereovision.get_disparity_map(
        args.leftimage,
        args.rightimage,
        min_disparity=vars(args)['min_disparity'],
        max_disparity=vars(args)['max_disparity'],
        win_size=vars(args)['win_size'],
        block_size=vars(args)['block_size'],
        disp12_max_diff=vars(args)['disp12_max_diff'],
        uniqueness_ratio=vars(args)['uniqueness_ratio'],
        speckle_window_size=vars(args)['speckle_window_size'],
        speckle_range=vars(args)['speckle_range'],
        sgbm_mode=vars(args)['sgbm_mode']
    )
    points, colors = stereovision.get_point_cloud(args.leftimage, disparity_map)
    stereovision.write_point_cloud(vars(args)['plyfile'], points, colors)


def _init_logger():
    formatter = logging.Formatter('%(asctime)s %(process)d:%(thread)d:%(levelname)s:%(name)s:%(lineno)d: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel('INFO')

    rootlogger = logging.getLogger('stereo_vision')
    rootlogger.addHandler(stream_handler)
    rootlogger.setLevel('DEBUG')


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Stereo Vision CLI version {}.'.format(__version__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparser = parser.add_subparsers(help='CLI command', dest='command')

    get_disp_img = subparser.add_parser('generate-disparity-image', help='Combine stereo image into a single image which represents disparity map')
    get_disp_img.add_argument('--min-disparity', type=int, help='Minimum disparity. Default is %(default)d', default=-16)
    get_disp_img.add_argument('--max-disparity', type=int, help='Maximum disparity. Default is %(default)d', default=16)
    get_disp_img.add_argument('--win-size', type=int, help='Window size. Default is %(default)d', default=2)
    get_disp_img.add_argument('--block-size', type=int, help='Block size. Default is %(default)d', default=1)
    get_disp_img.add_argument('--disp12-max-diff', type=int, help='Maximum allowed difference. Default is %(default)d', default=-1)
    get_disp_img.add_argument('--uniqueness-ratio', type=int, help='Uniqueness ratio. Default is %(default)d', default=15)
    get_disp_img.add_argument('--speckle-window-size', type=int, help='Speckle window size. Default is %(default)d', default=200)
    get_disp_img.add_argument('--speckle-range', type=int, help='Speckle range. Default is %(default)d', default=64)
    get_disp_img.add_argument('--sgbm-mode', type=str, help='SGBM mode. Default is %(default)s', choices=['hh', '3way', 'sgbm'], default='3way')
    get_disp_img.add_argument('leftimage', type=str, help='Left image')
    get_disp_img.add_argument('rightimage', type=str, help='Right image')
    get_disp_img.add_argument('outimage', type=str, help='Output image')

    get_pntcloud_img = subparser.add_parser('generate-point-cloud', help='Compute disparity map and generate point cloud')
    get_pntcloud_img.add_argument('--min-disparity', type=int, help='Minimum disparity. Default is %(default)d', default=-16)
    get_pntcloud_img.add_argument('--max-disparity', type=int, help='Maximum disparity. Default is %(default)d', default=16)
    get_pntcloud_img.add_argument('--win-size', type=int, help='Window size. Default is %(default)d', default=2)
    get_pntcloud_img.add_argument('--block-size', type=int, help='Block size. Default is %(default)d', default=1)
    get_pntcloud_img.add_argument('--disp12-max-diff', type=int, help='Maximum allowed difference. Default is %(default)d', default=-1)
    get_pntcloud_img.add_argument('--uniqueness-ratio', type=int, help='Uniqueness ratio. Default is %(default)d', default=15)
    get_pntcloud_img.add_argument('--speckle-window-size', type=int, help='Speckle window size. Default is %(default)d', default=200)
    get_pntcloud_img.add_argument('--speckle-range', type=int, help='Speckle range. Default is %(default)d', default=64)
    get_pntcloud_img.add_argument('--sgbm-mode', type=str, help='SGBM mode. Default is %(default)s', choices=['hh', '3way', 'sgbm'], default='3way')
    get_pntcloud_img.add_argument('leftimage', type=str, help='Left image')
    get_pntcloud_img.add_argument('rightimage', type=str, help='Right image')
    get_pntcloud_img.add_argument('plyfile', type=str, help='Output PLY file')

    args = parser.parse_args()

    return args, parser
