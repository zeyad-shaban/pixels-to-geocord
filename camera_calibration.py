import cv2
import numpy as np
import glob
import os
import shutil

# MAKE CHANGES HERE

IMAGE_PATH = "./data/hidden_keyboard/*.JPG"  # do i seriously need to explain this?
OUT_DEBUG_PATH = "./data/out_images/"  # after done calibrating go over that folder and manually ensure all corners are correctly predicted
board_size = (4, 4)  # amount of corners in the checkboard, so 5x5 checkboard got 4x4 corners
square_size = 3.5e-2  # unit in meters
ratio = 1 / 9  # ratio to downsample the image

# DONT MODIFY BELOW

if os.path.exists(OUT_DEBUG_PATH):
    shutil.rmtree(OUT_DEBUG_PATH)
os.makedirs(OUT_DEBUG_PATH, exist_ok=True)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object‐points
objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
objp[:, :2] = np.indices(board_size).T.reshape(-1, 2) * square_size

objpoints, imgpoints = [], []
images = glob.glob(IMAGE_PATH)

for fname in images:
    img = cv2.imread(fname)
    img = cv2.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio)))

    if img is None:
        print(f"Couldn’t load {fname}")
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    found, corners = cv2.findChessboardCorners(gray, board_size, None)
    print(f"{fname}: corners found? {found}, shape {img.shape}")
    if not found:
        continue

    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    objpoints.append(objp)
    imgpoints.append(corners)

    cv2.drawChessboardCorners(img, board_size, corners, found)

    # Save the processed image with corners
    output_path = os.path.join(OUT_DEBUG_PATH, os.path.basename(fname))
    cv2.imwrite(output_path, img)

    cv2.imshow("corners", img)
    cv2.waitKey(200)

cv2.destroyAllWindows()

if len(objpoints) < 3:
    raise RuntimeError("Not enough valid calibration images found.")

ret, K, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
K = K * 1 / ratio

print("Reprojection error:", ret)
print("Intrinsic K:\n", K)
print("Distortion coeffs:\n", dist_coeffs.ravel())

np.savez("calibration_result.npz", K=K, dist_coeffs=dist_coeffs)
print("Calibration results saved.")

# # %%
# import numpy as np
# stuff = np.load('calibration_result.npz')
# K = stuff['K']
# dist_coeffs = stuff['dist_coeffs']
# print(K)
# print(dist_coeffs)
