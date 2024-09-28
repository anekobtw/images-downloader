import logging
import shutil
import uuid
import os
from pathlib import Path

import customtkinter as ctk
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
from CTkMessagebox import CTkMessagebox
from PIL import Image

__version__ = "1.2.0"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ctk.set_default_color_theme("theme.json")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloads_dir = Path("downloaded images")
        self.downloads_dir.mkdir(exist_ok=True)

        self.title("Images Downloader")
        self.draw_infobar()
        self.draw_settingsbar()

    def draw_infobar(self) -> None:
        sidebar = ctk.CTkFrame(self, width=140)
        sidebar.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        # Info Label
        ctk.CTkLabel(sidebar, text=f"Images Downloader {__version__}", font=ctk.CTkFont(size=20, weight="bold")).grid(padx=20, pady=(10, 0))
        ctk.CTkLabel(sidebar, text="© anekobtw, 2024\ntheme by avalon60").grid(padx=10, pady=(5, 10))

        # Query Entry and Download Button
        self.query_entry = ctk.CTkEntry(sidebar, placeholder_text="Query")
        self.query_entry.grid(padx=10, pady=(20, 0))
        ctk.CTkButton(sidebar, text="Download", command=self.download).grid(padx=10, pady=(10, 20))

        ctk.CTkButton(sidebar, text="Open Downloads Folder", command=lambda: os.startfile(self.downloads_dir)).grid(pady=5)

    def draw_settingsbar(self) -> None:
        settingsbar = ctk.CTkFrame(self)
        settingsbar.grid(row=0, column=1, pady=20, padx=20, sticky="ew")

        ctk.CTkLabel(settingsbar, text="Settings", font=ctk.CTkFont(size=20, weight="bold")).grid()

        # Search Engine Checkboxes
        gb_frame = ctk.CTkFrame(settingsbar, fg_color="transparent")
        gb_frame.grid(pady=10, padx=20, sticky="nsew")

        self.google_checkbox = ctk.CTkCheckBox(gb_frame, text="Google", corner_radius=36)
        self.google_checkbox.pack(side="left", padx=(0, 100))
        self.google_checkbox.select()

        self.bing_checkbox = ctk.CTkCheckBox(gb_frame, text="Bing", width=50, corner_radius=36)
        self.bing_checkbox.pack(side="right")
        self.bing_checkbox.select()

        # Filter Checkbox
        self.filter_checkbox = ctk.CTkCheckBox(settingsbar, text="Filter", width=50, command=self.update_entries)
        self.filter_checkbox.grid(sticky="n")

        # Resolution Entry Fields
        res_frame = ctk.CTkFrame(settingsbar, fg_color="transparent")
        res_frame.grid(pady=(10, 40), padx=20, sticky="nsew")
        self.height_entry = ctk.CTkEntry(res_frame, width=50, placeholder_text="height")
        self.height_entry.pack(side="left", padx=(0, 100))
        self.width_entry = ctk.CTkEntry(res_frame, width=50, placeholder_text="width")
        self.width_entry.pack(side="right")
        self.update_entries()

    def update_entries(self) -> None:
        """Enable or disable resolution entry fields based on filter checkbox."""
        for entry in (self.height_entry, self.width_entry):
            entry.configure(state=["disabled", "normal"][self.filter_checkbox.get()], placeholder_text=entry._placeholder_text)

    def download(self):
        """Handle the download process based on user input."""
        query = self.query_entry.get()
        height, width = (int(self.height_entry.get()), int(self.width_entry.get())) if self.filter_checkbox.get() else (None, None)

        for engine in ["google", "bing"]:
            if getattr(self, f"{engine}_checkbox").get():
                self.download_images(query, engine)
                if height and width:
                    self.filter_images(engine, height, width)

        CTkMessagebox(title="Images downloader", message="Images have been downloaded!", option_1="Ok")

    def download_images(self, query, engine):
        """Download images using the specified search engine."""
        download_dir = self.downloads_dir / engine
        download_dir.mkdir(exist_ok=True)

        crawler_cls = GoogleImageCrawler if engine == "google" else BingImageCrawler
        crawler = crawler_cls(feeder_threads=200, parser_threads=200, downloader_threads=200,
                              storage={"root_dir": download_dir})
        crawler.crawl(keyword=query, max_num=999)

    def filter_images(self, engine, height, width):
        """Filter images based on given resolution."""
        download_dir = self.downloads_dir / engine
        given_res_dir = self.downloads_dir / "Given resolution"
        similar_res_dir = self.downloads_dir / "Similar resolution"

        # Create directories for filtered images
        given_res_dir.mkdir(exist_ok=True)
        similar_res_dir.mkdir(exist_ok=True)

        for file in download_dir.glob("*.*"):
            if file.suffix not in (".png", ".jpg", ".jpeg"):
                continue
            
            img = Image.open(file)
            dst = (given_res_dir if img.size == (height, width)
                   else similar_res_dir if img.size[0] / img.size[1] == height / width else None)
            img.close()
            
            if dst:
                shutil.move(file, dst / f"{uuid.uuid4()}.png")
            else:
                file.unlink()

        download_dir.rmdir()


if __name__ == "__main__":
    app = App()
    app.mainloop()
