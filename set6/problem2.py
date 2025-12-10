class HashableByAttributes:
    def __hash__(self):
        hashable_attrs = {}
        for attr_name in dir(self):
            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue

            try:
                attr_value = getattr(self, attr_name)
                hash(attr_value)
                if not callable(attr_value):
                    hashable_attrs[attr_name] = attr_value
            except (TypeError, AttributeError):
                continue

        sorted_attrs = tuple(sorted(hashable_attrs.items()))
        return hash(sorted_attrs)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        self_attrs = self._get_hashable_attributes()
        other_attrs = other._get_hashable_attributes()

        return self_attrs == other_attrs

    def _get_hashable_attributes(self):
        hashable_attrs = {}
        for attr_name in dir(self):
            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue

            try:
                attr_value = getattr(self, attr_name)
                hash(attr_value)
                if not callable(attr_value):
                    hashable_attrs[attr_name] = attr_value
            except (TypeError, AttributeError):
                continue

        return hashable_attrs


class Person(HashableByAttributes):
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        self.friends = []

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


class Product(HashableByAttributes):
    def __init__(self, product_id, name, price, tags):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.tags = tags
        self._internal_data = {"created": "today"}

    def get_description(self):
        return f"{self.name} - ${self.price}"

    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.name}')"