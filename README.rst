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


To run it, clone this repo, then you can get an interactive prompt with::

    $ python cli.py

or run a PostScript file with::

    $ python cli.py the_file.ps
