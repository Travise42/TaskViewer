import json
import pygame

from src.Category import Category
from src.Constants import *

class Entry:
    
    PADX = 20
    PADY = 10
    
    screen: pygame.Surface
    x: int
    y: int
    width: int
    font: pygame.font.Font
    text: str
    placeholder: str
    type: int
    date: int
    
    hovered: bool
    typing: bool
    typing_index: int
    valid: bool
    open: bool
    options: list[str]
    
    tick: int
    backspace_cooldown: int
    
    ascii_dictionary: dict[str:str]
    
    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, font: pygame.font.Font, text: str = "", placeholder: str = "", type: int = TEXT_ENTRY, date: bool = False):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.text = text
        self.placeholder = placeholder
        self.type = type
        self.date = date
        
        self.hovered = False
        self.typing = False
        self.typing_index = 0
        self.valid = True
        self.open = False
        self.options = []
        
        self.backspace_cooldown = 0
        self.tick = 0
        
        with open("src/data/ascii.json", "r") as file:
            self.ascii_dictionary = json.load(file)
        
    def add_options(self, options: list[str]) -> object:
        self.options += options
        
        return self
        
    def click(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        
        if self.type == TEXT_ENTRY:
            
            # Start typing if entry is clicked
            if self.hovered:
                self.typing = True
                
                x = mouse_pos[0] - self.x - Entry.PADX
                for i in range(len(self.text)):
                    self.typing_index = i
                    if x < self.font.size(self.text[i])[0]/2:
                        break
                    x -= self.font.size(self.text[i])[0]
                else:
                    self.typing_index = len(self.text)
                
            # Stop typing if mouse clicked elsewhere
            elif self.typing:
                self.finish()
                
            self.tick = 0
        
        elif self.type == DROPDOWN_ENTRY:
            if self.open:
                # Select an option
                count = 0
                for option in self.options:
                    if option == self.text:
                        continue
                    count += 1
                    
                    dy = count*self.get_height()
                    if 0 < mouse_pos[0] - self.x < self.width and 0 < mouse_pos[1] - self.y - dy < self.get_height():
                        self.text = option
                        break
                
                self.open = False
            else:
                self.open = self.hovered
    
    def input(self, key: int):
        if not self.typing:
            return
        
        # Type
        if 32 <= key <= 126:
            if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]) and chr(key) in self.ascii_dictionary.keys():
                self.insert(self.ascii_dictionary.get(chr(key)))
            else:
                self.insert(chr(key))
            
        # Backspace
        elif key == pygame.K_BACKSPACE:
            self.backspace(pygame.key.get_pressed()[pygame.K_LCTRL])
            self.backspace_cooldown = 10
            
        # Finish
        elif key == pygame.K_RETURN:
            self.finish()
            
        # Move Index
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.move_index([-1, 1][key == pygame.K_RIGHT], pygame.key.get_pressed()[pygame.K_LCTRL])
    
    def insert(self, character: chr) -> None:
        self.text = self.text[:self.typing_index] + character + self.text[self.typing_index:]
        self.typing_index += 1
        
        self.tick = 0
    
    def move_index(self, indexes: int, ctrl: bool) -> None:
        if ctrl:
            if indexes < 0:
                self.typing_index = 0
            elif indexes > 0:
                self.typing_index = len(self.text)
        else:
            self.typing_index = max(min(self.typing_index + indexes, len(self.text)), 0)
        
        self.tick = 0
    
    def backspace(self, ctrl: bool) -> None:
        if ctrl:
            self.text = self.text[self.typing_index:]
            self.typing_index = 0
        elif self.typing_index:
            self.text = self.text[:self.typing_index - 1] + self.text[self.typing_index:]
            self.typing_index -= 1
            
        self.tick = 0
    
    def finish(self) -> None:
        self.typing = False
        
        if self.date:
            # Reformat
            date = self.text.replace(" ", "").split("/")
            if len(date) >= 3:
                self.text = date[0].rjust(2, "0") + " / " + date[1].rjust(2, "0") + " / " + date[2].rjust(2, "0")
        
    def update(self, a_dropdown_is_open: bool = False) -> None:
        mx, my = pygame.mouse.get_pos()
        self.hovered = (not a_dropdown_is_open or self.open) and 0 < mx - self.x < self.width and 0 < my - self.y < self.get_height()
        
        if self.typing:
            if self.backspace_cooldown < 0 and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                if self.tick%2:
                    self.backspace(pygame.key.get_pressed()[pygame.K_LCTRL])
        
        self.backspace_cooldown -= 1
        self.tick += 1
    
    def draw(self, categories: list[Category] = []) -> None:
        # Entry Box
        pygame.draw.rect(self.screen, COLOR_CONTRAST, (self.x, self.y, self.width, self.get_height()))
        color = COLOR_HIGHLIGHT if self.hovered else COLOR_TEXT if self.valid else COLOR_ERROR
        pygame.draw.rect(self.screen, color, (self.x, self.y, self.width, self.get_height()), 3)
        
        # Text
        if len(self.text):
            color = COLOR_GREY
            for category in categories:
                if self.text == category.name:
                    color = category.color
            text = self.font.render(self.text, True, color)
            self.screen.blit(text, (self.x + Entry.PADX, self.y + Entry.PADY))
        else:
            text = self.font.render(self.placeholder, True, COLOR_TEXT)
            self.screen.blit(text, (self.x + Entry.PADX, self.y + Entry.PADY))
        
        # Dropdown menu
        if self.open:
            mx, my = pygame.mouse.get_pos()
            count = 0
            for option in self.options:
                if option == self.text:
                    continue
                
                count += 1
                
                # Box
                dy = count*self.get_height()
                pygame.draw.rect(self.screen, COLOR_CONTRAST, (self.x, self.y + dy, self.width, self.get_height()))
                color = COLOR_HIGHLIGHT if 0 < mx - self.x < self.width and 0 < my - self.y - dy < self.get_height() else COLOR_TEXT
                pygame.draw.rect(self.screen, color, (self.x, self.y + dy, self.width, self.get_height()), 3)
                
                # Text
                color = COLOR_GREY
                for category in categories:
                    if option == category.name:
                        color = category.color
                text = self.font.render(option, True, color)
                self.screen.blit(text, (self.x + Entry.PADX, self.y + Entry.PADY + dy))
        
        # Indicator
        if self.typing and not self.tick//20 % 2:
            x = self.x + Entry.PADX + self.font.size(self.text[:self.typing_index])[0]
            pygame.draw.line(self.screen, COLOR_GREY, (x, self.y + Entry.PADY), (x, self.y + Entry.PADY + self.font.get_height()), 3)
    
    def dropdown(self) -> None:
        pass
    
    def get_height(self) -> int:
        return self.font.get_height() + 2*Entry.PADY