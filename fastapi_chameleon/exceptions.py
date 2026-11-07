from typing import Optional


class FastAPIChameleonException(Exception):
    """
    Base class for every error raised by fastapi-chameleon.

    Raised directly for configuration and rendering problems, such as calling
    ``global_init()`` with a missing or invalid template folder, rendering before
    ``global_init()`` has run, or returning an unsupported type from a decorated view.
    The control-flow exceptions below subclass it, so catching this type catches them all.

    Example::

        try:
            fastapi_chameleon.global_init(settings.template_folder)
        except FastAPIChameleonException as e:
            raise SystemExit(f'Template folder problem: {e}')
    """

    pass


class FastAPIChameleonNotFoundException(FastAPIChameleonException):
    """
    Signals a 404 response from inside a decorated view.

    Raised by ``not_found()`` and caught by the ``template()`` decorator, which renders
    ``template_file`` with an HTTP 404 status. You normally raise it indirectly via
    ``not_found()`` rather than constructing it yourself.

    Example::

        try:
            fastapi_chameleon.not_found('errors/custom_404.pt')
        except FastAPIChameleonNotFoundException as e:
            assert e.template_file == 'errors/custom_404.pt'

    :ivar template_file: The template to render for the 404 response (the constructor
        accepts it as ``four04template_file``).
    :vartype template_file: str
    :ivar message: The optional human-readable message describing the error.
    :vartype message: Optional[str]
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

    Example::

        try:
            fastapi_chameleon.generic_error('errors/403.pt', 403, template_data={'user': user})
        except FastAPIChameleonGenericException as e:
            assert e.status_code == 403 and e.template_data == {'user': user}

    :ivar template_file: The template to render for the error response.
    :vartype template_file: str
    :ivar status_code: The HTTP status code to return.
    :vartype status_code: int
    :ivar message: The optional human-readable message describing the error.
    :vartype message: Optional[str]
    :ivar template_data: Optional variables passed to the template when rendering.
    :vartype template_data: Optional[dict]
    """

    def __init__(
        self, template_file: str, status_code: int, message: Optional[str] = None, template_data: Optional[dict] = None
    ):
        super().__init__(message)

        self.template_file: str = template_file
        self.status_code: int = status_code
        self.message: Optional[str] = message
        self.template_data: Optional[dict] = template_data
