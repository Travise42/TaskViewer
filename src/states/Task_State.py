import json
import pygame

from src.states.Add_State import Add_State

from src.Constants import *
from src.Category import Category
from src.Task import Task

class Task_State:
    
    screen: pygame.Surface
    categories: list[Category]
    tasks: list[Task]
    
    selected_category: Category
    hovered_category: Category
    hovered_task: Task
    
    scroll_tasks: int
    preview_cooldown: int
    
    def __init__(self, screen: pygame.Surface, categories: list[Category], tasks: list[Task]):
        self.screen = screen
        self.categories = categories
        self.tasks = tasks
        
        self.selected_category = categories[0]
        self.hovered_category = None
        self.hovered_task = None
        
        self.scroll_tasks = 0
        self.reset_preview_cooldown()
        
        self.font = pygame.font.SysFont("Monsterat", Category.FONT_SIZE)
        
    def update(self, add_state: Add_State) -> list[bool, int]:
        return_values = [True, TASK_STATE]
        
        if self.hovered_category is None:
            self.preview_cooldown += 1
            if self.preview_cooldown > 0:
                self.reset_preview_cooldown()
        else:
            self.preview_cooldown -= 1
            if self.preview_cooldown < 0:
                self.preview_cooldown = -10
            
            if self.preview_cooldown == 0:
                self.bound_scroll_tasks()
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quiting
            if event.type == pygame.QUIT:
                return_values[0] = False
            
            # Clicking
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for category in self.categories:
                    if category is self.hovered_category:
                        self.selected_category = category
                        self.reset_preview_cooldown()
                        self.scroll_tasks = 0
                        break
                    
                if self.selected_category != None:
                    for i, task in enumerate(self.get_visible_tasks()):
                        if task is self.hovered_task:
                            return_values[1] = ADD_STATE
                            add_state.open(task)
                        
                x = SCREEN_WIDTH * 3/4
                y = SCREEN_HEIGHT - 40
                radius = 30
                if (mouse_pos[0] - x)**2 + (mouse_pos[1] - y)**2 < radius**2:
                    return_values[1] = ADD_STATE
                    add_state.new(self.selected_category.name)
                    
            # Hovering
            elif event.type == pygame.MOUSEMOTION:
                for i, category in enumerate(self.categories):
                    if -10 < mouse_pos[0] - Category.get_x() < Category.OPTION_WIDTH + 10 and -10 < mouse_pos[1] - Category.get_y(i) < 1.5*Category.FONT_SIZE + 10:
                        if self.hovered_category != category:
                            self.hovered_category = category
                            self.bound_scroll_tasks()
                            if self.preview_cooldown > 0:
                                self.reset_preview_cooldown()
                        break
                else:
                    self.hovered_category = None
                
                if self.selected_category != None:
                    for i, task in enumerate(self.get_visible_tasks()):
                        if -10 < mouse_pos[0] - Task.get_x() < Task.OPTION_WIDTH + 10 and -10 < mouse_pos[1] - Task.get_y(i) < 1.5*Task.FONT_SIZE + 10:
                            self.hovered_task = task
                            break
                    else:
                        self.hovered_task = None 
                        
            # Scrolling
            elif event.type == pygame.MOUSEWHEEL:
                if 0 < mouse_pos[0] - Task.get_x() + 10 < Task.OPTION_WIDTH + 20 and 0 < mouse_pos[1] - 10 < len(self.categories) * (1.5*Task.FONT_SIZE + 10) + 10:
                    self.scroll_tasks -= event.y
                    self.bound_scroll_tasks()
            
        return return_values

    def draw(self) -> None:
        """Draw the tasks screen
        """
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Background
        self.screen.fill(COLOR_BACKGROUND)
        
        # Categories background
        pygame.draw.rect(self.screen, COLOR_CONTRAST, (10, 10, Category.OPTION_WIDTH + 20, 10*(1.5*Category.FONT_SIZE + 10) + 10), 0, 25)
        
        # Categories
        for i, category in enumerate(self.categories):
            
            # Move selected categories to the right
            if category is self.hovered_category or category is self.selected_category or category.dx == 5:
                category.dx = min(category.dx + 5, 9)
            elif category.dx > 0:
                category.dx = max(category.dx - 5, 0)
            
            # Get color of category
            color = category.color
            if category.dx and not (pygame.mouse.get_pressed()[0] and category is self.hovered_category):
                color = category.highlight
                
            # Draw box
            pygame.draw.rect(self.screen, color, (Category.get_x() + category.dx, Category.get_y(i), Category.OPTION_WIDTH, 1.5*Category.FONT_SIZE), 0, 25)
            
            # White outline when hovered
            if category is self.hovered_category:
                pygame.draw.rect(self.screen, COLOR_HIGHLIGHT, (Category.get_x() + category.dx, Category.get_y(i), Category.OPTION_WIDTH, 1.5*Category.FONT_SIZE), 3, 25)
            
            # Category Texts
            text = self.font.render(category.name, True, COLOR_TEXT)
            self.screen.blit(text, (Category.get_x() + category.dx + Category.OPTION_WIDTH / 2 - text.get_width()/2, Category.get_y(i) + 1.5*Category.FONT_SIZE/3.5))
        
        # Tasks background
        pygame.draw.rect(self.screen, COLOR_CONTRAST, (Task.get_x() - 10, 10, Task.OPTION_WIDTH + 20, 10*(1.5*Task.FONT_SIZE + 10) + 10), 0, 25)
        
        # Tasks
        if self.preview_cooldown <= 0 and self.hovered_category != None:
            category = self.hovered_category
        elif self.selected_category != None:
            category = self.selected_category
            
        for i, task in enumerate(self.get_visible_tasks()):
            
            for task_category in self.categories:
                if task.parent == task_category.name:
                    break
            
            # Get color of task
            color = task_category.color
            if self.hovered_task == task and not (pygame.mouse.get_pressed()[0] and task is self.hovered_task):
                color = task_category.highlight
                
            # Draw box
            pygame.draw.rect(self.screen, color, (Task.get_x(), Task.get_y(i), Task.OPTION_WIDTH, 1.5*Task.FONT_SIZE), 0, 25)
            
            # White outline when hovered
            if task is self.hovered_task:
                pygame.draw.rect(self.screen, (220, 220, 220), (Task.get_x(), Task.get_y(i), Task.OPTION_WIDTH, 1.5*Task.FONT_SIZE), 3, 25)
            
            # Task Texts
            text = self.font.render(task.name, True, COLOR_TEXT)
            self.screen.blit(text, (Task.get_x() + Task.OPTION_WIDTH / 2 - text.get_width()/2, Task.get_y(i) + 1.5*Task.FONT_SIZE/3.5))
        
        # Add task button
        
        # Button
        x = SCREEN_WIDTH * 3/4
        y = SCREEN_HEIGHT - 40
        radius = 30
        touching_mouse = (mouse_pos[0] - x)**2 + (mouse_pos[1] - y)**2 < radius**2
        color = COLOR_TEXT
        if touching_mouse:
            color = COLOR_GREY if pygame.mouse.get_pressed()[0] else COLOR_HIGHLIGHT
            
        pygame.draw.circle(self.screen, COLOR_CONTRAST, (x, y), radius)
        if touching_mouse:
            pygame.draw.circle(self.screen, color, (x, y), radius, 3)
        
        # Plus Sign
        for dx, dy in [(1, 0), (0, 1)]:
            pygame.draw.line(self.screen, color, (x - dx*radius/2, y - dy*radius/2), (x + dx*radius/2, y + dy*radius/2), 6)
            
    def reset_preview_cooldown(self):
        self.preview_cooldown = 20
            
    def handle_tasks(self):
        self.tasks.sort(key=lambda task: task.name)
        self.tasks.sort(key=lambda task: task.priority, reverse=True)
        
        self.bound_scroll_tasks()
        
        with open("src/data/tasks.json", "w") as file:
            json.dump([[task.name, 
                        task.parent,
                        task.type,
                        task.date.month,
                        task.date.day,
                        task.date.year,
                        task.date.hour,
                        task.date.minute,
                        *task.length,
                        task.priority] for task in self.tasks], file)
            
    def get_visible_tasks(self) -> list[Task]:
        if self.preview_cooldown <= 0 and self.hovered_category != None:
            category = self.hovered_category
        else:
            category = self.selected_category
        
        return list(filter(lambda task: task.parent == category.name or category.name == "All", self.tasks))[self.scroll_tasks:][:10]
            
    def bound_scroll_tasks(self):
        if self.preview_cooldown <= 0 and self.hovered_category != None:
            category = self.hovered_category
        else:
            category = self.selected_category
        
        self.scroll_tasks = max(min(self.scroll_tasks, len(list(filter(lambda task: task.parent == category.name or category.name == "All", self.tasks))) - 5), 0)
        