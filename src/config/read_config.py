import yaml
import codecs

class Config:
    _config = {}
    def __init__(self, config_file_path) -> None:
        with codecs.open(config_path, 'r', 'utf-8') as file:
            self.config = yaml.safe_load(file)

    def get_paths(self):
        return self.config['paths']

    def get_exclude_lines(self):
        return self.config['excludeLines']

    def get_prefix_name_case(self):
        return self.config['prefixNameCase']

    def get_json_indent(self):
        return self.config['jsonIndent']

    def get_use_oj_bundle(self):
        return self.config['useOjBundle']
