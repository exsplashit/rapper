# Welcome to Rapper

## Local development

```
python3 -m venv venv
pip3 install -r requirements.txt
```

## Scrape lyrics from Genius

For scraping fill the `rules` field in `config.yaml`. At the moment the structure has only 2 fields

To scrape data run:
`python3 -m scrape`


## Load lyrics to vector database

Run:
`python3 load_json_to_db.py`

## UI

UI component implemented using Streamlit. **not tested**
`streamlit ui/app.py`
