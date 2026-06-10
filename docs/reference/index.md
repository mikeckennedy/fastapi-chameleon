# API Reference


Everything fastapi-chameleon exposes: the template decorator, app setup, error helpers, and the exception types.


## Setup


Point the library at your Chameleon templates folder once at app startup.


[global_init()](global_init.md#fastapi_chameleon.global_init)  
Initialize the Chameleon template engine for your app.


## Rendering views


Decorate FastAPI view functions to render templates, or build a response directly.


[template()](template.md#fastapi_chameleon.template)  
Decorate a FastAPI view to render its return value through a Chameleon template.

[response()](response.md#fastapi_chameleon.response)  
Render a template and return it as a FastAPI response directly.


## Error responses


Short-circuit a view to render a friendly error page with the right status code.


[not_found()](not_found.md#fastapi_chameleon.not_found)  
Short-circuit the current view and render a friendly 404 page.

[generic_error()](generic_error.md#fastapi_chameleon.generic_error)  
Short-circuit the current view and render an error page with a custom status code.


## Exceptions


Exception types raised by the library (the error helpers raise these internally).


[exceptions.FastAPIChameleonException](exceptions.FastAPIChameleonException.md#fastapi_chameleon.exceptions.FastAPIChameleonException)  
Base class for every error raised by fastapi-chameleon.

[exceptions.FastAPIChameleonNotFoundException](exceptions.FastAPIChameleonNotFoundException.md#fastapi_chameleon.exceptions.FastAPIChameleonNotFoundException)  
Signals a 404 response from inside a decorated view.

[exceptions.FastAPIChameleonGenericException](exceptions.FastAPIChameleonGenericException.md#fastapi_chameleon.exceptions.FastAPIChameleonGenericException)  
Signals an arbitrary error response from inside a decorated view.
