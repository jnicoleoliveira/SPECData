
class Composition:

    def __init__(self, composition_string):

        self.string = composition_string
        self.elements = []

        self.__get_elements_from_string()

    def __get_elements_from_string(self):

        array = self.string.split()

        for a in array:
            new_element = Element.string_to_element(a)
            self.elements.append(new_element)

class Element:

    def __init__(self, symbol, count):
        self.symbol = symbol
        self.count = count

    def __str__(self):
        return self.symbol + "(" + str(self.count) + ")"

    @staticmethod
    def string_to_element(string):
        """
        Creates an element from a string of the form,
        (symbol(count))
        :param string:
        :return:
        """
        b = string.replace(')', ' ').replace('(', ' ').split()
        element = Element(b[0], int(b[1]))
        return element

    @staticmethod
    def is_element_string(string):
        """
        Determines if the string is the correct format
        :return:
        """

        try:
            b = string.replace(')', ' ').replace('(', ' ').split()
            if b[0] is string and b[1] is int and len(b) == 2:
                return True
            else:
                return False
        except:
            return False


def main():
    c = Composition("Ha(2) O(2)")
    print c.elements[0]
    print c.elements[1]

if __name__ == '__main__':
    main()