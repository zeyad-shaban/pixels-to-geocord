# Camera Calibration Tool

This tool performs camera calibration using chessboard images to compute intrinsic camera parameters.

### Image Processing Settings

```python
IMAGE_PATH = "./data/hidden_keyboard/*.JPG"  # Path pattern for input chessboard images
OUT_DEBUG_PATH = './data/out_images/'        # Path for debug output images
board_size = (4, 4)                          # Number of corners in chessboard (4x4 means 5x5 squares)
square_size = 3.5e-2                          # Size of chessboard squares in meters
ratio = 1 / 8                                # Image downsample ratio (1/8)
```

### Debug Output

The tool generates debug output images in `OUT_DEBUG_PATH` that show:

- Resized images with detected corners
- Chessboard pattern overlay
- Corner refinement results

These images should be manually reviewed to verify that corners are being correctly detected and exactly match the acutal corners.
if any missalignment occured delete any image that caused this and rerun (it will have the same name as the original one)

## Usage
!! ENSURE YOU RUN THIS USING THE LATEST OPENCV VERSION WHICH IS INCOMPATAIBLE WITH TEH NUMPY VERSION REQUIRED
MEANING THIS SCRIPT NEEDS TO RUN WITH A DIFFERENT PYTHON ENVIRONMENT THAN THE ONE FOR PIXEL TO LAT LON EXTRACTION ITSELF
the reason behind this is that gopro-overlay library requires older numpy version, the opencv version that uses this numpy version got a crappy checkboard detection, like really terrible one

Note that a keyboard and Mesbah's T-Shirt will be detected as checkboard if not carefully covered

1. Place your chessboard calibration images in the `./data/hidden_keyboard/` directory
2. Run the calibration script:
   ```bash
   python camera_calibration.py
   ```
3. Review debug images in `./data/out_images/` to verify corner detection
4. Calibration results will be saved to `calibration_result.npz`, containing:
   - Intrinsic matrix (K)
   - Distortion coefficients
   - Reprojection error
     \*For optimum results must have at least +10 images having thehre corners successfully parsed. If that wasnt' the case try to play with the ratio
     \*Reprojection error ideally should be below 0.5

## Output

The script generates two types of output:

1. Debug Images:

   - Processed images showing detected corners
   - Saved in `OUT_DEBUG_PATH`
   - Used for manual verification of corner detection accuracy

2. Calibration Results:
   - Saved in `calibration_result.npz`
   - Contains:
     - Intrinsic matrix (K)
     - Distortion coefficients
     - Reprojection error

## Troubleshooting

If corner detection fails for some images:

1. Check debug images in `OUT_DEBUG_PATH`
2. Verify chessboard pattern is clear and well-lit
3. Consider adjusting `board_size` if using a different chessboard pattern
4. Ensure chessboard squares are approximately `square_size` meters
