from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import shutil
import time

from PIL import Image, ImageFilter

# Directory where processed images will be stored
OUTPUT_DIR = Path("processed")

# Maximum image size
THUMBNAIL_SIZE = (1200, 1200)

# Images to process
IMAGE_NAMES = [
    "photo-1516117172878-fd2c41f4a759.jpg",
    "photo-1532009324734-20a7a5813719.jpg",
    "photo-1524429656589-6633a470097c.jpg",
    "photo-1530224264768-7ff8c1789d79.jpg",
    "photo-1564135624576-c5c88640f235.jpg",
    "photo-1541698444083-023c97d3f4b6.jpg",
    "photo-1522364723953-452d3431c267.jpg",
    "photo-1513938709626-033611b8cc03.jpg",
    "photo-1507143550189-fed454f93097.jpg",
    "photo-1493976040374-85c8e12f0c0e.jpg",
    "photo-1504198453319-5ce911bafcde.jpg",
    "photo-1530122037265-a5f1f91d3b99.jpg",
    "photo-1516972810927-80185027ca84.jpg",
    "photo-1550439062-609e1531270e.jpg",
    "photo-1549692520-acc6669e2f0c.jpg",
]


def process_image(image_name):
    """
    Apply a Gaussian blur, resize the image,
    and save it to the output directory.
    """
    image = Image.open(image_name)

    # Apply a blur effect
    image = image.filter(ImageFilter.GaussianBlur(radius=15))

    # Resize the image while preserving its aspect ratio
    image.thumbnail(THUMBNAIL_SIZE)

    # Save the processed image
    output_path = OUTPUT_DIR / image_name
    image.save(output_path)

    print(f"{image_name} processed.")


def process_sequential(images):
    """Process all images sequentially."""
    print("\n=== Sequential processing ===")

    start = time.perf_counter()

    for image in images:
        process_image(image)

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)\n")


def process_parallel(images):
    """Process all images using multiple processes."""
    print("\n=== Multiprocessing ===")

    start = time.perf_counter()

    # executor.map() distributes the work across multiple processes
    with ProcessPoolExecutor() as executor:
        list(executor.map(process_image, images))

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)\n")


def cleanup():
    """Remove all processed images and delete the output directory."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)


def main():
    """Run the image processing examples."""

    # Create the output directory if it does not already exist
    OUTPUT_DIR.mkdir(exist_ok=True)

    process_sequential(IMAGE_NAMES)
    process_parallel(IMAGE_NAMES)

    cleanup()


if __name__ == "__main__":
    # Required when using ProcessPoolExecutor on Windows.
    # Without this guard, child processes would re-execute the script.
    main()