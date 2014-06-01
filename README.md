PCX
===========

Python scripts to take C or C++ source code and extract an XML representation from Clang's AST


parse_source.py
---------------

Usage: python2 parse_source.py filename.c(pp)

Walks through the AST produced by clang using the Python bindings of libclang.

Uses to_xml.py, which will break down the elements in the AST tree into XML nodes. Note that the tokenizing of clang is not perfect, and must be handled relatively manually.

