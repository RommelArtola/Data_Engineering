

# POKEMON_BASE_DROP_SCRIPT = """
#     DROP TABLE IF EXISTS pokemon_ids
# """
# POKEMON_STATS_TABLE_DROP_SCRIPT = """
#     DROP TABLE IF EXISTS stats
# """
# POKEMON_TYPES_DB_DROP_SCRIPT = """
#     DROP TABLE IF EXSITS types
# """


POKEMON_BASE_TABLE_CREATION_SCRIPT = """
    CREATE TABLE IF NOT EXISTS pokemon_ids (
        --DATABASE_ID     SERIAL      PRIMARY KEY,
        POKEMON_ID      INTEGER         PRIMARY KEY,
        NAME            VARCHAR(255)    NOT NULL,
        IMG_URL         VARCHAR(600),
        UPLOAD_DATE     DATE            NOT NULL          
    );
"""


POKEMON_STATS_TABLE_CREATION_SCRIPT = """
    CREATE TABLE IF NOT EXISTS stats (
        POKEMON_ID          INTEGER,
        STAT_NAME   VARCHAR(255),
        STAT_VALUE  INTEGER,
        UPLOAD_DATE     DATE            NOT NULL                
    );
"""

POKEMON_TYPES_TABLE_CREATION_SCRIPT = """
    CREATE TABLE IF NOT EXISTS types (
        POKEMON_ID      INTEGER         NOT NULL,
        TYPE    VARCHAR(24)     NOT NULL,
        UPLOAD_DATE     DATE            NOT NULL
    );

"""


POKEMON_LOCATIONS_TABLE_CREATION_SCRIPT = """
    CREATE TABLE IF NOT EXISTS locations (
        POKEMON_ID      INTEGER         NOT NULL,
        LOCATION        VARCHAR(255),
        UPLOAD_DATE     DATE            NOT NULL            
    );
"""

POKEMON_CHARACTERISTICS_TABLE_CREATION_SCRIPT = """
    CREATE TABLE IF NOT EXISTS characteristics (
        POKEMON_ID      INTEGER         NOT NULL,
        HEIGHT          INTEGER                 ,
        WEIGHT          INTEGER,
        UPLOAD_DATE     DATE            NOT NULL
    );
"""