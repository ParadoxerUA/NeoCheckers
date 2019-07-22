colors = enumerate(['black', 'white'])
class Checker():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if y < 3:
            self.colour = 'white'
        else:
            self.colour = 'black'
        self.area_of_affect = 1



