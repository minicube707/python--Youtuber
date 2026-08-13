# CHANGED FROM V1:
# asyncio is now used to coordinate concurrent tasks.
import asyncio
import time
from pathlib import Path

import requests
from PIL import Image

import shutil


# Command to run Scalene and generate an HTML profiling report:
# uv run scalene run --html --outfile profile_report01.html real_world_example_async_v1.py

# Command to open the profiling report in a web browser:
# uv run scalene view profile_report01.json


# List of image URLs to download.
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


def download_single_image(url: str, img_num: int) -> Path:
    """
    Download a single image and save it to the original images directory.

    NOTE:
    This function is still synchronous.
    In V2, it is executed in a separate thread using asyncio.to_thread().
    """

    print(f"Downloading {url}...")

    # Add a timestamp to the URL to prevent caching issues.
    ts = int(time.time())
    url = f"{url}?ts={ts}"

    # Perform the HTTP request.
    #
    # requests is a synchronous library, so this call would normally
    # block the current thread until the download is complete.
    response = requests.get(
        url,
        timeout=10,
        allow_redirects=True,
    )

    # Raise an exception if the request failed.
    response.raise_for_status()

    # Generate the local filename.
    filename = f"image_{img_num}.jpg"
    download_path = ORIGINAL_DIR / filename

    # Write the response to disk in chunks.
    # This avoids loading the entire response into memory at once.
    with download_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded and saved to: {download_path}")

    return download_path


# CHANGED FROM V1:
# This function is now asynchronous.
async def download_images(urls: list) -> list[Path]:
    """
    Download all images concurrently.

    Instead of downloading images one after another as in V1,
    each blocking download is executed in a separate thread.
    """

    # CHANGED FROM V1:
    # TaskGroup is used to manage multiple concurrent tasks.
    #
    # All tasks created inside the TaskGroup are allowed to run
    # concurrently, and the context manager waits for all of them
    # to finish before continuing.
    async with asyncio.TaskGroup() as tg:

        # CHANGED FROM V1:
        # Each synchronous download_single_image() call is moved
        # to a worker thread using asyncio.to_thread().
        #
        # This prevents the blocking requests.get() call from
        # blocking the asyncio event loop.
        tasks = [
            tg.create_task(
                asyncio.to_thread(
                    download_single_image,
                    url,
                    img_num,
                )
            )
            for img_num, url in enumerate(urls, start=1)
        ]

    # Retrieve the result of each completed task.
    #
    # The order is preserved because the tasks list was created
    # in the same order as the input URLs.
    img_paths = [task.result() for task in tasks]

    return img_paths


def process_single_image(orig_path: Path) -> Path:
    """
    Process a single image using a simple edge-detection algorithm.

    The algorithm compares each pixel with its right and bottom
    neighbors and converts the image into a black/white edge map.

    NOTE:
    The processing logic itself is unchanged from V1.
    """

    # Create the output path using the same filename as the original image.
    save_path = PROCESSED_DIR / orig_path.name

    # Open the image with Pillow.
    with Image.open(orig_path) as img:

        # Convert the image into a list of RGB pixel values.
        data = list(img.get_flattened_data())

        # Get the image dimensions.
        width, height = img.size

        # Store the pixels of the resulting black/white image.
        new_data = []

        # Process every pixel in the image.
        for i in range(len(data)):

            # Get the RGB values of the current pixel.
            current_r, current_g, current_b = data[i]

            total_diff = 0
            neighbor_count = 0

            # Compare the current pixel with:
            # - the pixel to the right
            # - the pixel below
            for dx, dy in [(1, 0), (0, 1)]:

                # Convert the linear pixel index into x/y coordinates.
                x = (i % width) + dx
                y = (i // width) + dy

                # Make sure the neighbor is inside the image boundaries.
                if 0 <= x < width and 0 <= y < height:

                    # Get the RGB values of the neighboring pixel.
                    neighbor_r, neighbor_g, neighbor_b = data[
                        y * width + x
                    ]

                    # Calculate the RGB difference between the two pixels.
                    diff = (
                        abs(current_r - neighbor_r)
                        + abs(current_g - neighbor_g)
                        + abs(current_b - neighbor_b)
                    )

                    total_diff += diff
                    neighbor_count += 1

            # Calculate the average difference between the pixel
            # and its valid neighbors.
            if neighbor_count > 0:
                edge_strength = total_diff // neighbor_count

                # Pixels with a sufficiently large difference are
                # considered edges and become white.
                if edge_strength > 30:
                    new_data.append((255, 255, 255))

                # Non-edge pixels become black.
                else:
                    new_data.append((0, 0, 0))

            # Pixels without neighbors are considered non-edge pixels.
            else:
                new_data.append((0, 0, 0))

        # Create a new RGB image with the same dimensions.
        edge_img = Image.new("RGB", (width, height))

        # Replace its pixels with the generated black/white data.
        edge_img.putdata(new_data)

        # Save the processed image.
        edge_img.save(save_path)

    print(f"Processed {orig_path} and saved to {save_path}")

    return save_path


# CHANGED FROM V1:
# This function is now asynchronous.
async def process_images(orig_paths: list[Path]) -> list[Path]:
    """
    Process all images concurrently.

    Each image-processing operation is moved to a separate worker thread.
    """

    # CHANGED FROM V1:
    # Use TaskGroup to manage multiple image-processing tasks.
    async with asyncio.TaskGroup() as tg:

        # CHANGED FROM V1:
        # process_single_image() is synchronous, so it is executed
        # in a worker thread using asyncio.to_thread().
        #
        # This allows several images to be processed concurrently.
        tasks = [
            tg.create_task(
                asyncio.to_thread(
                    process_single_image,
                    orig_path,
                )
            )
            for orig_path in orig_paths
        ]

    # Collect the results from all completed tasks.
    img_paths = [task.result() for task in tasks]

    return img_paths


# CHANGED FROM V1:
# main() is now an asynchronous function.
async def main():
    """Run the complete asynchronous workflow."""

    # Create the required directories if they do not already exist.
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Start measuring the total execution time.
    start_time = time.perf_counter()

    # CHANGED FROM V1:
    # Wait asynchronously for all downloads to complete.
    img_paths = await download_images(IMAGE_URLS)

    # Mark the beginning of the image-processing phase.
    proc_start_time = time.perf_counter()

    # CHANGED FROM V1:
    # Wait asynchronously for all image-processing tasks to complete.
    processed_paths = await process_images(img_paths)

    # Mark the end of the complete workflow.
    finished_time = time.perf_counter()

    # Calculate the duration of each phase.
    dl_total_time = proc_start_time - start_time
    proc_total_time = finished_time - proc_start_time
    total_time = finished_time - start_time

    # Display download performance.
    print(
        f"\nDownloaded {len(img_paths)} images in: "
        f"{dl_total_time:.2f} seconds. "
        f"{(dl_total_time / total_time) * 100:.2f}% of total time",
    )

    # Display image-processing performance.
    print(
        f"Processed {len(processed_paths)} images in: "
        f"{proc_total_time:.2f} seconds. "
        f"{(proc_total_time / total_time) * 100:.2f}% of total time",
    )

    # Display total execution time.
    print(
        f"\nTotal execution time: {total_time:.2f} seconds. "
        f"{(total_time / total_time) * 100:.2f}% of total time",
    )

    # Delete the directory containing the original images.
    folder_path = ORIGINAL_DIR
    shutil.rmtree(folder_path)
    print(f"\nFolder '{folder_path}' deleted successfully.")

    # Delete the directory containing the processed images.
    folder_path = PROCESSED_DIR
    shutil.rmtree(folder_path)
    print(f"Folder '{folder_path}' deleted successfully.")


# CHANGED FROM V1:
# main() is now asynchronous, so asyncio.run() is required
# to create and manage the event loop.
if __name__ == "__main__":
    asyncio.run(main())