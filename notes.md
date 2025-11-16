# features
- profiles
    - architecture (k6 or k8)
    - default includes (for hw definitions)
    - image size and location
    - syntax (modern or classic)
    - case sensitivity
    - string encoding

- all features and preprocessors from python kasm + basic math preprocessors

# architecture
- all instructions are objects of a class
    - mnemonics (modern and classic)
    - .assemble()
    - they inherit from template functions
    - throw exception upon error

- parser class
    - current file and line
    - current byte offset
    - passed to the instructions during parsing
    - catch error
    - defaults to one syntax, is overridden by the other (or is an abstract class)
    
# debug library
- debug prints (including function name)
- print stack trace (if possible)
- std::chrono (for basic profiling)
- disableable by a global toggle (ideally a build flag)
