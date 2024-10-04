import logging
import os

import customtkinter as ctk

from crawlers import download_images, filter_images

# Basic configuring
__version__ = "2.0.0"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ctk.set_default_color_theme("theme.json")
PADX = 20


# App config
window = ctk.CTk()
window.title = "Images Downloader"

infobar = ctk.CTkFrame(window)
infobar.grid(row=0, column=0, padx=PADX, pady=20, columnspan=2)

downloadbar = ctk.CTkFrame(window)
downloadbar.grid(row=1, column=0, padx=PADX, pady=10, sticky="nsew")

filterbar = ctk.CTkFrame(window)
filterbar.grid(row=1, column=1, padx=PADX, pady=10, sticky="nsew")


# Infobar
ctk.CTkLabel(infobar, text=f"Images Downloader {__version__}", font=ctk.CTkFont(size=20, weight="bold")).grid(padx=PADX, pady=(10, 0))
ctk.CTkLabel(infobar, text="© anekobtw, 2024\ntheme by avalon60").grid(padx=PADX, pady=(5, 10))


# Download bar
query_entry = ctk.CTkEntry(downloadbar, placeholder_text="Query")
query_entry.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=2)

google_checkbox = ctk.CTkCheckBox(downloadbar, text="Google", corner_radius=36)
google_checkbox.grid(row=1, column=0, sticky="w", padx=PADX, pady=(10, 20))
google_checkbox.select()

pinterest_checkbox = ctk.CTkCheckBox(downloadbar, text="Pinterest", width=50, corner_radius=36)
pinterest_checkbox.grid(row=1, column=1, sticky="w", padx=PADX, pady=(10, 20))
pinterest_checkbox.select()

ctk.CTkButton(
    downloadbar,
    text="Download",
    command=lambda: download_images(
        query=query_entry.get(),
        google=google_checkbox.get(),
        pinterest=pinterest_checkbox.get(),
    ),
).grid(row=2, column=0, pady=10, columnspan=2)

ctk.CTkButton(downloadbar, text="Open Downloads Folder", command=lambda: os.startfile("downloads")).grid(row=3, column=0, pady=(0, 10), columnspan=2)


# Filter bar
height_entry = ctk.CTkEntry(filterbar, width=50, placeholder_text="height")
height_entry.grid(row=0, column=0, sticky="w", padx=PADX, pady=10)

width_entry = ctk.CTkEntry(filterbar, width=50, placeholder_text="width")
width_entry.grid(row=0, column=1, sticky="w", padx=PADX, pady=10)

rembg_checkbox = ctk.CTkCheckBox(filterbar, text="Remove background", width=50, corner_radius=36)
rembg_checkbox.grid(row=1, column=0, sticky="w", padx=PADX, pady=(5, 10), columnspan=2)

ctk.CTkButton(
    filterbar,
    text="Filter",
    command=lambda: filter_images(
        height=height_entry.get(),
        width=width_entry.get(),
        remove_bg=rembg_checkbox.get(),
    ),
).grid(row=2, column=0, pady=(53, 0), columnspan=2)


if __name__ == "__main__":
    window.mainloop()
