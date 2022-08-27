#######
Stilted
#######

An partial implementation of a subset of PostScript, with graphics by PyCairo,
just for fun.

Some things are just wrong:

- Strings do not nest parentheses.

- Literal/executable bits are stored on objects, so this is wrong::

    null dup cvx xcheck exch xcheck  -->  true false    % PostScript
    null dup cvx xcheck exch xcheck  -->  true true     % Stilted


I've written a bit about `Stilted on my blog`__.

__ https://nedbatchelder.com/blog/202208/stilted.html
