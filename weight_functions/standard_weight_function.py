from utils.norms import norm_L2

class StandardWeightFunction(object):
    def __init__(self, z, epsilon):
        """
        C-tor
        :param z: z parameter of the weight function
        :param epsilon: epsilon parameter of standard weight function
        """
        self.z = z
        self.epsilon = epsilon

    def __call__(self, u, v):
        """
        Compute the standard weight function for two diferent coordinates, according to pdf.
        :param u: Hole's pixel
        :param v: Boundary pixel
        :return: scalar flaot, the weight of those 2 pixels.
        """
        ux, uy = u
        vx, vy = v
        return 1. / (norm_L2(uy-vy,ux-vx)**self.z + self.epsilon)