# read binary data
import numpy as np

def read_file(filename):
    with open(filename, 'rb') as file:
        # Read the header
        header = file.read(0x1ca)
        # Read the data
        data = file.read()
        # Convert the data to a numpy array
        data = np.frombuffer(data, dtype=np.int16)
        return data

import matplotlib.pyplot as plt

data = read_file('TEK0000RF1.isf')

adata = data[530000:1790000]



# Set values greater than 75 to zero
adata_c = adata.copy()
adata_c[adata_c > 75] = 0
# Define a simple moving average function
def moving_average(data, window_size=3):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Smooth the data
smoothed_data = moving_average(adata_c, window_size=3)

plt.plot(smoothed_data, label='Signal')
plt.legend()
plt.grid(True)
plt.show()