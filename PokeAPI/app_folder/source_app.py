import streamlit as st
import numpy as np
from app_folder.data_handler import User_Selections


import streamlit as st
import numpy as np
from app_folder.data_handler import User_Selections


class PokedexExplorer:
    def __init__(self):
        self.user = User_Selections()

    def display(self):
        tab1, tab2 = st.tabs(["🔍 Explorer", "📒 About"])

        with tab1:
            self.display_explorer()

        with tab2:
            self.display_notes()


    def display_explorer(self):
        st.title("Pokédex Explorer")

        # Load filter options
        min_height, max_height, min_weight, max_weight = self.user.get_minmax_height_weight()
        min_attack, max_attack, min_defense, max_defense, min_hp, max_hp, \
            min_spec_attack, max_spec_attack, min_spec_defense, max_spec_defense, \
            min_speed, max_speed = self.user.get_minmax_stats()

        locations_base = self.user.get_unique_locations_list()
        types_base = self.user.get_unique_types_list()

        # Filters
        with st.expander("Filter Pokémon", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                hp_range = st.slider("HP", min_hp, max_hp, (min_hp, max_hp))
                attack_range = st.slider("Attack", min_attack, max_attack, (min_attack, max_attack))
                defense_range = st.slider("Defense", min_defense, max_defense, (min_defense, max_defense))
                sp_attack_range = st.slider("Special Attack", min_spec_attack, max_spec_attack, (min_spec_attack, max_spec_attack))
                sp_defense_range = st.slider("Special Defense", min_spec_defense, max_spec_defense, (min_spec_defense, max_spec_defense))
                speed_range = st.slider("Speed", min_speed, max_speed, (min_speed, max_speed))
            with col2:
                weight_range = st.slider("Weight", min_weight, max_weight, (min_weight, max_weight))
                height_range = st.slider("Height", min_height, max_height, (min_height, max_height))
                locations = st.multiselect("Location", locations_base, default=locations_base)
                types = st.multiselect("Type", types_base, default=types_base)

        # Apply Filters
        id_characteristics = self.user.characteristics[
            (self.user.characteristics['weight'].between(*weight_range)) &
            (self.user.characteristics['height'].between(*height_range))
        ]['pokemon_id'].unique()

        id_stats = self.user.stats[
            (self.user.stats['Attack'].between(*attack_range)) &
            (self.user.stats['Defense'].between(*defense_range)) &
            (self.user.stats['Hp'].between(*hp_range)) &
            (self.user.stats['Special-Attack'].between(*sp_attack_range)) &
            (self.user.stats['Special-Defense'].between(*sp_defense_range)) &
            (self.user.stats['Speed'].between(*speed_range))
        ]['pokemon_id'].unique()

        ids = np.unique(np.concatenate((id_characteristics, id_stats)))
        filtered = self.user.pokemon_ids[self.user.pokemon_ids['pokemon_id'].isin(ids)]

        if locations:
            loc_ids = self.user.locations[self.user.locations['location'].isin(locations)]['pokemon_id'].unique()
            filtered = filtered[filtered['pokemon_id'].isin(loc_ids)]

        if types:
            type_ids = self.user.types[self.user.types['type'].isin(types)]['pokemon_id'].unique()
            filtered = filtered[filtered['pokemon_id'].isin(type_ids)]

        if filtered.empty:
            st.warning("No Pokémon match the selected filters.")
            return

        # Display Selected Pokémon
        names = filtered['name'].tolist()
        selected_name = st.selectbox("Select a Pokémon That Fit Your Filters", names)
        selected_row = filtered[filtered['name'] == selected_name].iloc[0]

        img_col = st.columns([1, 2, 1])[1]
        with img_col:
            st.image(selected_row['img_url'], use_container_width=True)
        st.markdown(
            f"<h3 style='text-align: center;'>{selected_row['name'].capitalize()}</h3>",
            unsafe_allow_html=True
        )

    def display_notes(self):
        st.title("📒 About This App")
        st.caption("Developer Notes and Documentation")

        st.markdown(
            """
            ## Welcome to the Pokédex Explorer

            This app was built by **Rommel Artola** as a fun and interactive way to explore Pokémon data, 
            and as a way to showcase some Data Engineering principles on the backend.

            ### Features:
            - Filter Pokémon by **stats**, **height**, **weight**, **type**, and **location**
            - View official artwork and names

            ### Data Source:
            - All data comes from [PokeAPI](https://pokeapi.co/), an open Pokémon RESTful API.
            - It has some minor transformations and is then uploaded to a PostgreSQL database hosted on Supabase
            - The data is then queried and has some additional pivoting to get row-wise unique values
            - The data is then filtered given the selected filters, and the image is then shown.

            ---
            """,
            unsafe_allow_html=True
        )


                                
# test = PokedexExplorer()
# test.display()