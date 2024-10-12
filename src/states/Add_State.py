import pygame

from src.Constants import *
from src.Category import Category
from src.Task import Task
from src.Entry import Entry

import datetime

class Add_State:
    
    FONT_SIZE = 50
    MARGIN = 200
    
    NAME_WIDTH = 500
    PARENT_WIDTH = 500
    TYPE_WIDTH = 300
    DATE_WIDTH = 250
    TIME_WIDTH = 200
    LENGTH_WIDTH = 200
    PRIORITY_WIDTH = 300
    
    screen: pygame.Surface
    categories: list[Category]
    tasks: list[Task]
    is_new: bool
    
    task: Task
    entries: list[Entry]
    
    def __init__(self, screen: pygame.Surface, categories: list[Category], tasks: list[Task]):
        self.screen = screen
        self.categories = categories
        self.tasks = tasks
        
        self.Task = None
        self.entries = []
        
        self.font = pygame.font.SysFont("Monsterat", Add_State.FONT_SIZE)
        
        self.is_new = False

    def update(self) -> list[bool, int]:
        return_values = [True, ADD_STATE]
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quiting
            if event.type == pygame.QUIT:
                return_values[0] = False
                
            # Clicking
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Text boxes
                for entry in self.entries:
                    entry.click()
                self.validate_entries()
                
                # Buttons
                
                width = ( SCREEN_WIDTH - 2*Add_State.MARGIN - 20 ) /2
                height = self.font.get_height() + 2*Entry.PADY
                y = Add_State.MARGIN + 6*(height + 10)
                x = Add_State.MARGIN
                
                # Cancel/Delete Button
                if 0 < mouse_pos[0] - x < width and 0 < mouse_pos[1] - y < height:
                    return_values[1] = TASK_STATE
                    if self.is_new and self.task in self.tasks:
                        self.tasks.remove(self.task)
                    
                # Save button
                x = Add_State.MARGIN + width + 20
                if 0 < mouse_pos[0] - x < width and 0 < mouse_pos[1] - y < height:
                    if all(entry.valid for entry in self.entries):
                        # Update Task
                        self.task.name = self.entries[0].text
                        self.task.parent = self.entries[1].text
                        self.task.type = self.entries[2].options.index(self.entries[2].text)
                        self.task.date.replace(
                            month = int(self.entries[3].text.split(" / ")[0]),
                            day = int(self.entries[3].text.split(" / ")[1]),
                            year = int("20" + self.entries[3].text.split(" / ")[2]),
                            hour = int(self.entries[4].text.split(":")[0]),
                            minute = int(self.entries[4].text.split(":")[1])
                        )
                        self.task.length = tuple(int(i) for i in self.entries[5].text.split(":"))
                        self.task.priority = self.entries[6].options.index(self.entries[6].text)
                        
                        return_values[1] = TASK_STATE
                
                # Delete Button
                radius = 50
                x = Add_State.MARGIN - 50 - radius
                y = Add_State.MARGIN + 10 + radius
                if (mouse_pos[0] - x)**2 + (mouse_pos[1] - y)**2 < radius**2:
                    return_values[1] = TASK_STATE
                    if self.task in self.tasks:
                        self.tasks.remove(self.task)
                    
            # Typing
            elif event.type == pygame.KEYDOWN:
                for entry in self.entries:
                    entry.input(event.key)
                
                self.validate_entries()
                
        return return_values

    def validate_entries(self):
        # Name must not be the same as any other tasks in the category
        self.entries[0].valid = self.entries[0].text not in [task.name for task in self.tasks if (task.parent == "All" or task.parent == self.entries[1].text) and task is not self.task]
        
        # Date must be in the proper MM/DD/YY format
        date = self.entries[3].text.replace(" ", "").split("/")
        
        self.entries[3].valid = True
        if len(date) != 3:
            self.entries[3].valid = False
        
        else:
            for i in range(3):
                # Dates are numbers
                if not date[i].isnumeric():
                    self.entries[3].valid = False
                    break
                    
                # Numbers are in a valid range
                if not (0 < int(date[i]) <= [12, 31, 99][i]):
                    self.entries[3].valid = False
                    break
                
        # Time must be in the format HH:MM
        time = self.entries[4].text.split(":")
        
        self.entries[4].valid = True
        if len(time) == 0:
            pass
        elif len(time) != 2:
            self.entries[4].valid = False
        else:
            for i in range(2):
                # Times are numbers
                if not time[i].isnumeric():
                    self.entries[4].valid = False
                    break
                    
                # Times are in a valid range
                if not (0 <= int(time[i]) < [24, 60][i]):
                    self.entries[4].valid = False
                    break
                
        # Length must be in the format HH:MM
        time = self.entries[5].text.split(":")
        
        self.entries[5].valid = True
        if len(time) == 0:
            pass
        elif len(time) != 2:
            self.entries[5].valid = False
        else:
            for i in range(2):
                # Times are numbers
                if not time[i].isnumeric():
                    self.entries[5].valid = False
                    break
                    
                # Times are in a valid range
                if not (0 <= int(time[i]) < [24, 60][i]):
                    self.entries[5].valid = False
                    break

    def draw(self) -> None:
        """Draw the add task screen
        """
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Background
        self.screen.fill(COLOR_BACKGROUND)
            
        ## Buttons ##
        
        width = ( SCREEN_WIDTH - 2*Add_State.MARGIN - 20 ) /2
        height = self.font.get_height() + 2*Entry.PADY
        y = Add_State.MARGIN + 6*(height + 10)
        
        # Delete/Cancel Button
        
        # Button
        x = Add_State.MARGIN
        touching_mouse = 0 < mouse_pos[0] - x < width and 0 < mouse_pos[1] - y < height
        colors = [COLOR_TEXT, COLOR_CONTRAST]
        if touching_mouse:
            colors = [COLOR_GREY, COLOR_CONTRAST] if pygame.mouse.get_pressed()[0] else [COLOR_HIGHLIGHT, COLOR_ERROR]
        
        pygame.draw.rect(self.screen, colors[1], (x, y, width, height), 0, height//2)
        pygame.draw.rect(self.screen, colors[0], (x, y, width, height), 3, height//2)
        
        # Text
        button_text = "Delete" if self.is_new else "Cancel"
        text = self.font.render(button_text, True, colors[0])
        self.screen.blit(text, (x + width/2 - self.font.size(button_text)[0]/2, y + Entry.PADY))
        
        # Save Button
        
        # Button
        x = Add_State.MARGIN + width + 20
        touching_mouse = 0 < mouse_pos[0] - x < width and 0 < mouse_pos[1] - y < height
        color = COLOR_TEXT
        if touching_mouse:
            color = COLOR_GREY if pygame.mouse.get_pressed()[0] else COLOR_HIGHLIGHT
            
        pygame.draw.rect(self.screen, COLOR_CONTRAST, (x, y, width, height), 0, height//2)
        pygame.draw.rect(self.screen, color, (x, y, width, height), 3, height//2)
        
        # Text
        text = self.font.render("Save", True, color)
        self.screen.blit(text, (x + width/2 - self.font.size("Save")[0]/2, y + Entry.PADY))
            
        # Delete Button
        
        if not self.is_new:
            # Button
            radius = 50
            x = Add_State.MARGIN - 50 - radius
            y = Add_State.MARGIN + 10 + radius
            touching_mouse = (mouse_pos[0] - x)**2 + (mouse_pos[1] - y)**2 < radius**2
            colors = [COLOR_TEXT, COLOR_CONTRAST]
            if touching_mouse:
                colors = [COLOR_GREY, COLOR_CONTRAST] if pygame.mouse.get_pressed()[0] else [COLOR_HIGHLIGHT, COLOR_ERROR]
                
            pygame.draw.circle(self.screen, colors[1], (x, y), radius)
            pygame.draw.circle(self.screen, colors[0], (x, y), radius, 3)
            
            # Garbage Can
            pygame.draw.line(self.screen, colors[0], (x, y - 3/5*radius), (x, y - 2/5*radius), 8)
            pygame.draw.line(self.screen, colors[0], (x - 1/2*radius, y - 2/5*radius), (x + 1/2*radius, y - 2/5*radius), 8)
            for x1, x2 in [(-5/12, -1/3), (0, 0), (5/12, 1/3)]:
                pygame.draw.line(self.screen, colors[0], (x + x1*radius, y - 1/8*radius), (x + x2*radius, y + 1/2*radius), 8)
        
        # Draw dropdown menus first, then entries
        for entry in sorted(self.entries, key=lambda entry: entry.open):
            entry.update(any(e.open for e in self.entries if e.type == DROPDOWN_ENTRY))
            entry.draw(self.categories)
            
        
    def new(self, category: str) -> None:
        task = Task.createNew(parent=category)
        self.tasks.append(task)
        self.open(task)
        self.is_new = True
        
    def open(self, task: Task):
        self.task = task
        self.is_new = False
    
        spacing = self.font.get_height() + 2*Entry.PADY + 10
        self.entries = []
        self.entries.append(Entry(self.screen, Add_State.MARGIN, Add_State.MARGIN, Add_State.NAME_WIDTH, self.font, self.task.name, "name"))
        self.entries.append(Entry(self.screen, Add_State.MARGIN, Add_State.MARGIN + spacing, Add_State.PARENT_WIDTH, self.font, self.task.parent, "category", DROPDOWN_ENTRY).add_options([category.name for category in self.categories]))
        self.entries.append(Entry(self.screen, Add_State.MARGIN, Add_State.MARGIN + 2*spacing, Add_State.TYPE_WIDTH, self.font, ["Deadline", "Effort", "Event"][self.task.type], "type", DROPDOWN_ENTRY).add_options(["Deadline", "Effort", "Event"]))
        self.entries.append(Entry(self.screen, Add_State.MARGIN, Add_State.MARGIN + 3*spacing, Add_State.DATE_WIDTH, self.font, datetime_to_string(self.task.date), "MM/DD/YY", date=True))
        self.entries.append(Entry(self.screen, Add_State.MARGIN + Add_State.DATE_WIDTH + 20, Add_State.MARGIN + 3*spacing, Add_State.TIME_WIDTH, self.font, str(self.task.date.time())[:-3], "HH:MM"))
        self.entries.append(Entry(self.screen, Add_State.MARGIN, Add_State.MARGIN + 4*spacing, Add_State.LENGTH_WIDTH, self.font, time_to_string(*self.task.length), "HH:MM"))
        self.entries.append(Entry(self.screen, Add_State.MARGIN + Add_State.LENGTH_WIDTH + 20, Add_State.MARGIN + 4*spacing, Add_State.PRIORITY_WIDTH, self.font, ["Low", "Medium", "High"][self.task.priority], "priority", DROPDOWN_ENTRY).add_options(["Low", "Medium", "High"]))
        
        self.validate_entries()
        
def datetime_to_string(date: datetime.datetime) -> str:
    """Return datetime in the form MM/DD/YY.
    """
        
    return str(date.month).rjust(2, "0") + " / " + str(date.day).rjust(2, "0") + " / " + str(date.year)[-2:]

def time_to_string(hour: int, minute: int):
    return str(hour).rjust(2, "0") + ":" + str(minute).rjust(2, "0")
        

