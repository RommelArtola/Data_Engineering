from configparser import ConfigParser

def config_parse(file_name:str, section_name:str):
    parser = ConfigParser()
    parser.read(file_name)

    param_kwargs = {}

    if parser.has_section(section=section_name):
        params = parser.items(section_name)
        for param_name, param_value in params:
            param_kwargs[param_name] = param_value
    else:
        raise Exception(
            'Section {0} is not found in {1} file'.format(section_name, file_name)
        )
    
    return param_kwargs
