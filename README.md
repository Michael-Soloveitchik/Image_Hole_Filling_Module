# About:
#### This module written by Michael Soloveitchik for a home assginment in Lightricks ltd. company.
#### The module solve the "Hole Filling" task. Task's details and restrictions can be found in "Exercise_Hole_Filling.pdf" file., that attached to this module

# Test:
#### This module contains also test package. The test can be executed throw following command:

python ./tests test.py 

# Installations:
#### Install the following liblaries in the following order:
pip install numpy

pip install matplotlib

pip install opencv-python 

# Usage:
    usage: main.py [-h] [--input_path INPUT_PATH] [--mask_path MASK_PATH]
                   [--output_path OUTPUT_PATH] [--z Z] [--epsilon EPSILON]
                   [--is_8_connectivity] [--KNN]
    
    This library is a small image processing module for filling holes in images.
    Imlemented by Michael Soloveitchik. This module implement boundary based
    filling. Based on weigth function, see 'weight functions' package and the
    following parameters: z, epsilon, connectivity
    
    optional arguments:
      -h, --help            show this help message and exit
      --input_path INPUT_PATH
                            path to an input image
      --mask_path MASK_PATH
                            path to the mask image
      --output_path OUTPUT_PATH
                            path to the outpput image
      --z Z                 z parameter of the weight function
      --epsilon EPSILON     epsilon parameter of the weight function
      --is_8_connectivity   If passed than connectivity assigned to be 8,
                            othervise 4
      --KNN                 If passed than thealgorithm run in KNN (sub optimal)
                        mode

Improvment's suggestions and feedback might be addressed to me by
michael.soloveitchik@gmail.com
# Design
**Code design**

The code designed as following:
    
    'models' package - Algorithms migth be found here - I implemented one
    'utils' package - preprocessing and algebra formulas might be found there
    'weight_functions' package - weight functions that used into algorithms from 'models' package are found here
    'tests' package - input (images and masks files)

                      'test' script - Script for testing the module.
**Boundary detection:**

The boundary detection implemented in efficient way based on incolsure & exclosure algebra of maask with based on numpy.
# Answers
Answers can be found in "Answers.pdf" file