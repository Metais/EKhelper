import unicodedata

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        image_path_name = self.remove_accents(name)
        image_path_name = image_path_name.lower().replace(' ', '-').replace("'", "")
        self.image_path = f'images/items/{image_path_name}.gif'

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

    def __str__(self):
        return f'{self.name}: {self.description}'

    def __repr__(self):
        return self.name