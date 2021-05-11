# sphinx4bug
Demonstrating a failure with Sphinx 4

To show the problem, install Sphinx 4.0.0 in your current Python (virtual) environment and run:

```
make clean html
```

(Building on Windows with this cut down version not formally supported. I don't care!)

## Example build
Note the WARNING about a duplicate `Grill` reference, one of which is for its logical API location and the other of which is for where the implementation is.

```
bash$ make clean html
rm -f -rf foo.rst foo.bar.rst modules.rst _build
Running Sphinx v4.0.0
making output directory... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 4 source files that are out of date
updating environment: [new config] 4 added, 0 changed, 0 removed
reading sources... [100%] modules
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] modules
/home/dkf/git/sphinx4bug/foo/example.py:docstring of foo.example.FooBarExample.make_grill:: WARNING: more than one target found for cross-reference 'Grill': foo.bar.Grill, foo.bar.grill.Grill
generating indices... genindex py-modindex done
writing additional pages... search done
copying static files... done
copying extra files... done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded, 1 warning.

The HTML pages are in _build/html.
```
