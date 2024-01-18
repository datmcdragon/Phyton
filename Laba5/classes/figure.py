""" figure file"""
from abc import abstractmethod,ABC

class Figure(ABC):
    """ Class Figure for generating figure"""
    def __init__(self, center):
        self.center = center

    def set_color(self, color):
        """Set color """
        self.color = color

    @abstractmethod
    def project_to_2d(self):
        """ Method for 2d generating"""

    @abstractmethod
    def draw(self):
        """ Method for drawing"""
