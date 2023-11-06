
from enum import Enum

class PirorityEnum(Enum):
    HIGH = 'HIGH'
    MEDUIM = 'MEDUIM'
    LOW = 'LOW'

class TaskStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    
