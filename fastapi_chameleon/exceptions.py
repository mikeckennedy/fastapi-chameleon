from typing import Optional


class FastAPIChameleonException(Exception):
    pass


class FastAPIChameleonNotFoundException(FastAPIChameleonException):
    def __init__(self, message: Optional[str] = None, four04template_file: str = 'errors/404.pt'):
        super().__init__(message)

        self.template_file: str = four04template_file
        self.message: Optional[str] = message
