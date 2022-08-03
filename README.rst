#######
Stilted
#######

An partial implementation of a subset of PostScript, just for fun.

Some things are just wrong:

- Strings do not nest parentheses.

- Literal/executable bits are stored on objects, so this is wrong::

    null dup cvx xcheck exch xcheck  -->  true false    % PostScript
    null dup cvx xcheck exch xcheck  -->  true true     % Stilted
