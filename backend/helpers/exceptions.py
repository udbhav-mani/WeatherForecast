class WrongInputError(ValueError):
    def __init__(self, message="Wrong input"):
        self.message = message
        super().__init__(self.message)
