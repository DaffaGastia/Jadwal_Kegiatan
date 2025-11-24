import json
from models.kegiatan import Kegiatan

class Serializer:
    @staticmethod
    def load_from_json(filepath, btree):
        try:
            with open(filepath, 'r') as file:
                data_list = json.load(file)
            for data in data_list:
                kegiatan = Kegiatan.from_dict(data)
                key = kegiatan.get_key()
                btree.insert(key, kegiatan)
        except FileNotFoundError:
            with open(filepath, 'w') as file:
                json.dump([], file)
        except json.JSONDecodeError:
            with open(filepath, 'w') as file:
                json.dump([], file)

    @staticmethod
    def save_to_json(filepath, btree):
        traversal = btree.traverse()
        data_list = []
        for key, kegiatan in traversal:
            data_list.append(kegiatan.to_dict())
        with open(filepath, 'w') as file:
            json.dump(data_list, file, indent=4)
