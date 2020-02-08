from enum import Enum

class PendingStatus(Enum):
    """交易的4中状态"""
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4