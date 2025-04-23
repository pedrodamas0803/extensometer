import os, sys
import napari
import argparse
import numpy as np
import skimage as sk
import h5py
from ext_io import choose_tiff_files
from particle import Particle


def main(out_file, bbox_size = 60, plot = False):

    file_paths = choose_tiff_files()

    if len(file_paths) < 2:
        print('At least 2 images are needed for strain calculations. Exiting...')
        sys.exit(1)

    all_samples = []

    for file_path in file_paths:

        vol = sk.io.imread(file_path, plugin='tifffile')

        # Start the viewer
        viewer = napari.Viewer()

        image_layer = viewer.add_image(vol)

        # Add an empty 3D Points layer (you can also load from existing data)
        points_layer = viewer.add_points(
            data=np.empty((0, 3)),  # 3D points
            ndim=3,
            size=5,
            face_color='lime',
            name='Picked Points'
        )

        
        # Function to extract the points from the viewer
        def extract_points():
            points = points_layer.data  # This is a NumPy array of shape (N, 3)
            p1 = Particle(file_path, image=vol, position=points[0], bbox_size=bbox_size)
            p2 = Particle(file_path, image=vol, position=points[1], bbox_size=bbox_size)
            all_samples.append([p1, p2])
            # for ii, point in enumerate(points_array):
            #     # print("Extracted Point:\n", point)
            #     p1 = Particle(file_path, image=vol, position=point, file='points.h5')
            #     all_samples.append(p)
            #     # print(p)
            # viewer.close()
            # return points
        


        # Optional: Bind extraction to a key (e.g. press 'e' to extract)
        @viewer.bind_key('e')
        def on_key_e(viewer):
            extract_points()
            # print(points)
            viewer.close()

        napari.run()

    image_names = []
    z_coord_p1 = np.zeros(len(all_samples))
    z_coord_p2 = np.zeros(len(all_samples))

    for ii, [p1, p2] in enumerate(all_samples):

        image_names.append(p1.image_name)
        z_coord_p1[ii] = p1.centroid[0]
        z_coord_p2[ii] = p2.centroid[0]

    dz = z_coord_p2 - z_coord_p1

    strains = (dz - dz[0])/dz[0]

    with h5py.File(out_file, 'w') as hout:

        hout['images'] = image_names
        hout['p1z'] = z_coord_p1
        hout['p2z'] = z_coord_p2
        hout['dz'] = dz
        hout['eps'] = strains

    # print(strains)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out_file', type=str)
    parser.add_argument('-bb', '--bbox_size', type=int)

    args = parser.parse_args()
    # print(args.bbox_size, args.out_file )
    main(out_file=args.out_file, bbox_size=args.bbox_size, plot=False)



    
