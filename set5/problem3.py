class Animal:
    def __init__(self, species, habitat):
        self._species = species
        self._habitat = habitat

    def species(self):
        return self._species

    def habitat(self):
        return self._habitat

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self._species == other._species and self._habitat == other._habitat

class Tiger(Animal):
    def __init__(self, species, habitat, stripe_count):
        super().__init__(species, habitat)
        self._stripe_count = stripe_count

    def stripe_count(self):
        return self._stripe_count

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return super().__eq__(other) and self._stripe_count == other._stripe_count
