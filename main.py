import napari
import numpy as np
import skimage as sk
from ext_io import choose_tiff_file

file_path = choose_tiff_file()

vol = sk.io.imread(file_path, plugin='tifffile')

# Start the viewer
viewer = napari.Viewer()

image_layer = viewer.add_image(vol)

# # Add an empty 3D Points layer (you can also load from existing data)
# points_layer = viewer.add_points(
#     data=np.empty((0, 3)),  # 3D points
#     ndim=3,
#     size=5,
#     face_color='red',
#     name='3D Points'
# )

# # Function to extract the points from the viewer


# def extract_points():
#     points_array = points_layer.data  # This is a NumPy array of shape (N, 3)
#     print("Extracted Points:\n", points_array)
#     return points_array

# # Optional: Bind extraction to a key (e.g. press 'e' to extract)


# @viewer.bind_key('e')
# def on_key_e(viewer):
#     extract_points()


napari.run()
