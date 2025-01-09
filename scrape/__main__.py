from .genius import GeniusScraper
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["settings.yaml"],
)

if __name__ == "__main__":
    genius = GeniusScraper(
        token=settings.scrape.genius.token,
        rules=settings.scrape.genius.rules,
    )
    result = genius.scrape()
    if result:
        genius.save_to_disk(result, output_dir=settings.scrape.output_dir)
    else:
        print("Scraping failed or no data found.")
