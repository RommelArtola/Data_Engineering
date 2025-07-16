import pandas as pd
import numpy as np
from shared_utils.database import PostgreSQL

pd.options.display.max_columns = None


class User_Selections:
    def __init__(self):
        
        self.PSQL = PostgreSQL(section_name='user')

        pokemon_ids_raw        = pd.DataFrame(self.PSQL.run_query("SELECT * FROM POKEMON_IDS")).drop(columns='upload_date')
        self.characteristics    = pd.DataFrame(self.PSQL.run_query("SELECT * FROM CHARACTERISTICS")).drop(columns='upload_date')
        locations_raw          = pd.DataFrame(self.PSQL.run_query("SELECT * FROM LOCATIONS")).drop(columns='upload_date')
        stats_raw               = pd.DataFrame(self.PSQL.run_query("SELECT * FROM STATS")).drop(columns='upload_date')
        types_raw              = pd.DataFrame(self.PSQL.run_query("SELECT * FROM TYPES")).drop(columns='upload_date')
        

        self.pokemon_ids = (
            pokemon_ids_raw
            .assign(
                name = lambda df: df['name'].str.title()
            )
        )

        self.locations = (
            locations_raw
            .assign(
                location = lambda df: df['location'].str.title()
            )
        )

        self.types = (
            types_raw
            .assign(
                type = lambda df: df['type'].str.title()
            )
        )


        self.stats = (
            stats_raw
            .pivot(index='pokemon_id', columns='stat_name', values='stat_value')
            .reset_index()
            .rename_axis('', axis=1)
        )


    def get_user_pokemon_name_photo(self, pokemon_id):
        """ Returns name and link"""
        df = self.pokemon_ids[self.pokemon_ids['pokemon_id'] == pokemon_id]
        name, url = df['name'].values[0], df['img_url'].values[0]
        return name, url
    
    def get_user_pokemon_types(self, pokemon_id):
        df = self.types[self.types['pokemon_id'] == pokemon_id]
        return df['type'].values[0]
    
    def get_user_pokemon_characteristics(self, pokemon_id):
        """ Returns height and weight of a pokemon"""
        df = self.characteristics[self.characteristics['pokemon_id'] == pokemon_id]
        height = df['height'].values[0]
        weight = df['weight'].values[0]

        return height, weight


    def get_user_pokemon_locations(self, pokemon_id):
        df = self.locations[self.locations['pokemon_id'] == pokemon_id]
        locations = sorted(df['location'].unique().tolist())
        return locations


    def get_user_pokemon_stats(self, pokemon_id):
        """Returns attack, defense, hp, special-attack, special-defense, and speed of a specific pokemon"""
        df = (
            self.stats[self.stats['pokemon_id'] == pokemon_id]
        )
        attack      = df['Attack'].values[0]
        defense     = df['Defense'].values[0]
        hp          = df['Hp'].values[0]
        spec_att    = df['Special-Attack'].values[0]
        spec_def    = df['Special-Defense'].values[0]
        speed       = df['Speed'].values[0]

        return attack, defense, hp, spec_att, spec_def, speed

    def get_minmax_height_weight(self):
        """ Returns min height, max height, min weight, max weight"""
        min_height = self.characteristics['height'].min()
        max_height = self.characteristics['height'].max()

        min_weight = self.characteristics['weight'].min()
        max_weight = self.characteristics['weight'].max()

        return min_height, max_height, min_weight, max_weight


    def get_minmax_stats(self):
        """Returns min max values of attack, defense, hp, special-attack,
        special_defense, speed"""
        cols = ['Attack', 'Defense', 'Hp', 'Special-Attack', 'Special-Defense', 'Speed']

        min_df = self.stats[cols].min()
        max_df = self.stats[cols].max()

        min_attack, max_attack                  = min_df.loc['Attack'], max_df.loc['Attack']
        min_defense, max_defense                = min_df.loc['Defense'], max_df.loc['Attack']
        min_hp, max_hp                          = min_df.loc['Hp'], max_df.loc['Attack']
        min_special_attack, max_special_attack  = min_df.loc['Special-Attack'], max_df.loc['Attack']
        min_special_denfese, max_special_defense    = min_df.loc['Special-Defense'], max_df.loc['Attack']
        min_speed, max_speed                    = min_df.loc['Speed'], max_df.loc['Attack']

        return (min_attack, max_attack, 
                min_defense, max_defense,
                min_hp, max_hp,
                min_special_attack, max_special_attack,
                min_special_denfese, max_special_defense,
                min_speed, max_speed,
        )


    def get_unique_locations_list(self, ):
        locs = sorted(self.locations['location'].unique().tolist())
        return locs
    
    def get_unique_types_list(self):
        types = sorted(self.types['type'].unique().tolist())
        return types
