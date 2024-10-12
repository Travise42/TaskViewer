import pygame

import json

from src.states.Task_State import Task_State
from src.states.Add_State import Add_State

from src.Constants import *
from src.Category import Category
from src.Task import Task

def run():
    
    # Create window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_icon(pygame.image.load("task_icon.png"))
    pygame.display.set_caption("TaskViewer")
    clock = pygame.time.Clock()
    
    categories: list[Category] = [Category("All", (220, 120, 120))]
    with open("src/data/categories.json", "r") as file:
        for category in json.load(file):
            categories.append(Category(category[0], (int(category[1]), int(category[2]), int(category[3]))))
    
    tasks: list[Task] = []
    with open("src/data/tasks.json", "r") as file:
        for task in json.load(file):
            tasks.append(Task(task))
    
    task_state = Task_State(screen, categories, tasks)
    add_state = Add_State(screen, categories, tasks)
    
    running = True
    state = TASK_STATE
    pending = False
    while running:
        
        if state == TASK_STATE:
            if pending:
                task_state.handle_tasks()
                pending = False
            return_values = task_state.update(add_state)
            task_state.draw()
        
        elif state == ADD_STATE:
            pending = True
            return_values = add_state.update()
            add_state.draw()
        
        pygame.display.update()
        clock.tick(30)
        running, state = return_values


if __name__ == '__main__':
    run()