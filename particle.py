import numpy as np
import skimage as sk
import scipy.ndimage as ndi
import h5py

# from dataclasses import dataclass

# @dataclass
class Particle:

    def __init__(self, image_name: str,
                image: np.ndarray,
                position:tuple ,
                bbox_size:int = 60,):
                # file:str = 'points', 
                # name:str = 'ppt'):
        
        self.image_name = image_name
        self.image = image
        self.init_position = position
        self.centroid = None
        self.bbox_size = bbox_size
        self.pz, self.py, self.px = self.init_position

        bb = self.bbox_size//2

        self.pimage = self.image[int(self.pz)-bb:int(self.pz)+bb, 
                                 int(self.py)-bb:int(self.py)+bb, 
                                 int(self.px)-bb:int(self.px)+bb]
        
        self.refine_centroid()


    def refine_centroid(self):

        mask = self.pimage < sk.filters.threshold_otsu(self.pimage)

        labels, _ = ndi.label(mask)

        props = sk.measure.regionprops(labels)

        dpz, dpy, dpx = props[0].centroid

        self.centroid = (int(self.pz) + dpz, 
                         int(self.py) + dpy,
                         int(self.px) + dpx)

        return self.centroid
    
    def __repr__(self):
        txt = f'Particle centered at {self.centroid}'
        return txt
    
    # def save_particle(self):

    #     with h5py.File()

        
        

    
