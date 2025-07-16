# from data_extraction.api_extract import PokeAPI
from app_folder.source_app import PokedexExplorer

# Extract, drop, and re-create tables
# API = PokeAPI()
# API.extract_data()


# Launch App
app = PokedexExplorer()
app.display()