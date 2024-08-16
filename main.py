import logging
import os
import shutil
from pathlib import Path

import customtkinter as ctk
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
from PIL import Image

__version__ = "1.0.1"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Images Downloader")
        self.draw_sidebar()
        self.draw_mainbar()

    def draw_sidebar(self) -> None:
        sidebar_frame = ctk.CTkFrame(self, width=140)
        sidebar_frame.grid(row=0, column=0, rowspan=4, pady=20, padx=20, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(sidebar_frame, text=f"Images Downloader {__version__}", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 0))
        ctk.CTkLabel(sidebar_frame, text="© anekobtw, 2024").grid(row=1, column=0, padx=20, pady=(0, 20))
        ctk.CTkLabel(sidebar_frame, text="Appearance Mode:").grid(row=5, column=0, padx=20)

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"], command=lambda x: ctk.set_appearance_mode(x))
        self.appearance_mode_optionmenu.set("System")
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(0, 10))

    def draw_mainbar(self) -> None:
        mainbar_frame = ctk.CTkFrame(self, width=140)
        mainbar_frame.grid(row=0, column=1, rowspan=4, pady=20, padx=20, sticky="nsew")
        self.query_entry = ctk.CTkEntry(mainbar_frame, placeholder_text="Query")
        self.query_entry.grid(row=0, column=0, padx=20, pady=10)
        states = ["disabled", "normal"]
        self.filter_checkbox = ctk.CTkCheckBox(
            mainbar_frame,
            text="Filter",
            command=lambda: [state.configure(state=states[self.filter_checkbox.get()], placeholder_text=text) for state, text in [(self.res_entry1, "height"), (self.res_entry2, "width")]]
        )
        self.filter_checkbox.grid(row=1, column=0, padx=20, pady=10)

        res_frame = ctk.CTkFrame(mainbar_frame, fg_color="transparent")
        res_frame.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        self.res_entry1 = ctk.CTkEntry(res_frame, state="disabled", width=50)
        self.res_entry1.pack(side="left", padx=(0, 40))
        self.res_entry2 = ctk.CTkEntry(res_frame, state="disabled", width=50)
        self.res_entry2.pack(side="right")

        ctk.CTkButton(mainbar_frame, text="Download", command=self.download).grid(row=3, column=0, padx=20, pady=5)

    def download(self) -> None:
        self.download_images(self.query_entry.get())

        if self.filter_checkbox.get() == 0:
            return
        self.filter_images("google", int(self.res_entry1.get()), int(self.res_entry2.get()))
        self.filter_images("bing", int(self.res_entry1.get()), int(self.res_entry2.get()))

    def download_images(self, query: str) -> None:
        google_crawler = GoogleImageCrawler(
            feeder_threads=200,
            parser_threads=200,
            downloader_threads=200,
            storage={"root_dir": "google"},
        )
        google_crawler.crawl(keyword=query, max_num=999)

        bing_crawler = BingImageCrawler(
            feeder_threads=200,
            parser_threads=200,
            downloader_threads=200,
            storage={"root_dir": "bing"},
        )
        bing_crawler.crawl(keyword=query, max_num=999)

    def filter_images(self, directory: str, height: int, width: int) -> None:
        pics_dir = Path("Given resolution")
        similar_res_dir = Path("Similar resolution")

        pics_dir.mkdir(exist_ok=True)
        similar_res_dir.mkdir(exist_ok=True)

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if not file_path.lower().endswith(("png", "jpg", "jpeg")):
                continue

            try:
                img = Image.open(file_path)
                if img.size == (height, width):
                    dst = pics_dir
                elif img.size[0] / img.size[1] == height / width:
                    dst = similar_res_dir
                else:
                    img.close()
                    Path(file_path).unlink()
                    logging.log(level=logging.INFO, msg=f"Deleted {file_path}")
                    continue

                img.close()
                try:
                    shutil.move(file_path, dst)
                except shutil.Error:
                    name, ext = os.path.splitext(filename)
                    new_file_path = dst / f"{name}_2{ext}"
                    shutil.move(file_path, new_file_path)
                logging.log(level=logging.INFO, msg=f"Moved {file_path} to {dst}")
            except (IOError, OSError) as e:
                print(f"Error processing file {file_path}: {e}")

        if not os.listdir(directory):
            Path(directory).rmdir()


if __name__ == "__main__":
    app = App()
    app.mainloop()