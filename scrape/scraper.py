from abc import ABC, abstractmethod
from typing import List
import os
import json


class Config(object):
    """Configuration for the scraper"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        fields = ", ".join(f"{key}={value!r}" for key,
                           value in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"


class ScrapeRule(object):
    def __init__(self, json_dict):

        for key, value in json_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        name = self.__class__.__name__
        attrs = ", ".join(list(self.__dict__.keys()))
        return "{}({!r})".format(name, attrs)


class BaseScraper(ABC):
    "Base class for all scrapers"

    config: Config

    def __init__(self, **kwargs):
        self.config = Config(**kwargs)

    @abstractmethod
    def scrape(self) -> List:
        "Scrape data from the source based on config rules"

    def save_to_disk(self, song_data, output_dir="output"):
        """Save song data to JSON files, skipping already existing files."""
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        skipped_files = 0
        saved_files = 0

        for song in song_data:
            # Construct the filename
            filename = f"{song['artist']}_{
                song['song_name']}.json".replace(
                " ", "_"
            )
            file_path = os.path.join(output_dir, filename)

            # Skip if the file already exists
            if os.path.exists(file_path):
                print(f"Skipping existing file: {filename}")
                skipped_files += 1
                continue

            # Save the new file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(song, f, ensure_ascii=False, indent=4)
            saved_files += 1

        print(
            f"Saved {saved_files} new song(s) to {output_dir}. Skipped {
                skipped_files} existing file(s)."
        )
