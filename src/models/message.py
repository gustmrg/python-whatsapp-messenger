DEFAULT_WAIT_TIME = 10
DEFAULT_TAB_CLOSE = True
DEFAULT_CLOSE_TIME = 5


class Message:
    def __init__(self):
        self.phone_number = None
        self.message_body = None
        self.time_hour = None
        self.time_minute = None
        self.wait_time = DEFAULT_WAIT_TIME
        self.tab_close = DEFAULT_TAB_CLOSE
        self.close_time = DEFAULT_CLOSE_TIME
