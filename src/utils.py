from pathlib import Path

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from icrawler.builtin import GoogleImageCrawler
from PIL import Image
from rembg import remove

DOWNLOADS = Path("downloaded images")
DOWNLOADS.mkdir(exist_ok=True)


def update_entries(filter_checkbox: ctk.CTkCheckBox, *entries: ctk.CTkEntry) -> None:
    """Enable or disable resolution entry fields based on filter checkbox."""
    for entry in entries:
        entry.configure(
            state=["disabled", "normal"][filter_checkbox.get()],
            placeholder_text=entry._placeholder_text,
        )


def download(
    query: str,
    height: int = None,
    width: int = None,
    do_rembg: bool = False,
    google: bool = False,
    bing: bool = False,
) -> None:
    """Handle the download process based on user input."""
    engine = "google"

    for engine, enabled in engines.items():
        if not enabled:
            continue
        download_images(query, engine)
        if do_rembg:
            for file in (DOWNLOADS / engine).iterdir():
                img = Image.open(str(file)).convert("RGBA")
                output = remove(img)
                output.save(str(file)[:-4] + ".png")
        if height and width:
            filter_images(engine, height, width)
    CTkMessagebox(
        title="Images downloader",
        message="Images have been downloaded!",
        options=["Ok"],
    )


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
