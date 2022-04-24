# This is a sample Python script.
import argparse
from utils.preprocessing import mask_2_hole
from models.holes_filling_module import HolesFilling
import cv2
# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''This library is a small image processing module for filling holes in images.
           Imlemented by Michael Soloveitchik.
           This module implement boundary based filling. Based on weigth function, see 'weight functions' package and the following parameters: z, epsilon, connectivity
           ''',
        epilog="""Improvment's suggestions and feedback might be addressed to me by michael.soloveitchik@gmail.com""")
    parser.add_argument('--input_path', type=str, help='path to an input image')
    parser.add_argument('--mask_path', type=str, help='path to the mask image')
    parser.add_argument('--output_path', type=str, help='path to the outpput image')
    parser.add_argument('--z', type=float, help='z parameter of the weight function')
    parser.add_argument('--epsilon', type=float, help='epsilon parameter of the weight function')
    parser.add_argument('--is_8_connectivity', action='store_true', help='If passed than connectivity assigned to be 8, othervise 4')
    args = parser.parse_args()

    # reading and preprocessing input with hole
    input = cv2.imread(args.input_path)
    mask_hole = cv2.imread(args.mask_path)

    # merge the mask and input iamge into image with hole
    input_with_hole = mask_2_hole(input, mask_hole)

    # Initialziation of the module with input parameters
    module = HolesFilling(z=args.z, epsilon=args.epsilon, is_8_connectivity=args.is_8_connectivity)
    output = module.fill_holes(input_with_hole)

    color_output = cv2.imwrite(args.output_path, (output*255.).astype('uint8'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# if __name__ == '__main__':
#     '''
#     python ./main.py --input_path ./tests/input/input_83.jpg --mask_path .//tests/input/mask_83.jpg --output_path ./tests/output_test/output_83.jpg --z 2.5 --epsilon 0.00044281924004845117 --is_8_connectivity
#
#     '''