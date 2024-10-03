import os
from pathlib import Path

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


def filter_images(height: int, width: int) -> None:
    """Filter images based on given resolution."""
    for file in pinterest_dir.glob("*.*"):
        img = Image.open(file)
        if file.suffix not in (".png", ".jpg", ".jpeg") or img.size != (height, width):
            print(f"Deleting {file.absolute()}")
            os.remove(file)
        img.close()


def download_images(query: str) -> None:
    crawl_pinterest(query, 5)
    crawl_google(query, 5)


if __name__ == "__main__":
    download_images("key png")
