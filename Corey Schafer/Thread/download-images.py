import concurrent.futures
import os
import time

import requests

# Change the working directory so downloaded images
# are saved next to this Python script.
module_dir = os.path.dirname(__file__)
os.chdir(module_dir)


# List of images to download.
img_urls = [
    "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759",
    "https://images.unsplash.com/photo-1532009324734-20a7a5813719",
    "https://images.unsplash.com/photo-1524429656589-6633a470097c",
    "https://images.unsplash.com/photo-1530224264768-7ff8c1789d79",
    "https://images.unsplash.com/photo-1564135624576-c5c88640f235",
    "https://images.unsplash.com/photo-1541698444083-023c97d3f4b6",
    "https://images.unsplash.com/photo-1522364723953-452d3431c267",
    "https://images.unsplash.com/photo-1513938709626-033611b8cc03",
    "https://images.unsplash.com/photo-1507143550189-fed454f93097",
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e",
    "https://images.unsplash.com/photo-1504198453319-5ce911bafcde",
    "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99",
    "https://images.unsplash.com/photo-1516972810927-80185027ca84",
    "https://images.unsplash.com/photo-1550439062-609e1531270e",
    "https://images.unsplash.com/photo-1549692520-acc6669e2f0c",
]


def download_image(img_url):
    """
    Download an image from the given URL and save it locally.
    """

    # Download the image content.
    img_bytes = requests.get(img_url).content

    # Generate a filename from the URL.
    img_name = img_url.split("/")[3]
    img_name = f"{img_name}.jpg"

    # Save the image to disk.
    with open(img_name, "wb") as img_file:
        img_file.write(img_bytes)

    print(f"{img_name} was downloaded...")


def remove_images():
    """
    Delete every downloaded JPG file from the current directory.
    """

    for file in os.listdir():
        if file.endswith(".jpg"):
            os.remove(file)


def download_without_thread_pool():
    """
    Download images sequentially.

    Each download starts only after the previous one finishes.
    """

    print("Download without ThreadPoolExecutor")

    start = time.perf_counter()

    for img_url in img_urls:
        download_image(img_url)

    finish = time.perf_counter()

    print(f"Finished in {finish - start:.2f} second(s)")


def download_with_thread_pool():
    """
    Download images concurrently using ThreadPoolExecutor.

    Since downloading images is an I/O-bound task,
    multiple downloads can happen simultaneously,
    significantly reducing the total execution time.
    """

    print("\nDownload with ThreadPoolExecutor")

    start = time.perf_counter()

    # Create a pool of worker threads.
    with concurrent.futures.ThreadPoolExecutor() as executor:

        # Schedule one download task for each URL.
        # executor.map() blocks until all downloads complete.
        executor.map(download_image, img_urls)

    finish = time.perf_counter()

    print(f"Finished in {finish - start:.2f} second(s)")


# ---------------------------------------------------------
# Compare sequential downloads with concurrent downloads.
# ---------------------------------------------------------

download_without_thread_pool()

# Remove downloaded files before the next test.
remove_images()

download_with_thread_pool()

# Clean up downloaded files.
remove_images()