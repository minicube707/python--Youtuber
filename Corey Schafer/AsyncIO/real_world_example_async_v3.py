# asyncio is used to coordinate the asynchronous workflow.
import asyncio

# NEW IN V4:
# os.cpu_count() is used to determine the number of CPU workers.
import os

import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import aiofiles
import httpx
from PIL import Image

import shutil


# NEW IN V4:
# Maximum number of downloads allowed to run concurrently.
#
# This prevents all image downloads from starting at the same time,
# which can reduce network contention and avoid putting too much
# pressure on the remote server or the local system.
DOWNLOAD_LIMIT = 4


# NEW IN V4:
# Use the number of available CPU cores to determine the number
# of worker processes used for image processing.
#
# This makes the process pool adapt to the machine running the program.
CPU_WORKERS = os.cpu_count()


# Command to run Scalene and generate an HTML profiling report:
# uv run scalene run --html --outfile profile_report03.html real_world_example_async_v3.py

# Command to open the profiling report in a web browser:
# uv run scalene view profile_report03.json


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


async def download_single_image(
    client: httpx.AsyncClient,
    url: str,
    img_num: int,
    semaphore: asyncio.Semaphore,
) -> Path:
    """
    Download a single image asynchronously.

    The semaphore limits the number of downloads that can execute
    concurrently.
    """

    # NEW IN V4:
    # Acquire the semaphore before starting the download.
    #
    # Only DOWNLOAD_LIMIT tasks can enter this block at the same time.
    # The remaining tasks wait until a slot becomes available.
    async with semaphore:

        print(f"Downloading {url}...")

        # Add a timestamp to the URL to prevent caching issues.
        ts = int(time.time())
        url = f"{url}?ts={ts}"

        # Perform the HTTP request asynchronously.
        response = await client.get(
            url,
            timeout=10,
            follow_redirects=True,
        )

        # Raise an exception if the HTTP request failed.
        response.raise_for_status()

        # Generate the local filename.
        filename = f"image_{img_num}.jpg"
        download_path = ORIGINAL_DIR / filename

        # Write the image asynchronously to disk.
        async with aiofiles.open(download_path, "wb") as f:

            # Download the response in chunks instead of loading
            # the complete image into memory.
            async for chunk in response.aiter_bytes(chunk_size=8192):

                # Write each chunk asynchronously.
                await f.write(chunk)

        print(f"Downloaded and saved to: {download_path}")

        return download_path


async def download_images(urls: list) -> list[Path]:
    """
    Download all images concurrently with a controlled concurrency limit.
    """

    # NEW IN V4:
    # Create a semaphore that limits concurrent downloads to DOWNLOAD_LIMIT.
    dl_semaphore = asyncio.Semaphore(DOWNLOAD_LIMIT)

    # Create one shared asynchronous HTTP client for all requests.
    async with httpx.AsyncClient() as client:

        # TaskGroup manages all download tasks.
        async with asyncio.TaskGroup() as tg:

            # CHANGED FROM V3:
            # The semaphore is passed to every download task.
            #
            # All tasks are still created immediately, but the semaphore
            # ensures that only DOWNLOAD_LIMIT downloads actually run
            # at the same time.
            tasks = [
                tg.create_task(
                    download_single_image(
                        client,
                        url,
                        img_num,
                        dl_semaphore,
                    )
                )
                for img_num, url in enumerate(urls, start=1)
            ]

        # Retrieve the result of each completed task.
        img_paths = [task.result() for task in tasks]

    return img_paths


def process_single_image(orig_path: Path) -> Path:
    """
    Process a single image using a simple edge-detection algorithm.

    This CPU-intensive function is executed in a separate process
    by ProcessPoolExecutor.
    """

    # Define the path of the processed image.
    save_path = PROCESSED_DIR / orig_path.name

    # Open the image with Pillow.
    with Image.open(orig_path) as img:

        # Convert the image into a list of RGB pixel values.
        data = list(img.get_flattened_data())

        # Get the image dimensions.
        width, height = img.size

        # Store the generated black/white pixels.
        new_data = []

        # Process every pixel in the image.
        for i in range(len(data)):

            # Get the RGB values of the current pixel.
            current_r, current_g, current_b = data[i]

            total_diff = 0
            neighbor_count = 0

            # Compare the current pixel with its right and bottom neighbors.
            for dx, dy in [(1, 0), (0, 1)]:

                # Convert the linear pixel index into x/y coordinates.
                x = (i % width) + dx
                y = (i // width) + dy

                # Check that the neighbor is inside the image.
                if 0 <= x < width and 0 <= y < height:

                    # Retrieve the neighboring pixel's RGB values.
                    neighbor_r, neighbor_g, neighbor_b = data[
                        y * width + x
                    ]

                    # Calculate the difference between the two pixels.
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

                # A large difference indicates an edge.
                if edge_strength > 30:
                    new_data.append((255, 255, 255))

                # Otherwise, the pixel is considered non-edge.
                else:
                    new_data.append((0, 0, 0))

            # Pixels without valid neighbors are black.
            else:
                new_data.append((0, 0, 0))

        # Create the resulting RGB image.
        edge_img = Image.new("RGB", (width, height))

        # Insert the calculated black/white pixel data.
        edge_img.putdata(new_data)

        # Save the processed image.
        edge_img.save(save_path)

    print(f"Processed {orig_path} and saved to {save_path}")

    return save_path


async def process_images(orig_paths: list[Path]) -> list[Path]:
    """
    Process images concurrently using multiple CPU processes.
    """

    # Get the currently running asyncio event loop.
    loop = asyncio.get_running_loop()

    # CHANGED IN V4:
    # Explicitly configure the number of worker processes.
    #
    # V3 relied on ProcessPoolExecutor's default number of workers.
    # V4 explicitly uses the number of CPUs available on the machine.
    with ProcessPoolExecutor(max_workers=CPU_WORKERS) as executor:

        # Submit one image-processing task per image.
        #
        # Each task is executed by a separate worker process
        # when a worker becomes available.
        tasks = [
            loop.run_in_executor(
                executor,
                process_single_image,
                orig_path,
            )
            for orig_path in orig_paths
        ]

        # Wait asynchronously for all processing tasks to finish.
        processed_paths = await asyncio.gather(*tasks)

    return processed_paths


async def main():
    """Run the complete asynchronous workflow."""

    # Create the required directories if they do not already exist.
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Start measuring total execution time.
    start_time = time.perf_counter()

    # Download all images asynchronously.
    #
    # V4 limits the number of simultaneous downloads to DOWNLOAD_LIMIT.
    img_paths = await download_images(IMAGE_URLS)

    # Mark the beginning of the image-processing phase.
    proc_start_time = time.perf_counter()

    # Process all images using the configured process pool.
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

    # Delete the original image directory.
    folder_path = ORIGINAL_DIR
    shutil.rmtree(folder_path)
    print(f"\nFolder '{folder_path}' deleted successfully.")

    # Delete the processed image directory.
    folder_path = PROCESSED_DIR
    shutil.rmtree(folder_path)
    print(f"Folder '{folder_path}' deleted successfully.")


# Start the asyncio event loop and execute the asynchronous main function.
if __name__ == "__main__":
    asyncio.run(main())