## exceptions.FastAPIChameleonException


Base class for every error raised by fastapi-chameleon.


Usage

``` python
exceptions.FastAPIChameleonException()
```


Raised directly for configuration and rendering problems, such as calling [global_init()](global_init.md#fastapi_chameleon.global_init) with a missing or invalid template folder, rendering before [global_init()](global_init.md#fastapi_chameleon.global_init) has run, or returning an unsupported type from a decorated view. The control-flow exceptions below subclass it, so catching this type catches them all.
