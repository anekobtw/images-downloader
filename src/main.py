import logging
import os

import customtkinter as ctk

from src.utils import *

# Basic configuring
__version__ = "1.2.1"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ctk.set_default_color_theme("theme.json")
PADX = 20


# App config
app = ctk.CTk()
app.title = "Images Downloader"

infobar = ctk.CTkFrame(app)
infobar.grid(row=0, column=0, padx=PADX, pady=20, sticky="nsew")

settingsbar = ctk.CTkFrame(app)
settingsbar.grid(row=0, column=1, padx=PADX, pady=20, sticky="ew")

gb_frame = ctk.CTkFrame(settingsbar, fg_color="transparent")
gb_frame.grid(row=1, pady=10, padx=PADX, sticky="nsew")

res_frame = ctk.CTkFrame(settingsbar, fg_color="transparent")
res_frame.grid(row=3, pady=10, padx=PADX, sticky="nsew")

font = ctk.CTkFont(size=20, weight="bold")


# Infobar
ctk.CTkLabel(
    infobar,
    text=f"Images Downloader {__version__}",
    font=font
).grid(padx=PADX, pady=(10, 0))

ctk.CTkLabel(
    infobar,
    text="© anekobtw, 2024\ntheme by avalon60"
).grid(padx=PADX, pady=(5, 10))

query_entry = ctk.CTkEntry(infobar, placeholder_text="Query")
query_entry.grid(padx=10, pady=(20, 0))

ctk.CTkButton(
    infobar,
    text="Download",
    command=lambda: download(query_entry.get(), height_entry.get(), width_entry.get(), rembg_checkbox.get(), google_checkbox.get(), bing_checkbox.get()),
).grid(padx=10, pady=(10, 20))

ctk.CTkButton(
    infobar,
    text="Open Downloads Folder",
    command=lambda: os.startfile(DOWNLOADS)
).grid(pady=(5, 13))


# Settings bar
ctk.CTkLabel(
    settingsbar,
    text="Settings",
    font=font
).grid(row=0, pady=(10, 0))

google_checkbox = ctk.CTkCheckBox(gb_frame, text="Google", corner_radius=36)
google_checkbox.pack(side="left", padx=(0, 100))
google_checkbox.select()

bing_checkbox = ctk.CTkCheckBox(gb_frame, text="Bing", width=50, corner_radius=36)
bing_checkbox.pack(side="right")
bing_checkbox.select()

filter_checkbox = ctk.CTkCheckBox(
    res_frame,
    text="Filter",
    width=50,
    command=lambda: update_entries(filter_checkbox, height_entry, width_entry)
)
filter_checkbox.grid(row=0, column=0, padx=(0, PADX))

height_entry = ctk.CTkEntry(
    res_frame,
    width=50,
    placeholder_text="height"
)
height_entry.configure(state="disabled")
height_entry.grid(row=0, column=1, padx=PADX)

width_entry = ctk.CTkEntry(
    res_frame,
    width=50,
    placeholder_text="width"
)
width_entry.configure(state="disabled")
width_entry.grid(row=0, column=2, padx=(PADX, 0))

rembg_checkbox = ctk.CTkCheckBox(settingsbar, text="Remove BG", width=50, corner_radius=36)
rembg_checkbox.grid(row=4, pady=(0, 20))

if __name__ == "__main__":
    app.mainloop()