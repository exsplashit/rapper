from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from lyricsgenius import Genius
from .scraper import BaseScraper


class ScrapeRule:

    def __init__(self, artist: str, max_songs: int) -> None:
        self.artist = artist
        self.max_songs = max_songs

    def __repr__(self):
        return f"ScrapeRule(artist={self.artist}, max_songs={self.max_songs})"


class GeniusScraper(BaseScraper):
    client: Genius
    rules: List[ScrapeRule]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client = Genius(self.config.token)
        self.rules = [
            ScrapeRule(artist=rule["artist"], max_songs=rule["max_songs"])
            for rule in self.config.rules
        ]

    def scrape_rule(self, rule: ScrapeRule):
        """Scrape a single artist based on a rule."""
        print(f"Scraping artist: {rule.artist} (max {rule.max_songs} songs)")
        try:
            artist = self.client.search_artist(
                rule.artist, max_songs=rule.max_songs)
            if not artist:
                print(f"No data found for artist: {rule.artist}")
                return []

            songs_data = []
            for song in artist.songs:
                song_data = {
                    "artist": artist.name,
                    "song_name": song.title,
                    "year": song._body.get("release-date")
                    or "",  # Assuming year is available
                    "metadata": {
                        "pageviews": song.stats.pageviews or "",
                    },
                    "lyrics": song.lyrics,
                }
                songs_data.append(song_data)

            return songs_data

        except Exception as e:
            print(f"Error while scraping {rule.artist}: {e}")
            return []

    def scrape(self):
        """Scrape data for all rules in parallel."""
        all_songs_data = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit each rule to the executor
            futures = {
                executor.submit(self.scrape_rule, rule): rule for rule in self.rules
            }
            for future in as_completed(futures):
                rule = futures[future]
                try:
                    result = future.result()
                    all_songs_data.extend(result)
                except Exception as e:
                    print(f"Error while processing rule {rule}: {e}")

        return all_songs_data
