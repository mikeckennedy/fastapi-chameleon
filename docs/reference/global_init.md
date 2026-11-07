## global_init()


Initialize the Chameleon template engine for your app.


Usage

``` python
global_init(
    template_folder,
    auto_reload=False,
    cache_init=True,
)
```


Call this once at startup, pointing it at the folder that holds your `*.pt` templates. Template paths used elsewhere (in [template()](template.md#fastapi_chameleon.template), [response()](response.md#fastapi_chameleon.response), [not_found()](not_found.md#fastapi_chameleon.not_found), and [generic_error()](generic_error.md#fastapi_chameleon.generic_error)) are resolved relative to this folder. Call it before the modules that define decorated views are imported, so that template name inference sees the right folder.

## Examples

``` python
from pathlib import Path
import fastapi_chameleon
```

    templates = Path(__file__).resolve().parent / 'templates'
    fastapi_chameleon.global_init(templates, auto_reload=dev_mode)


## Parameters


`template_folder: Union[str, os.PathLike[str]]`  
Path to the folder containing your Chameleon templates, as a `str` or any `os.PathLike` such as `pathlib.Path`.

`auto_reload: bool = ``False`  
Reload templates from disk when they change. Handy in development; leave `False` in production. Defaults to `False`.

`cache_init: bool = ``True`  
When `True` (the default), a second call is a no-op once the engine is already initialized. Pass `False` to force re-initialization (for example, to switch template folders in tests).


## Raises


`FastAPIChameleonException`  
If `template_folder` is empty or is not a directory.
