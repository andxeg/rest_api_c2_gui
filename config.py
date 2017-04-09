import os
import json


class Config(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.config_dict = None

    def read_config(self):
        if self.config_dict is not None:
            return

        if not os.access(self.file_path, os.R_OK):
            raise Exception("file '%s' not found or can not read"
                            % self.file_path)

        try:
            with open(self.file_path, "r") as config_file:
                config = config_file.read()
        except IOError as e:
            raise Exception("error '%s' in open file '%s'"
                            % (e, self.file_path))

        try:
            self.config_dict = json.loads(config)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception("error '%s' while convert '%s' to json"
                            % (e, self.file_path,))

        print json.dumps(self.config_dict, indent=4, sort_keys=True)

    def get_full_config(self):
        self.read_config()
        return self.config_dict

    def get_sub_config_by_key(self, key):
        self.read_config()

        try:
            sub_config = self.config_dict[key]
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception("error '%s' when read config" % e)

        return sub_config


