import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

# Define the file paths
ux_file = "Ufx.raw"
uy_file = "Ufy.raw"
uz_file = "Ufz.raw"

# Define the dimensions of the data
height, width, depth = 875, 857, 875

#height is the z direction
#width is the y direction
#depth is the x direction

# Define the data type (float32 for real values, adjust if necessary)
data_type = np.float32

# Function to read raw files
def read_raw_file(file_path, dtype, shape):
    data = np.fromfile(file_path, dtype=dtype)
    if data.size != np.prod(shape):
        raise ValueError("Data size {} does not match expected dimensions {}.".format(data.size, shape))
    return data.reshape(shape)

# Read the data from the files

ux = read_raw_file(ux_file, data_type, (height, width, depth+1))
uy = read_raw_file(uy_file, data_type, (height, width+1, depth))
uz = read_raw_file(uz_file, data_type, (height+1, width, depth))
Ux = (ux[:,:,:-1]+ux[:,:,1:])/2
Uy = (uy[:,:-1,:]+uy[:,1:,:])/2
Uz = (uz[:-1,:,:]+uz[:1,:,:])/2
# Compute the magnitude of velocity
V = np.sqrt(Ux**2 + Uy**2 + Uz**2)

# Save the result as a TIFF file
io.imsave('flowfield.tif', V.astype(np.float32))

# Optionally, visualize a slice of the data
slice_index = depth // 2

plt.figure(figsize=(10, 5))

plt.subplot(1, 3, 1)
plt.imshow(ux[:, :, slice_index], cmap='gray')
plt.title('Ux Slice')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(uy[:, :, slice_index], cmap='gray')
plt.title('Uy Slice')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(V[:, :, slice_index], cmap='gray')
plt.title('Velocity Magnitude Slice')
plt.axis('off')

plt.show()
