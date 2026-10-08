from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


INPUT = Path("source-photo.jpeg")
OUTPUT = Path("source-prepped.png")


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Could not find {INPUT}")

    print("1. Removing background...")

    with open(INPUT, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    temp_path = Path("source-no-bg.png")
    temp_path.write_bytes(output_data)

    print("2. Processing image...")

    # Open image with alpha channel
    image = cv2.imread(str(temp_path), cv2.IMREAD_UNCHANGED)

    if image is None:
        raise RuntimeError("Could not read processed image.")

    # Separate RGB and alpha
    if image.shape[2] == 4:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]
    else:
        bgr = image
        alpha = np.full(
            (image.shape[0], image.shape[1]),
            255,
            dtype=np.uint8,
        )

    # Convert to grayscale
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    gray = clahe.apply(gray)

    # White background using the removed-background alpha mask
    alpha_float = alpha.astype(np.float32) / 255.0

    white = np.full_like(gray, 255, dtype=np.float32)

    result = (
        gray.astype(np.float32) * alpha_float
        + white * (1.0 - alpha_float)
    )

    result = np.clip(result, 0, 255).astype(np.uint8)

    cv2.imwrite(str(OUTPUT), result)

    # Remove temporary file
    temp_path.unlink(missing_ok=True)

    print()
    print(f"Done!")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()