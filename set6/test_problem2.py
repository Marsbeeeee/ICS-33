import unittest
from problem2 import HashableByAttributes, Person, Product


class TestHashableByAttributes(unittest.TestCase):

    def test_person_hashability(self):
        person1 = Person("Alice", 30, "alice@example.com")
        person2 = Person("Alice", 30, "alice@example.com")
        person3 = Person("Bob", 25, "bob@example.com")

        self.assertEqual(hash(person1), hash(person2))

        self.assertNotEqual(hash(person1), hash(person3))

        self.assertEqual(person1, person2)

        self.assertNotEqual(person1, person3)

    def test_person_with_different_non_hashable_attrs(self):
        person1 = Person("Charlie", 40, "charlie@example.com")
        person1.friends.append("David")

        person2 = Person("Charlie", 40, "charlie@example.com")

        self.assertEqual(hash(person1), hash(person2))
        self.assertEqual(person1, person2)

    def test_product_hashability(self):
        product1 = Product(1, "Laptop", 999.99, ("electronics", "tech"))
        product2 = Product(1, "Laptop", 999.99, ("electronics", "tech"))
        product3 = Product(2, "Mouse", 29.99, ("electronics", "accessories"))

        self.assertEqual(hash(product1), hash(product2))

        self.assertNotEqual(hash(product1), hash(product3))

        self.assertEqual(product1, product2)
        self.assertNotEqual(product1, product3)

    def test_product_with_non_hashable_tags(self):
        product1 = Product(1, "Laptop", 999.99, ["electronics", "tech"])
        product2 = Product(1, "Laptop", 999.99, ["electronics", "tech"])

        self.assertEqual(hash(product1), hash(product2))
        self.assertEqual(product1, product2)

    def test_hashable_in_sets(self):
        person_set = set()

        p1 = Person("Alice", 30, "alice@example.com")
        p2 = Person("Alice", 30, "alice@example.com")
        p3 = Person("Bob", 25, "bob@example.com")

        person_set.add(p1)
        person_set.add(p2)
        person_set.add(p3)

        self.assertEqual(len(person_set), 2)

        person_dict = {}
        person_dict[p1] = "first alice"
        person_dict[p2] = "second alice"
        person_dict[p3] = "bob"

        self.assertEqual(len(person_dict), 2)
        self.assertEqual(person_dict[p1], "second alice")

    def test_different_types_not_equal(self):
        person = Person("Test", 100, "test@example.com")


        class OtherPerson(HashableByAttributes):
            def __init__(self, name, age, email):
                self.name = name
                self.age = age
                self.email = email


        other_person = OtherPerson("Test", 100, "test@example.com")

        self.assertNotEqual(person, other_person)

    def test_inheritance_chain(self):

        class Employee(Person):
            def __init__(self, name, age, email, employee_id):
                super().__init__(name, age, email)
                self.employee_id = employee_id


        emp1 = Employee("Eve", 35, "eve@company.com", 101)
        emp2 = Employee("Eve", 35, "eve@company.com", 101)
        emp3 = Employee("Eve", 35, "eve@company.com", 102)

        self.assertEqual(emp1, emp2)
        self.assertNotEqual(emp1, emp3)
        self.assertEqual(hash(emp1), hash(emp2))
        self.assertNotEqual(hash(emp1), hash(emp3))


if __name__ == '__main__':
    unittest.main()