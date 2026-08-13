# CHANGED FROM V2:
# asyncio is still used to coordinate the asynchronous workflow.
import asyncio
import time

# NEW IN V3:
# ProcessPoolExecutor is used to run CPU-intensive image processing
# in separate processes instead of threads.
from concurrent.futures import ProcessPoolExecutor

from pathlib import Path

# NEW IN V3:
# aiofiles provides asynchronous file I/O.
import aiofiles

# NEW IN V3:
# httpx provides a native asynchronous HTTP client.
import httpx

from PIL import Image

import shutil


# Command to run Scalene and generate an HTML profiling report:
# uv run scalene run --html --outfile profile_report02.html real_world_example_async_v2.py

# Command to open the profiling report in a web browser:
# uv run scalene view profile_report02.json


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


# CHANGED FROM V2:
# The function is now fully asynchronous.
#
# In V2, requests.get() was synchronous and had to be wrapped
# inside asyncio.to_thread().
#
# In V3, httpx.AsyncClient is used directly, so no worker thread
# is required for the HTTP request.
async def download_single_image(
    client: httpx.AsyncClient,
    url: str,
    img_num: int,
) -> Path:
    """Download a single image asynchronously and save it to disk."""

    print(f"Downloading {url}...")

    # Add a timestamp to the URL to prevent caching issues.
    ts = int(time.time())
    url = f"{url}?ts={ts}"

    # CHANGED FROM V2:
    # Perform the HTTP request asynchronously using httpx.
    #
    # Unlike requests.get(), this does not block the asyncio event loop
    # while waiting for the network response.
    response = await client.get(
        url,
        timeout=10,
        follow_redirects=True,
    )

    # Raise an exception if the request failed.
    response.raise_for_status()

    # Generate the local filename.
    filename = f"image_{img_num}.jpg"
    download_path = ORIGINAL_DIR / filename

    # CHANGED FROM V2:
    # aiofiles provides asynchronous file writing.
    #
    # This prevents file I/O from blocking the event loop.
    async with aiofiles.open(download_path, "wb") as f:

        # Read the response asynchronously in chunks.
        # This avoids loading the entire image into memory at once.
        async for chunk in response.aiter_bytes(chunk_size=8192):

            # Write each chunk asynchronously.
            await f.write(chunk)

    print(f"Downloaded and saved to: {download_path}")

    return download_path


async def download_images(urls: list) -> list[Path]:
    """
    Download all images concurrently using asynchronous HTTP requests.

    V3 uses native async I/O instead of wrapping synchronous requests
    in worker threads.
    """

    # NEW IN V3:
    # Create a shared asynchronous HTTP client.
    #
    # Reusing the same client allows connections to be reused efficiently.
    async with httpx.AsyncClient() as client:

        # TaskGroup is still used to manage the concurrent downloads.
        async with asyncio.TaskGroup() as tg:

            # CHANGED FROM V2:
            # download_single_image() is already asynchronous,
            # so asyncio.to_thread() is no longer necessary.
            tasks = [
                tg.create_task(
                    download_single_image(
                        client,
                        url,
                        img_num,
                    )
                )
                for img_num, url in enumerate(urls, start=1)
            ]

        # Retrieve the result from each completed task.
        img_paths = [task.result() for task in tasks]

    return img_paths


def process_single_image(orig_path: Path) -> Path:
    """
    Process a single image using a simple edge-detection algorithm.

    This function remains synchronous because the image-processing
    operation is CPU-intensive.
    """

    save_path = PROCESSED_DIR / orig_path.name

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

            # Compare the current pixel with its right and bottom neighbors.
            for dx, dy in [(1, 0), (0, 1)]:

                # Convert the linear pixel index into x/y coordinates.
                x = (i % width) + dx
                y = (i // width) + dy

                # Make sure the neighboring pixel is inside the image.
                if 0 <= x < width and 0 <= y < height:

                    # Retrieve the neighboring pixel's RGB values.
                    neighbor_r, neighbor_g, neighbor_b = data[
                        y * width + x
                    ]

                    # Calculate the absolute RGB difference.
                    diff = (
                        abs(current_r - neighbor_r)
                        + abs(current_g - neighbor_g)
                        + abs(current_b - neighbor_b)
                    )

                    total_diff += diff
                    neighbor_count += 1

            # Calculate the average difference with the valid neighbors.
            if neighbor_count > 0:
                edge_strength = total_diff // neighbor_count

                # A strong difference indicates an edge.
                if edge_strength > 30:
                    new_data.append((255, 255, 255))

                # Otherwise, the pixel is considered a non-edge.
                else:
                    new_data.append((0, 0, 0))

            # Pixels without valid neighbors are black.
            else:
                new_data.append((0, 0, 0))

        # Create the output image.
        edge_img = Image.new("RGB", (width, height))

        # Insert the generated black/white pixel data.
        edge_img.putdata(new_data)

        # Save the processed image.
        edge_img.save(save_path)

    print(f"Processed {orig_path} and saved to {save_path}")

    return save_path


# CHANGED FROM V2:
# Image processing is no longer performed with asyncio.to_thread().
#
# Instead, a ProcessPoolExecutor is used.
# Each image can therefore be processed in a separate Python process.
async def process_images(orig_paths: list[Path]) -> list[Path]:
    """
    Process all images concurrently using multiple processes.

    This is particularly useful for CPU-bound workloads because
    separate processes can execute Python code in parallel without
    being restricted by the Global Interpreter Lock (GIL).
    """

    # Get the currently running asyncio event loop.
    loop = asyncio.get_running_loop()

    # Create a pool of worker processes.
    #
    # The number of workers is determined by ProcessPoolExecutor's
    # default configuration.
    with ProcessPoolExecutor() as executor:

        # Submit each image-processing operation to the process pool.
        #
        # run_in_executor() allows asyncio to wait asynchronously
        # for the CPU-bound tasks while they execute in worker processes.
        tasks = [
            loop.run_in_executor(
                executor,
                process_single_image,
                orig_path,
            )
            for orig_path in orig_paths
        ]

        # Wait until all processes have completed their work.
        processed_paths = await asyncio.gather(*tasks)

    return processed_paths


async def main():
    """Run the complete asynchronous workflow."""

    # Create the required directories if they do not already exist.
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Start measuring the total execution time.
    start_time = time.perf_counter()

    # Download all images concurrently using asynchronous HTTP I/O.
    img_paths = await download_images(IMAGE_URLS)

    # Mark the beginning of the image-processing phase.
    proc_start_time = time.perf_counter()

    # Process all images concurrently using multiple processes.
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