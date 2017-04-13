class Theme:
    def __init__(self, name):
        self.name = name
        self.light_background = "white"
        self.dark_background = "gray"
        self.color = "darkGray"

    @staticmethod
    def generate_stylesheet(**kwargs):

        if kwargs is not None:
            s = ""
            for key, value in kwargs.iteritems():
                s += str(key) + ": " + str(value) + ";"
        else:
            return ValueError

        return s
