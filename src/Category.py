
from src.Constants import *

class Category:
    """Categories Story Tasks

    Data saved is in the format:
    [Name, RGB*]
    """
    
    OPTION_WIDTH = SCREEN_WIDTH / 2 - 35
    FONT_SIZE = 40
    
    name: str
    color: tuple[int]
    dx: int
    
    def __init__(self, name: str, color: tuple[int] = (180, 180, 180)):
        self.name = name
        self.color = color
        self.highlight = Category.create_highlight(color)
        self.tasks = []
        self.dx = 0
        
    def create_highlight(color: tuple[int]) -> tuple[int]:
        average = sum(color)/3
        return tuple(min(max(6*value - 5*average, 0), 255) for value in color)
    
    def get_x() -> int:
        return 20

    def get_y(index: int) -> int:
        return 20 + index*(1.5*Category.FONT_SIZE + 10)