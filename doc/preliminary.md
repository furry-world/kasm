kemu specific directives:
- `ORIGIN x` - org command
- `DATA x y z...` - literal hytes to put in program memory
- `STRING "text"` - ASCII text converted to wavescii
- `INCLUDE "path/to/file"` - yea
- `INCLUDEBINARY "path/to/file"` - include file as raw bytes

there are two types of labels:
- `positional_label:` - the value becomes its offset in program memory
- `literal_label = #5` - the value is set literally and inline

preprocessors:
- `example@1` - return Nth hyte of a label's value (0 is least significant)
