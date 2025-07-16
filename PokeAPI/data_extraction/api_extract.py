import requests
from datetime import datetime


from data_extraction.utils.utils import API_BASE_URL

from shared_utils.database import PostgreSQL
from data_extraction.utils.str_scripts import (POKEMON_TYPES_TABLE_CREATION_SCRIPT, 
                               POKEMON_BASE_TABLE_CREATION_SCRIPT, 
                               POKEMON_STATS_TABLE_CREATION_SCRIPT,
                               POKEMON_LOCATIONS_TABLE_CREATION_SCRIPT,
                               POKEMON_CHARACTERISTICS_TABLE_CREATION_SCRIPT)


class PokeAPI:
    def __init__(self):
        
        # Main/Initial Response:
        root_response = requests.get(API_BASE_URL)
        root_endpoint = root_response.json()

        self.pokemons_endpoint = root_endpoint.get('pokemon')
        

        # Database Variables
        self.PQL_admin = PostgreSQL(section_name='admin')
        self.PQL_user = PostgreSQL(section_name='user')

    def _format_url_string(self, url_string):
        #type fix for manual/hardcoded
        if url_string[-1]  ==  '/':
            url_string = url_string[:-1]
            if url_string[-3:] == '907':
                url_string += '/'
        
        return url_string
    
    def _clear_and_create_tables(self):
        self.PQL_admin.drop_table("pokemon_ids") #first drop
        self.PQL_admin.drop_table("stats")
        self.PQL_admin.drop_table("types")
        self.PQL_admin.drop_table("locations")
        self.PQL_admin.drop_table('characteristics')

        self.PQL_admin.create_table(POKEMON_BASE_TABLE_CREATION_SCRIPT) #then create
        self.PQL_admin.create_table(POKEMON_STATS_TABLE_CREATION_SCRIPT)
        self.PQL_admin.create_table(POKEMON_TYPES_TABLE_CREATION_SCRIPT)
        self.PQL_admin.create_table(POKEMON_LOCATIONS_TABLE_CREATION_SCRIPT)
        self.PQL_admin.create_table(POKEMON_CHARACTERISTICS_TABLE_CREATION_SCRIPT)

    
    def _parse_through_pokemon_specifics(self, pokemon_row):
        pokemon_name = pokemon_row.get('name').title()
        pokemon_url = pokemon_row.get('url')

        pokemon_cleaned_url = self._format_url_string(pokemon_url)
        pokemon_specific_response = requests.get(pokemon_cleaned_url)
        pokemon_specific_data = pokemon_specific_response.json()

        pokemon_id = pokemon_specific_data.get('id')
        pokemon_img_url = pokemon_specific_data.get('sprites').get('other').get('official-artwork').get('front_default')

        return pokemon_id, pokemon_name, pokemon_img_url, pokemon_specific_data
    

    def _parse_through_pokemon_stats(self, pokemon_specific_data, upload_date):
        pokemon_stats = []

        pokemon_id = pokemon_specific_data.get('id')
        for stat_row in pokemon_specific_data.get('stats'):
            stat_value = stat_row.get('base_stat')
            stat_name = stat_row.get('stat').get('name').title()

            pokemon_stats.append( (pokemon_id, stat_name, stat_value, upload_date ) )

        return pokemon_stats

    def _parse_through_pokemon_types(self, pokemon_specific_data, upload_date):
        types_ret = []
        pokemon_id = pokemon_specific_data.get('id')
        for types_row in pokemon_specific_data.get('types'):
            pokemon_type = types_row.get('type').get('name').title()
            types_ret.append( (pokemon_id, pokemon_type, upload_date) )
        
        return types_ret
    
    def _parse_through_pokemon_locations(self, pokemon_specific_data, upload_date):
        locations_data = []

        pokemon_id = pokemon_specific_data.get('id')
        
        loc_url = pokemon_specific_data.get('location_area_encounters')
        locations = requests.get(loc_url).json()

        if locations != []:
            for locs in locations:
                loc_name = locs.get('location_area').get('name').title()
                cleaned_name = " ".join(loc_name.split('-')).title()
                locations_data.append( (pokemon_id, cleaned_name, upload_date) )
        else:
            locations_data.append( (pokemon_id, "No Location Reported", upload_date) )

        return locations_data


    def _parse_through_pokemon_characteristics(self, pokemon_specific_data, upload_date):
        characteristics = []
        
        pokemon_id = pokemon_specific_data.get('id')
        weight = pokemon_specific_data.get('weight')
        height = pokemon_specific_data.get('height')
        # default_pokemon = pokemon_specific_data['is_default']

        characteristics.append( (pokemon_id, weight, height, upload_date) )

        return characteristics


    def extract_data(self):
        self._clear_and_create_tables()
        updated_date = datetime.today().date()

        while self.pokemons_endpoint:
            pokemon_basics_data             = []
            pokemon_stats_data              = []
            pokemon_types_data              = []
            pokemon_locations_data          = []
            pokemon_characteristics_data    = []


            pokemons_response = requests.get(self.pokemons_endpoint)
            pokemons_data = pokemons_response.json()

            iter_results = pokemons_data.get('results')

            for pokemon_row in iter_results: #at this level we just have name and url
                id, name, img_url, specific_data = self._parse_through_pokemon_specifics(pokemon_row)
                stats = self._parse_through_pokemon_stats(pokemon_specific_data=specific_data, upload_date=updated_date)
                types = self._parse_through_pokemon_types(pokemon_specific_data=specific_data, upload_date=updated_date)
                locations = self._parse_through_pokemon_locations(pokemon_specific_data=specific_data, upload_date=updated_date)
                characteristics = self._parse_through_pokemon_characteristics(pokemon_specific_data=specific_data, upload_date=updated_date)


                pokemon_basics_data.append( (id, name, img_url, updated_date) ) #append a set
                pokemon_stats_data.extend( stats )
                pokemon_types_data.extend( types )
                pokemon_locations_data.extend( locations )
                pokemon_characteristics_data.extend( characteristics )

            print('Inserting Records')
            self.PQL_admin.insert_many("INSERT INTO pokemon_ids (POKEMON_ID, NAME, IMG_URL, UPLOAD_DATE) VALUES (%s, %s, %s, %s)",
                                    params_list=pokemon_basics_data)
            self.PQL_admin.insert_many("INSERT INTO stats (POKEMON_ID, STAT_NAME, STAT_VALUE, UPLOAD_DATE) VALUES (%s, %s, %s, %s)",
                                 params_list=pokemon_stats_data)
            self.PQL_admin.insert_many("INSERT INTO types (POKEMON_ID, TYPE, UPLOAD_DATE) VALUES (%s, %s, %s)",
                                 params_list=pokemon_types_data)
            self.PQL_admin.insert_many("INSERT INTO locations (POKEMON_ID, LOCATION, UPLOAD_DATE) VALUES (%s, %s, %s)",
                                 params_list=pokemon_locations_data)
            self.PQL_admin.insert_many("INSERT INTO characteristics (POKEMON_ID, HEIGHT, WEIGHT, UPLOAD_DATE) VALUES (%s, %s, %s, %s)",
                                 params_list=pokemon_characteristics_data)
            
            ### Update Pokemon Name and ID Parent Table
            self.pokemons_endpoint = pokemons_data.get('next')



# API = PokeAPI()
# API.extract_data()