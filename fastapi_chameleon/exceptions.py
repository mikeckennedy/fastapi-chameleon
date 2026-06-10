from typing import Optional


class FastAPIChameleonException(Exception):
    """
    Base class for every error raised by fastapi-chameleon.

    Raised directly for configuration and rendering problems, such as calling
    ``global_init()`` with a missing or invalid template folder, rendering before
    ``global_init()`` has run, or returning an unsupported type from a decorated view.
    The control-flow exceptions below subclass it, so catching this type catches them all.
    """

    pass


class FastAPIChameleonNotFoundException(FastAPIChameleonException):
    """
    Signals a 404 response from inside a decorated view.

    Raised by ``not_found()`` and caught by the ``template()`` decorator, which renders
    ``template_file`` with an HTTP 404 status. You normally raise it indirectly via
    ``not_found()`` rather than constructing it yourself.

    :ivar str template_file: The template to render for the 404 response.
    :ivar message: The optional human-readable message describing the error.
    """

    def __init__(self, message: Optional[str] = None, four04template_file: str = 'errors/404.pt'):
        super().__init__(message)

        self.template_file: str = four04template_file
        self.message: Optional[str] = message


class FastAPIChameleonGenericException(FastAPIChameleonException):
    """
    Signals an arbitrary error response from inside a decorated view.

    Raised by ``generic_error()`` and caught by the ``template()`` decorator, which
    renders ``template_file`` with the chosen ``status_code``. You normally raise it
    indirectly via ``generic_error()`` rather than constructing it yourself.

    :ivar str template_file: The template to render for the error response.
    :ivar int status_code: The HTTP status code to return.
    :ivar message: The optional human-readable message describing the error.
    :ivar template_data: Optional variables passed to the template when rendering.
    """

    def __init__(self, template_file: str, status_code: int,
                 message: Optional[str] = None, template_data: Optional[dict] = None):
        super().__init__(message)

        self.template_file: str = template_file
        self.status_code: int = status_code
        self.message: Optional[str] = message
        self.template_data: Optional[dict] = template_data
