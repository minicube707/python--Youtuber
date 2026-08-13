import time
from pathlib import Path

import requests
from PIL import Image

import shutil


# Command to run Scalene and generate an HTML profiling report:
# uv run scalene run --html --outfile profile_report00.html real_world_example_sync_v1.py

# Command to open the profiling report in a web browser:
# uv run scalene view profile_report00.json


# List of image URLs to download.
# Each image is requested at 1920x1080 and cropped to fit these dimensions.
IMAGE_URLS = [
    "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1532009324734-20a7a5813719?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1524429656589-6633a470097c?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530224264768-7ff8c1789d79?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1564135624576-c5c88640f235?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1541698444083-023c97d3f4b6?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1522364723953-452d3431c267?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1516972810927-80185027ca84?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1550439062-609e1531270e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=1920&h=1080&fit=crop",
]


# Directories used to store the original and processed images.
ORIGINAL_DIR = Path("original_images")
PROCESSED_DIR = Path("processed_images")


def download_single_image(
    session: requests.Session,
    url: str,
    img_num: int,
) -> Path:
    """Download a single image and save it to the original images directory."""

    print(f"Downloading {url}...")

    # Add a timestamp to the URL to prevent the request from being served
    # from a cache.
    ts = int(time.time())
    url = f"{url}?ts={ts}"

    # Send the HTTP GET request.
    # A timeout prevents the program from waiting indefinitely.
    # Redirects are explicitly allowed.
    response = session.get(
        url,
        timeout=10,
        allow_redirects=True,
    )

    # Raise an exception if the HTTP request returned an error status code.
    response.raise_for_status()

    # Generate a local filename for the downloaded image.
    filename = f"image_{img_num}.jpg"
    download_path = ORIGINAL_DIR / filename

    # Open the destination file in binary write mode.
    # The image is downloaded in chunks instead of loading the entire
    # response into memory at once.
    with download_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded and saved to: {download_path}")

    return download_path


def download_images(urls: list) -> list[Path]:
    """Download all images sequentially and return their local paths."""

    # A single Session is reused for all HTTP requests.
    # This allows requests to reuse the underlying connection when possible.
    with requests.Session() as session:

        # Images are downloaded one after another.
        # enumerate() provides an image number starting at 1.
        img_paths = [
            download_single_image(session, url, img_num)
            for img_num, url in enumerate(urls, start=1)
        ]

    return img_paths


def process_single_image(orig_path: Path) -> Path:
    """Detect edges in an image and save the result as a black/white image."""

    # Create the output path using the same filename as the original image.
    save_path = PROCESSED_DIR / orig_path.name

    # Open the image using Pillow.
    # The context manager automatically closes the image afterwards.
    with Image.open(orig_path) as img:

        # Convert the image data into a list of RGB pixel values.
        # Each element contains the red, green, and blue values of one pixel.
        data = list(img.get_flattened_data())

        # Get the image dimensions.
        width, height = img.size

        # This list will contain the resulting black/white pixels.
        new_data = []

        # Process every pixel in the image.
        for i in range(len(data)):

            # Get the RGB values of the current pixel.
            current_r, current_g, current_b = data[i]

            total_diff = 0
            neighbor_count = 0

            # Only two neighbors are checked:
            # - the pixel immediately to the right
            # - the pixel immediately below
            #
            # This is enough to detect local changes in pixel intensity
            # while avoiding duplicate comparisons.
            for dx, dy in [(1, 0), (0, 1)]:

                # Convert the linear pixel index into x/y coordinates
                # and calculate the coordinates of the neighboring pixel.
                x = (i % width) + dx
                y = (i // width) + dy

                # Make sure the neighboring pixel is inside the image.
                if 0 <= x < width and 0 <= y < height:

                    # Retrieve the RGB values of the neighboring pixel.
                    neighbor_r, neighbor_g, neighbor_b = data[y * width + x]

                    # Calculate the absolute difference between the current
                    # pixel and its neighbor for each RGB channel.
                    diff = (
                        abs(current_r - neighbor_r)
                        + abs(current_g - neighbor_g)
                        + abs(current_b - neighbor_b)
                    )

                    total_diff += diff
                    neighbor_count += 1

            # Calculate the average difference between the current pixel
            # and its valid neighbors.
            if neighbor_count > 0:
                edge_strength = total_diff // neighbor_count

                # If the average difference is greater than 30,
                # consider the pixel part of an edge and make it white.
                if edge_strength > 30:
                    new_data.append((255, 255, 255))

                # Otherwise, consider it a non-edge pixel and make it black.
                else:
                    new_data.append((0, 0, 0))

            # Pixels without valid neighbors are made black.
            else:
                new_data.append((0, 0, 0))

        # Create a new RGB image with the same dimensions as the original.
        edge_img = Image.new("RGB", (width, height))

        # Replace the image pixels with the calculated black/white data.
        edge_img.putdata(new_data)

        # Save the processed image to the processed images directory.
        edge_img.save(save_path)

    print(f"Processed {orig_path} and saved to {save_path}")

    return save_path


def process_images(orig_paths: list[Path]) -> list[Path]:
    """Process all images sequentially and return their output paths."""

    # Each image is processed one after another.
    img_paths = [
        process_single_image(orig_path)
        for orig_path in orig_paths
    ]

    return img_paths


def main():
    """Run the complete download, processing, benchmarking, and cleanup workflow."""

    # Create the required directories if they do not already exist.
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Start measuring the total execution time.
    start_time = time.perf_counter()

    # Download all images.
    img_paths = download_images(IMAGE_URLS)

    # Mark the end of the download phase and the beginning
    # of the image processing phase.
    proc_start_time = time.perf_counter()

    # Process all downloaded images.
    processed_paths = process_images(img_paths)

    # Mark the end of the complete workflow.
    finished_time = time.perf_counter()

    # Calculate the duration of each phase.
    dl_total_time = proc_start_time - start_time
    proc_total_time = finished_time - proc_start_time
    total_time = finished_time - start_time

    # Display download performance and its percentage of the total time.
    print(
        f"\nDownloaded {len(img_paths)} images in: "
        f"{dl_total_time:.2f} seconds. "
        f"{(dl_total_time / total_time) * 100:.2f}% of total time",
    )

    # Display image processing performance and its percentage
    # of the total execution time.
    print(
        f"Processed {len(processed_paths)} images in: "
        f"{proc_total_time:.2f} seconds. "
        f"{(proc_total_time / total_time) * 100:.2f}% of total time",
    )

    # Display the total execution time.
    # The percentage is always 100% because total_time is divided by itself.
    print(
        f"\nTotal execution time: {total_time:.2f} seconds. "
        f"{(total_time / total_time) * 100:.2f}% of total time",
    )

    # Delete the directory containing the original downloaded images.
    folder_path = ORIGINAL_DIR
    shutil.rmtree(folder_path)
    print(f"\nFolder '{folder_path}' deleted successfully.")

    # Delete the directory containing the processed images.
    folder_path = PROCESSED_DIR
    shutil.rmtree(folder_path)
    print(f"Folder '{folder_path}' deleted successfully.")


# Run the main function only when this file is executed directly.
# This prevents main() from running automatically if the module is imported.
if __name__ == "__main__":
    main()