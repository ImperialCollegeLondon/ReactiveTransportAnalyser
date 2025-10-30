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

import numpy as np
import pandas as pd
from skimage.io import imread
from scipy.ndimage import binary_dilation

# Define constants
number_of_images = 10
numberofVoxelDilation = 1  # Dilation size
poreLabel = 2
outLayer = 1

# Function to calculate face counts for an image
def calculate_face_counts(image, labels_of_interest, poreLabel, outLayer):
    face_counts = {label: 0 for label in labels_of_interest}
    for label in labels_of_interest:
        if (poreLabel == label) or (label == outLayer):
            continue
        for x in range(2, label):
            temp1 = np.sum((image[1:, :, :] == x) & (image[:-1, :, :] == label))
            temp2 = np.sum((image[:-1, :, :] == x) & (image[1:, :, :] == label))
            temp3 = np.sum((image[:, 1:, :] == x) & (image[:, :-1, :] == label))
            temp4 = np.sum((image[:, :-1, :] == x) & (image[:, 1:, :] == label))
            temp5 = np.sum((image[:, :, 1:] == x) & (image[:, :, :-1] == label))
            temp6 = np.sum((image[:, :, :-1] == x) & (image[:, :, 1:] == label))
            face_counts[label] += temp1 + temp2 + temp3 + temp4 + temp5 + temp6
    return face_counts

# Create an Excel writer to save results
output_file = "VoxelNumber_and_FacesToPore.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for i in range(1, number_of_images):
        # Load consecutive images
        image_path1 = f"image{i}.tif"
        image_path2 = f"image{i+1}.tif"
        image1 = imread(image_path1)
        image2 = imread(image_path2)

        # Analyze first image
        unique_values1, counts1 = np.unique(image1, return_counts=True)
        numberofVoxels1 = counts1

        # Analyze second image
        unique_values2, counts2 = np.unique(image2, return_counts=True)
        numberofVoxels2 = counts2

        # Labels of interest
        labels_of_interest = set(unique_values1)

        # Perform dilation on the first image
        binary_mask1 = (image1 == poreLabel)
        structuring_element = np.ones((numberofVoxelDilation, numberofVoxelDilation, numberofVoxelDilation), dtype=bool)
        dilated_mask1 = binary_dilation(binary_mask1, structure=structuring_element)
        dilated_image1 = image1.copy()
        dilated_image1[dilated_mask1] = poreLabel

        # Perform dilation on the second image
        binary_mask2 = (image2 == poreLabel)
        dilated_mask2 = binary_dilation(binary_mask2, structure=structuring_element)
        dilated_image2 = image2.copy()
        dilated_image2[dilated_mask2] = poreLabel

        # Calculate face counts
        face_counts1 = calculate_face_counts(dilated_image1, labels_of_interest, poreLabel, outLayer)
        face_counts2 = calculate_face_counts(dilated_image2, labels_of_interest, poreLabel, outLayer)

        # Calculate dissolved voxels
        dissolved_voxels = numberofVoxels1 - numberofVoxels2

        # Create a DataFrame with results
        combined_data = pd.DataFrame({
            "Phase (Image A)": unique_values1,
            "Voxel Count (Image A)": numberofVoxels1,
            "Phase (Image B)": unique_values2,
            "Voxel Count (Image B)": numberofVoxels2,
            "Face Count (Image A)": [face_counts1.get(phase, 0) for phase in unique_values1],
            "Face Count (Image B)": [face_counts2.get(phase, 0) for phase in unique_values2],
            "Dissolved Voxels": dissolved_voxels
        })

        # Save the data to a separate sheet
        sheet_name = f"Image{i}_Image{i+1}"
        combined_data.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Results saved to {output_file}")
