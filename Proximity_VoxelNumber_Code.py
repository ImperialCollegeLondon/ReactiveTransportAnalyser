# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Sajjad Foroughi
"""
Voxel face-count and dissolution analysis utilities.

Author: Dr. Sajjad Foroughi (Imperial College London)
Contact: <optional email>
Repository: https://github.com/ImperialCollegeLondon/ReactiveTransportAnalyser
License: MIT

If you use this code, please cite:
Adedipe, O. A., Al-Khulaifi, Y., Foroughi, S., Lin, Q., Blunt, M. J., & Bijeljic, B. (2025).
Impact of Mineral Spatial Distribution on CO₂ Dissolution Rates in Multimineral Carbonate Rocks.
ESS Open Archive. https://doi.org/10.22541/essoar.176169610.00294276/v1
"""

import pandas as pd
import numpy as np
from skimage.io import imread
from scipy.ndimage import distance_transform_edt
import os

# Define file paths for input images
image_files = [f"image{i}.tif" for i in range(1, 11)]
fastflow_files = [f"fastflowdistmap{i}.tif" for i in range(1, 11)]
slowregion_files = [f"slowregionsdistmap{i}.tif" for i in range(1, 11)]

# Define parameters
pore_label = 2  # Set pore label (modify as needed)
outLayer = 1    # Set outlayer label (modify as needed)

# Load base images
base_images = [imread(path) for path in image_files]
image1 = base_images[0]
image2 = base_images[1]

# Find unique values in image1 and define labels of interest
unique_values1, _ = np.unique(image1, return_counts=True)
labels_of_interest = set(unique_values1)

# Define a function to process and save Excel files with combined sheets
def process_images_combined(input_files, output_prefix, image1, image2):
    for idx, file_path in enumerate(input_files, start=1):
        # Define output file name
        output_file = f"{output_prefix}_{idx}.xlsx"

        # Skip processing if the output file already exists
        if os.path.exists(output_file):
            print(f"{output_file} already exists. Skipping...")
            continue

        print(f"Processing {file_path}...")  # Debugging message

        try:
            # Load binary image and compute the distance map
            binary_image = imread(file_path)
            binary_image = 1 * (binary_image > 0)
            distance_map = distance_transform_edt(1 - binary_image)

            # Create a dictionary to store data for all labels
            combined_results = {}

            # Iterate through labels of interest
            for desired_label in labels_of_interest:
                if pore_label == desired_label or desired_label == outLayer:
                    continue

                # Identify dissolved voxels based on image2 and image1
                logical_dissolved = (image2 == pore_label) & (image1 == desired_label)
                desired_distance = distance_map * logical_dissolved

                # Extract non-zero distances
                nonzero_distances = desired_distance.flatten()
                nonzeros_distance = nonzero_distances[nonzero_distances > 0]

                # Find unique values and their counts in non-zero distances
                arr_rounded = np.round(nonzeros_distance, decimals=0)
                unique_values, counts = np.unique(arr_rounded, return_counts=True)

                # Store the results in a DataFrame for each label
                result_df = pd.DataFrame({
                    'Unique Value': unique_values,
                    f'Count_Label_{desired_label}': counts
                })

                # Add the DataFrame to the combined results dictionary
                combined_results[desired_label] = result_df

            # Merge all DataFrames side by side
            combined_df = combined_results.pop(list(combined_results.keys())[0])
            for key, df in combined_results.items():
                combined_df = pd.merge(combined_df, df, on='Unique Value', how='outer')

            # Fill NaN values with 0 (optional)
            combined_df = combined_df.fillna(0)

            # Write the combined DataFrame to a single sheet in the Excel file
            combined_df.to_excel(output_file, sheet_name="Combined", index=False)

            print(f"Results saved to {output_file}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# Process fast flow files
process_images_combined(fastflow_files, "VoxelNumber_fast_channel", image1, image2)

# Process slow regions files
process_images_combined(slowregion_files, "VoxelNumber_slow_regions", image1, image2)

