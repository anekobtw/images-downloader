import logging
import os
import shutil
import uuid
from pathlib import Path

import customtkinter as ctk
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
from PIL import Image

__version__ = "1.2.0"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Images Downloader")
        self.draw_infobar()
        self.draw_settingsbar()

    def draw_infobar(self) -> None:
        sidebar = ctk.CTkFrame(self, width=140)
        sidebar.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        ctk.CTkLabel(sidebar, text=f"Images Downloader {__version__}", font=ctk.CTkFont(size=20, weight="bold")).grid(padx=20, pady=(10, 0))
        ctk.CTkLabel(sidebar, text="© anekobtw, 2024").grid(padx=10, pady=(5, 10))

        self.query_entry = ctk.CTkEntry(sidebar, placeholder_text="Query")
        self.query_entry.grid(padx=10, pady=(20, 0))
        ctk.CTkButton(sidebar, text="Download", command=self.download).grid(padx=10, pady=(10, 20))

        self.appearance = ctk.CTkOptionMenu(sidebar, values=["Light", "Dark", "System"], command=lambda x: ctk.set_appearance_mode(x))
        self.appearance.set("System")
        self.appearance.grid(padx=10, pady=10)

    def draw_settingsbar(self) -> None:
        settingsbar = ctk.CTkFrame(self)
        settingsbar.grid(row=0, column=1, pady=20, padx=20, sticky="nsew")

        self.filter_checkbox = ctk.CTkCheckBox(settingsbar, text="Filter", command=lambda: [state.configure(state=["disabled", "normal"][self.filter_checkbox.get()], placeholder_text=text) for state, text in [(self.res_entry1, "height"), (self.res_entry2, "width")]])
        self.filter_checkbox.grid(row=1, column=0, padx=20, pady=10)
        res_frame = ctk.CTkFrame(settingsbar, fg_color="transparent")
        res_frame.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        self.res_entry1 = ctk.CTkEntry(res_frame, state="disabled", width=50)
        self.res_entry1.pack(side="left", padx=(0, 40))
        self.res_entry2 = ctk.CTkEntry(res_frame, state="disabled", width=50)
        self.res_entry2.pack(side="right")

    def download(self):
        self.download_images(self.query_entry.get())

        if self.filter_checkbox.get():
            height, width = int(self.res_entry1.get()), int(self.res_entry2.get())
            for src in ("google", "bing"):
                self.filter_images(src, height, width)

    def download_images(self, query):
        for src, Crawler in zip(["google", "bing"], [GoogleImageCrawler, BingImageCrawler]):
            crawler = Crawler(feeder_threads=200, parser_threads=200, downloader_threads=200, storage={"root_dir": src})
            crawler.crawl(keyword=query, max_num=999)

    def filter_images(self, directory, height, width):
        Path("Given resolution").mkdir(exist_ok=True)
        Path("Similar resolution").mkdir(exist_ok=True)
        for file in Path(directory).glob("*.*"):
            if file.suffix not in (".png", ".jpg", ".jpeg"):
                continue
            img = Image.open(file)
            dst = Path("Given resolution") if img.size == (height, width) else Path("Similar resolution") if img.size[0] / img.size[1] == height / width else None
            img.close()
            if dst:
                shutil.move(file, dst / f"{uuid.uuid4()}.png")
            else:
                file.unlink()
        Path(directory).rmdir()


if __name__ == "__main__":
    app = App()
    app.mainloop()
