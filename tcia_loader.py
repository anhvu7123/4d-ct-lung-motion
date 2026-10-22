#!/usr/bin/env python3
"""
TCIA 4D-Lung DICOM Pipeline Connector
Author: Vu Minh Anh
Allows loading real anonymized 4D-CT patient data from The Cancer Imaging Archive (TCIA).
Sorts slices by AcquisitionTime / TriggerTime into 10 phase bins, extracts HU volumes,
and feeds directly into the centroid tracking & PTV coverage evaluation pipeline.
"""

import os
import glob
import pydicom
import numpy as np

def load_tcia_4dct_series(dicom_folder):
    """
    Load a folder containing 4D-CT DICOM slices and organize into (10, Z, Y, X) tensor in HU.
    """
    dcm_files = glob.glob(os.path.join(dicom_folder, "*.dcm"))
    if not dcm_files:
        raise FileNotFoundError(f"No DICOM files found in {dicom_folder}")

    print(f"Loading {len(dcm_files)} DICOM slices from TCIA folder...")
    slices = [pydicom.dcmread(f) for f in dcm_files]

    # Group by respiratory phase (DICOM tag 0020,0012 or Trigger Time / SeriesDescription)
    phases = {}
    for s in slices:
        phase_id = getattr(s, 'TemporalPositionIndex', None)
        if phase_id is None:
            # Fallback to TriggerTime or ContentTime
            phase_id = getattr(s, 'TriggerTime', 0)
        phases.setdefault(phase_id, []).append(s)

    print(f"Identified {len(phases)} respiratory phases.")
    sorted_phases = sorted(phases.keys())

    phase_volumes = []
    spacings = None

    for p_id in sorted_phases[:10]: # Keep up to 10 phases
        phase_slices = sorted(phases[p_id], key=lambda s: float(s.ImagePositionPatient[2]))
        
        # Voxel Spacing
        dz = abs(float(phase_slices[1].ImagePositionPatient[2]) - float(phase_slices[0].ImagePositionPatient[2])) if len(phase_slices) > 1 else 2.0
        dy, dx = float(phase_slices[0].PixelSpacing[0]), float(phase_slices[0].PixelSpacing[1])
        spacings = (dz, dy, dx)

        # Convert to Hounsfield Units (HU)
        vol = np.stack([s.pixel_array.astype(np.float32) * float(s.RescaleSlope) + float(s.RescaleIntercept) for s in phase_slices])
        phase_volumes.append(vol)

    volume_4d = np.stack(phase_volumes, axis=0) # (T, Z, Y, X)
    print(f"4D-CT Volume Loaded: shape={volume_4d.shape}, spacing (dz, dy, dx)={spacings} mm")
    return volume_4d, spacings

if __name__ == '__main__':
    print("TCIA 4D-Lung Loader module ready. Pass a DICOM folder path to load real patient data.")
