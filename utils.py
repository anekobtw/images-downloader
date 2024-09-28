import shutil
import uuid
from pathlib import Path

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
from PIL import Image

DOWNLOADS = Path("downloaded images")
DOWNLOADS.mkdir(exist_ok=True)


def update_entries(filter_checkbox: ctk.CTkCheckBox, *entries: ctk.CTkEntry) -> None:
    """Enable or disable resolution entry fields based on filter checkbox."""
    for entry in entries:
        entry.configure(
            state=["disabled", "normal"][filter_checkbox.get()],
            placeholder_text=entry._placeholder_text,
        )


def download(query: str, height: int = None, width: int = None) -> None:
    """Handle the download process based on user input."""
    for engine in ("google", "bing"):
        if getattr(f"{engine}_checkbox").get():
            download_images(query, engine)
            if height and width:
                filter_images(engine, height, width)

    CTkMessagebox(title="Images downloader", message="Images have been downloaded!", options=["Ok"])


def download_images(query: str, engine: str) -> None:
    """Download images using the specified search engine."""
    download_dir = DOWNLOADS / engine
    download_dir.mkdir(exist_ok=True)

    crawler_cls = GoogleImageCrawler if engine == "google" else BingImageCrawler
    crawler = crawler_cls(
        feeder_threads=200,
        parser_threads=200,
        downloader_threads=200,
        storage={"root_dir": download_dir},
    )
    crawler.crawl(keyword=query, max_num=999)


def filter_images(engine: str, height: int, width: int) -> None:
    """Filter images based on given resolution."""
    download_dir = DOWNLOADS / engine
    given_res_dir = DOWNLOADS / "Given resolution"
    similar_res_dir = DOWNLOADS / "Similar resolution"

    given_res_dir.mkdir(exist_ok=True)
    similar_res_dir.mkdir(exist_ok=True)

    for file in download_dir.glob('*.*'):
        if file.suffix not in (".png", ".jpg", ".jpeg"):
            continue

        img = Image.open(file)
        dst = (
            given_res_dir if img.size == (height, width)
            else similar_res_dir if img.size[0] / img.size[1] == height / width
            else None
        )
        img.close()

        shutil.move(file, dst / f"{uuid.uuid4()}.png") if dst else file.unlink()

    download_dir.rmdir()
