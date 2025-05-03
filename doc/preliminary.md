kemu specific directives:
- `ORIGIN x` - org command
- `DATA x y z...` - literal hytes to put in program memory
- `STRING "text"` - ASCII text converted to wavescii
- `INCLUDE "path/to/file"` - yea

there are two types of labels:
- `positional_label:` - the value becomes its offset in program memory
- `literal_label = #5` - the value is set literally and inline
