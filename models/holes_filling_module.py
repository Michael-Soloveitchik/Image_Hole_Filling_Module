import numpy as np
import matplotlib
from weight_functions.standard_weight_function import StandardWeightFunction
matplotlib.use("TkAgg")
HOLE = -1.
import matplotlib.pyplot as plt
class HolesFilling(object):
    def __init__(self, z, epsilon, is_8_connectivity):
        """
        C-tor
        :param z: the power [arameter
        :param epsilon:  The smoothing parameter of dinaminator
        :param is_8_connectivity:  Weather we search for 4 connectivity or 8 conneectivity
        """
        self.weight_function = StandardWeightFunction(z, epsilon)
        self.is_8_connectivity = is_8_connectivity
        self.bounds_mask = None
        self.hole_mask = None

    def find_hole_n_bounds(self, input_with_hole):
        """
        This function assign the connectivity mask, according to connectivity param.
        4 connectivity or 8 connectivity.
        All this done by enlosure & exclosure algebra of boolean masks

        :param temp_input_with_hole: [H,W] grayscale image in range [0,1] | {-1}, When -1. denotes hole pixels
        :rtype: Boolean mask of the hole & boolean mask of bound
        """
        # inverse mask of the hole
        input_mask = (input_with_hole==HOLE)
        self.hole_mask = input_mask
        not_hole_mask = ~input_mask
        temp_input_with_hole = input_with_hole + 0.
        temp_input_with_hole[not_hole_mask] = 1.
        # temp_input_with_hole = (temp_input_with_hole).reshape(input_with_hole.shape)

        # Closure of upper pxiels and the hole
        up_bound_closure = (temp_input_with_hole+np.roll(temp_input_with_hole, shift=-1, axis=0))==0.
        up_bound = not_hole_mask & up_bound_closure # subtraction (adding of inverse) with the hole to get the bound

        # Closure of down pxiels and the hole
        down_bound_closure = (temp_input_with_hole+np.roll(temp_input_with_hole, shift=1, axis=0))==0.
        down_bound = not_hole_mask & down_bound_closure # subtraction (adding of inverse) with the hole to get the bound
        up_down_bound = up_bound | down_bound # union to get both upper and lower bound pixels

        # Closure of left pxiels and the hole
        left_bound_closure = (temp_input_with_hole + np.roll(temp_input_with_hole, shift=1, axis=1)) == 0.
        left_bound = not_hole_mask & left_bound_closure # subtraction (adding of inverse) with the hole to get the bound

        # Closure of right pxiels and the hole
        right_bound_closure = (temp_input_with_hole + np.roll(temp_input_with_hole, shift=-1, axis=1)) == 0.
        right_bound = not_hole_mask & right_bound_closure # subtraction (adding of inverse) with the hole to get the bound
        left_right_bound = left_bound | right_bound # union to get both left and right bound pixels

        # union of upper-down and right-left bound pixels -> 4 connectivity bound mask
        connectivity_4 = up_down_bound | left_right_bound
        if self.is_8_connectivity:
            # Closure of upper-right pixels and the hole
            up_right_bound_closure = (temp_input_with_hole + np.roll(np.roll(temp_input_with_hole, shift=1, axis=0), shift=1, axis=1)) == 0.
            up_right_bound = not_hole_mask & up_right_bound_closure # subtraction (adding of inverse) with the hole to get the bound

            # Closure of upper-left pixels and the hole
            up_left_bound_closure = (temp_input_with_hole + np.roll(np.roll(temp_input_with_hole, shift=1, axis=0), shift=-1, axis=1)) == 0.
            up_left_bound = not_hole_mask & up_left_bound_closure # subtraction (adding of inverse) with the hole to get the bound
            up_right_left_bound = up_right_bound | up_left_bound # union to get both up-left and up-right bound pixels

            # Closure of down-right pixels and the hole
            down_right_bound_closure = (temp_input_with_hole + np.roll(np.roll(temp_input_with_hole, shift=-1, axis=0), shift=1, axis=1)) == 0.
            down_right_bound = not_hole_mask & down_right_bound_closure # subtraction (adding of inverse) with the hole to get the bound

            # Closure of down-left pixels and the hole
            down_left_bound_closure = (temp_input_with_hole + np.roll(np.roll(temp_input_with_hole, shift=-1, axis=0), shift=-1, axis=1)) == 0.
            down_left_bound = not_hole_mask & down_left_bound_closure # subtraction (adding of inverse) with the hole to get the bound
            down_right_left_bound = down_right_bound | down_left_bound # union to get both down-left and down-right bound pixels

            # union of upper-right-left and down-right-left bound pixels -> 4 diagonal connectivity bound mask
            connectivity_4_diagonal = up_right_left_bound | down_right_left_bound
            # union 4 connectivity and 4 diagonal connectivity -> 8 connectivity bound mask
            self.bounds_mask = connectivity_4_diagonal | connectivity_4
        else:
            self.bounds_mask = connectivity_4


    def fill_holes(self, input_with_hole):
        """
        THis function ia implemntation of an algorithm of filling holes. This Algorithm described in details in the pdf file.
        :param input_with_hole:  A grayscale image [H,W] in range [0,1] U {-1}, Wehn {-1} is the hole's pixels value
        :return: A grayscale image [H,W] in range [0,1], without a hole.
        """
        # A.
        # First tep According to algorithm first find the coordinates of the boundary pixels and hole's pixels.
        self.find_hole_n_bounds(input_with_hole)  # find the connections according to connectivity parameter

        # B.
        # Find the intensities of the boundary pixels
        boundary_intensities = input_with_hole[self.bounds_mask].flatten().tolist() # iniitaliztion weights array

        # C.
        # Preparing to iterate over pixels in hole
        output = input_with_hole + 0.
        y_x_hole_indeces = np.argwhere(self.hole_mask).tolist()  # hole's pixels coordinates
        y_x_bounds_indeces = np.argwhere(self.bounds_mask).tolist() # bounds's pixels coordinates
        # For each pixel in hole:
        # C.1. compute the weigths of this pixel from boundaries
        # C.2 compute the dot product of weights with boundaries intensions
        # C.3. normalize the former result by the sum of weights.
        # C.4. Assign the normalized result to be new intensity
        for i, (uy, ux) in enumerate(y_x_hole_indeces):
            # C.1 build weights array
            weights = np.array([self.weight_function((ux,uy), (vx,vy)) for vy,vx in y_x_bounds_indeces])

            # C.2.  compute the new value of the hole's pixel
            nominator = np.dot(boundary_intensities, weights)
            descriminator = np.dot(np.ones(weights.shape), weights)
            # C.3. Normalization
            new_intensity =  nominator / descriminator # new value in the hole
            # C.4. Assign new intensity
            output[uy, ux] = new_intensity # assignment
        return output

    def fill_holes_aproximation(self, input_with_hole):
        """
        THis function ia implemntation of an aproximation algorithm of filling holes. This Algorithm described in my answer to question 2 and detailed in the pdf file.
        :param input_with_hole:  A grayscale image [H,W] in range [0,1] U {-1}, Wehn {-1} is the hole's pixels value
        :return: A grayscale image [H,W] in range [0,1], without a hole.
        """
        # A.
        # First tep According to algorithm first find the coordinates of the boundary pixels and hole's pixels.
        self.find_hole_n_bounds(input_with_hole)  # find the connections according to connectivity parameter

        # B.
        # Find the intensities of the boundary pixels
        boundary_intensities = input_with_hole[self.bounds_mask].flatten().tolist() # iniitaliztion weights array

        # C. partion into connected froups
        # C.
        # Preparing to iterate over pixels in hole
        output = input_with_hole + 0.
        y_x_hole_indeces = np.argwhere(self.hole_mask).tolist()  # hole's pixels coordinates
        y_x_bounds_indeces = np.argwhere(self.bounds_mask).tolist() # bounds's pixels coordinates
        # For each pixel in hole:
        # C.1. compute the weigths of this pixel from boundaries
        # C.2 compute the dot product of weights with boundaries intensions
        # C.3. normalize the former result by the sum of weights.
        # C.4. Assign the normalized result to be new intensity
        for i, (uy, ux) in enumerate(y_x_hole_indeces):
            # C.1 build weights array
            weights = np.array([self.weight_function((ux,uy), (vx,vy)) for vy,vx in y_x_bounds_indeces])

            # C.2.  compute the new value of the hole's pixel
            nominator = np.dot(boundary_intensities, weights)
            descriminator = np.dot(np.ones(weights.shape), weights)
            # C.3. Normalization
            new_intensity =  nominator / descriminator # new value in the hole
            # C.4. Assign new intensity
            output[uy, ux] = new_intensity # assignment
        return output