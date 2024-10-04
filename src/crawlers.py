import logging
import os
from pathlib import Path

import rembg
from icrawler.builtin import GoogleImageCrawler
from PIL import Image
from pinterest_crawler import PinterestCrawler

Path("downloads").mkdir(exist_ok=True)
pinterest_dir = Path("downloads/pinterest")
pinterest_dir.mkdir(exist_ok=True)
google_dir = Path("downloads/google")
google_dir.mkdir(exist_ok=True)


def crawl_pinterest(query: str) -> None:
    pinterest_crawler = PinterestCrawler(output_dir_path="downloads/pinterest")
    pinterest_crawler(query.split())


def crawl_google(query: str, limit: int = 1000) -> None:
    crawler = GoogleImageCrawler(downloader_threads=limit, storage={"root_dir": google_dir})
    crawler.crawl(keyword=query, max_num=limit, overwrite=True)


def filter_images(directory: Path, height: int, width: int) -> None:
    """Filter images based on given resolution."""
    for file in directory.glob("*.*"):
        if file.suffix not in (".png", ".jpg", ".jpeg"):
            print(f"Deleting {file.absolute()}")
            os.remove(file)
            continue

        img = Image.open(file)
        if height and width and img.size != (int(height), int(width)):
            print(f"Deleting {file.absolute()}")
            img.close()
            os.remove(file)
            continue


def remove_background(directory: Path) -> None:
    """Remove background from the images."""
    for file in directory.glob("*.*"):
        logging.debug(f"Removing bg from {file}")
        input_path = file
        output_path = file.with_suffix(".png")

        with Image.open(input_path) as img:
            img = img.convert("RGBA")
            output = rembg.remove(img)
            output.save(output_path)

        logging.debug(f"Removed bg from {file}")
        if input_path != output_path:
            os.remove(input_path)


def download_images(query: str, google: bool, pinterest: bool, height: int, width: int, remove_bg: bool) -> None:
    if google:
        crawl_google(query, 150)
    if pinterest:
        crawl_pinterest(query)

    filter_images(google_dir, height, width)
    filter_images(pinterest_dir, height, width)
    if remove_bg:
        remove_background(google_dir)
        remove_background(pinterest_dir)


if __name__ == "__main__":
    download_images("key png")
