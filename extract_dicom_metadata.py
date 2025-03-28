#import libraries
import os
import pydicom
import pandas as pd
import numpy as np

# Define the source directory containing the DICOM images and the output Excel file path.
source_dir = 'path/to/images'
excel_path = 'metadata_dicom.xlsx'

# Initialize a list to store metadata for each file.
data = []

# Iterate through each file in the source directory.
for filename in sorted(os.listdir(source_dir)):
    file_path = os.path.join(source_dir, filename)
    
    # Prepare a dictionary to hold metadata for this file.
    row = {'filename': filename, 'image_type': '', 'pixel_data': '', 'LUT': ''}
    
    # Process only DICOM files (ending with '.dcm'); ignore JPEG and others.
    if filename.lower().endswith('.dcm'):
        try:
            # Read the DICOM file with force=True to handle incomplete headers.
            ds = pydicom.dcmread(file_path, force=True, stop_before_pixels=False)

            # Extract 'ImageType' (tag 0008,0008) and join its list elements.
            image_type = getattr(ds, 'ImageType', [])
            row['image_type'] = '\\'.join(image_type) if image_type else ''
            
            # Summarize pixel data instead of storing the full array.
            if hasattr(ds, 'PixelData'):
                try:
                    # Read the pixel array and generate a summary: shape, data type, and mean intensity.
                    arr = ds.pixel_array
                    pixel_summary = f"{arr.shape}, {arr.dtype}, mean={np.mean(arr):.2f}"
                    row['pixel_data'] = pixel_summary
                except (AttributeError, ValueError, KeyError):
                    row['pixel_data'] = 'Unable to read pixel data'
            else:
                row['pixel_data'] = 'No pixel data'
            
            # Extract the 'VOILUTFunction' (tag 0028,1056) which indicates contrast adjustment.
            row['LUT'] = getattr(ds, 'VOILUTFunction', '')
        except Exception as e:
            # If any error occurs during DICOM reading, record the error message.
            row['image_type'] = f'Reading error: {e}'
            row['pixel_data'] = ''
            row['LUT'] = ''
    # For non-DICOM files (like JPEG), leave the metadata fields blank.
    data.append(row)

# Create a pandas DataFrame from the collected metadata.
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file using openpyxl.
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f"Excel file '{excel_path}' successfully created with {len(df)} records.")
