
from src.Constants import *

from src.Category import Category

import datetime

class Task:
    """Makes up the components of TaskViewer. Contains the location, 
    date, time, length, and priority of events, deadlines, and efforts.
    
    Data saved is in the format:
    [Name, Parent, Type, Month, Day, Year, Hour, Minute, Length (Hours), Length (Minutes), Priority]
    """
    
    OPTION_WIDTH = SCREEN_WIDTH / 2 - 35
    FONT_SIZE = 40
    
    name: str
    parent: str
    type: int
    date: datetime.datetime
    length: tuple[int]
    priority: int
    
    def __init__(self, data: list) -> None:
        self.name = data[0]
        self.parent = data[1]
        self.type = data[2]
        self.date = datetime.datetime(data[5], data[3], data[4], data[6], data[7])
        self.length = (data[8], data[9])
        self.priority = data[10]
    
    def createNew(name: str = "New Task", parent: str = "All", type: int = TYPE_DEADLINE) -> None:
        date = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        return Task([name, parent, type, date.month, date.day, date.year, date.hour, date.minute, 1, 0, PRIORITY_LOW])
        
    def changeType(self, type: str) -> None:
        """Change the type of this task to Constants.TYPE_DEADLINE: Literal=[0],
        Constants.TYPE_EFFORT: Literal=[1], or Constants.TYPE_EVENT: Literal=[2]. Returns nothing.
        """
        
        self.type = type
        
    def changeDate(self, year: int, month: int, day: int) -> None:
        """Change the year, month, and day of this task to year, month, and day, 
        without changing the time of day. Returns nothing.
        """
        
        self.date.replace(year, month, day)
        
    def changeTime(self, hours: int, minutes: int) -> None:
        """Change the hour and minute of this task to hours and minutes,
        without changing the date. Returns nothing.
        """
        
        self.date.replace(hour=hours, minute=minutes)
        
    def changeLength(self, hours: int, minutes: int) -> None:
        """Chnage the length of this task to hours and minutes,
        without changing the starting time. Returns nothing.
        """
        
        self.length = hours, minutes
        
    def changePriority(self, priority: int) -> None:
        """Change the priority of this task to Constants.PRIORITY_LOW: Literal[0],
        Constants.PRIORITY_MEDIUM: Literal[1], or Constants.PRIORITY_HIGH: Literal[2]. Returns nothing.
        """
        
        self.priority = priority
        
    def get_x() -> int:
        return 50 + Category.OPTION_WIDTH
        
    def get_y(index: int) -> int:
        return 20 + index*(1.5*Task.FONT_SIZE + 10)
    