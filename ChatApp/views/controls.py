class Message:
    def __init__(
            self,
            username: str,
            message: str,
            session_id: str
            
    ):
        self.username = username
        self.message = message
        self.session_id = session_id