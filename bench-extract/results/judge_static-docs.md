# scenario: static-docs

## U1: https://example.com
_(note: тривиальная крошечная страница)_

**[local-auto]** (0.8s, 212 chars, tier http; wr=1.0, wo=1.0; hdr 0, code 0, links 0, lists 0)
```
---
title: Example Domain
url: https://example.com
hostname: example.com
sitename: example.com
---
This domain is for use in documentation examples without needing permission. Avoid use in operations.

Learn more
```

**[local-http]** (0.78s, 212 chars, tier http; wr=1.0, wo=1.0; hdr 0, code 0, links 0, lists 0)
```
---
title: Example Domain
url: https://example.com
hostname: example.com
sitename: example.com
---
This domain is for use in documentation examples without needing permission. Avoid use in operations.

Learn more
```

**[local-curl]** (3.84s, 213 chars, tier curl; wr=1.0, wo=1.0; hdr 0, code 0, links 0, lists 0)
```
---
title: Example Domain
url: https://example.com/
hostname: example.com
sitename: example.com
---
This domain is for use in documentation examples without needing permission. Avoid use in operations.

Learn more
```

**[local-browser]** (1.56s, 212 chars, tier browser; wr=1.0, wo=1.0; hdr 0, code 0, links 0, lists 0)
```
---
title: Example Domain
url: https://example.com
hostname: example.com
sitename: example.com
---
This domain is for use in documentation examples without needing permission. Avoid use in operations.

Learn more
```

**[firecrawl]** (16.29s, 167 chars; wr=1.0, wo=1.0; hdr 1, code 0, links 1, lists 0)
```
(пустой вывод, <200 симв.)
```

**[tavily]** (0.71s, 167 chars; wr=1.0, wo=1.0; hdr 1, code 0, links 1, lists 0)
```
(пустой вывод, <200 симв.)
```

**[jina]** (0.7s, 367 chars; wr=1.0, wo=1.0; hdr 0, code 0, links 1, lists 0)
```
Title: Example Domain

URL Source: https://example.com/

Published Time: Wed, 26 Aug 2026 20:16:59 GMT

Warning: This is a cached snapshot of the original page, consider retry with caching opt-out.

Markdown Content:
This domain is for use in documentation examples without needing permission. Avoid use in operations.

[Learn more](https://iana.org/domains/example)

```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U2: https://docs.python.org/3/library/os.html
_(note: большие EN-доки, много код-блоков)_

**[local-auto]** (1.98s, 32000 chars, tier http; wr=1.0, wo=None; hdr 1, code 0, links 21, lists 11)
```
---
title: os — Miscellaneous operating system interfaces
url: https://docs.python.org/3/library/os.html
hostname: python.org
description: "Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..."
sitename: Python documentation
date: "2016-06-02"
---
# `os` — Miscellaneous operating system interfaces[¶](https://docs.python.org#module-os)

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a threat to

[…середина…]

 unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.org/glossary.html#term-abstract-base-class) for objects representing a file system path,
e.g.[`pathlib.PurePath`](https://docs.python.org/pathlib.html#pathlib.PurePath) .Added in version 3.6.

- 
os.getenv(*key* ,*default=None* )[¶](https://docs.python.org#os.getenv)
- Return the value of the environment variable *key* as a string if it exists, or*default* if it doesn’t.*key* is a string. Note that
since`getenv()` uses[`os.environ`](https://docs.python.org#os.environ) , the mapping of`getenv()` is
similarly also captured on import, and the function may not reflect
future environment changes.On Unix, keys and values are decoded with [`sys.getfilesystemencoding()`](https://docs.python.org/sys.html#sys.getfilesystemencoding) and`'surrogateescape'` error handler. Use[`os.getenvb()`](https://docs.python
```

**[local-http]** (1.98s, 32000 chars, tier http; wr=1.0, wo=None; hdr 1, code 0, links 21, lists 11)
```
---
title: os — Miscellaneous operating system interfaces
url: https://docs.python.org/3/library/os.html
hostname: python.org
description: "Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..."
sitename: Python documentation
date: "2016-06-02"
---
# `os` — Miscellaneous operating system interfaces[¶](https://docs.python.org#module-os)

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a threat to

[…середина…]

 unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.org/glossary.html#term-abstract-base-class) for objects representing a file system path,
e.g.[`pathlib.PurePath`](https://docs.python.org/pathlib.html#pathlib.PurePath) .Added in version 3.6.

- 
os.getenv(*key* ,*default=None* )[¶](https://docs.python.org#os.getenv)
- Return the value of the environment variable *key* as a string if it exists, or*default* if it doesn’t.*key* is a string. Note that
since`getenv()` uses[`os.environ`](https://docs.python.org#os.environ) , the mapping of`getenv()` is
similarly also captured on import, and the function may not reflect
future environment changes.On Unix, keys and values are decoded with [`sys.getfilesystemencoding()`](https://docs.python.org/sys.html#sys.getfilesystemencoding) and`'surrogateescape'` error handler. Use[`os.getenvb()`](https://docs.python
```

**[local-curl]** (2.35s, 32000 chars, tier curl; wr=1.0, wo=None; hdr 1, code 0, links 21, lists 11)
```
---
title: os — Miscellaneous operating system interfaces
url: https://docs.python.org/3/library/os.html
hostname: python.org
description: "Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..."
sitename: Python documentation
date: "2016-06-02"
---
# `os` — Miscellaneous operating system interfaces[¶](https://docs.python.org#module-os)

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a threat to

[…середина…]

 unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.org/glossary.html#term-abstract-base-class) for objects representing a file system path,
e.g.[`pathlib.PurePath`](https://docs.python.org/pathlib.html#pathlib.PurePath) .Added in version 3.6.

- 
os.getenv(*key* ,*default=None* )[¶](https://docs.python.org#os.getenv)
- Return the value of the environment variable *key* as a string if it exists, or*default* if it doesn’t.*key* is a string. Note that
since`getenv()` uses[`os.environ`](https://docs.python.org#os.environ) , the mapping of`getenv()` is
similarly also captured on import, and the function may not reflect
future environment changes.On Unix, keys and values are decoded with [`sys.getfilesystemencoding()`](https://docs.python.org/sys.html#sys.getfilesystemencoding) and`'surrogateescape'` error handler. Use[`os.getenvb()`](https://docs.python
```

**[local-browser]** (3.1s, 32000 chars, tier browser; wr=1.0, wo=None; hdr 1, code 0, links 21, lists 11)
```
---
title: os — Miscellaneous operating system interfaces
url: https://docs.python.org/3/library/os.html
hostname: python.org
description: "Source code: Lib/os.py This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, s..."
sitename: Python documentation
date: "2016-06-02"
---
# `os` — Miscellaneous operating system interfaces[¶](https://docs.python.org#module-os)

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a threat to

[…середина…]

 unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.org/glossary.html#term-abstract-base-class) for objects representing a file system path,
e.g.[`pathlib.PurePath`](https://docs.python.org/pathlib.html#pathlib.PurePath) .Added in version 3.6.

- 
os.getenv(*key* ,*default=None* )[¶](https://docs.python.org#os.getenv)
- Return the value of the environment variable *key* as a string if it exists, or*default* if it doesn’t.*key* is a string. Note that
since`getenv()` uses[`os.environ`](https://docs.python.org#os.environ) , the mapping of`getenv()` is
similarly also captured on import, and the function may not reflect
future environment changes.On Unix, keys and values are decoded with [`sys.getfilesystemencoding()`](https://docs.python.org/sys.html#sys.getfilesystemencoding) and`'surrogateescape'` error handler. Use[`os.getenvb()`](https://docs.python
```

**[firecrawl]** (11.54s, 32000 chars; wr=0.333, wo=None; hdr 2, code 0, links 28, lists 14)
```
### Navigation

- [index](https://docs.python.org/3/genindex.html "General Index")
- [modules](https://docs.python.org/3/py-modindex.html "Python Module Index") \|
- [next](https://docs.python.org/3/library/io.html "io — Core tools for working with streams") \|
- [previous](https://docs.python.org/3/library/allos.html "Generic Operating System Services") \|
- ![Python logo](https://docs.python.org/3/_static/py.svg)
- [Python](https://www.python.org/) »
- Greek \| ΕλληνικάEnglishSpanish \| españolFrench \| françaisItalian \| italianoJapanese \| 日本語Korean \| 한국어Polish \| polskiBrazilian Portuguese \| Português brasileiroRomanian \| RomâneșteRussian \| РусскийTurkish \| TürkçeSimplified Chinese \| 简体中文Traditional Chinese \| 繁體中文

dev (3.16)pre (3.15)3.14.73.133.123.113.103.93.83.73.63.53.43.33.23.13.02.72.6

- [3.14.7 Documentation](https://docs.python.org/3/index.html) »

- [The Python Standard Library](https://docs.python.org/3/library/index.html) »
- [Generic Operating System Services](https://docs.python.org/3/library/allos.html) »
- [`os` — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html)
- \|

- Theme
AutoLightDark \|

# `os` — Miscellaneous operating system interfaces [¶](https://docs.python.org/3/library/os.html\#module-os "Link to this heading")

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

* * *

This module provides a portable way of using operating system dependent
functionality. If you just want to read or write a file see [`open()`](https://docs.python.org/3/library/functions.html#open "open"), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/3/library/os.path.html#module-os.path "os.path: Operations on pathnames.") module, and if you want to
read all the 

[…середина…]

 vice versa).

`environb` is only available if [`supports_bytes_environ`](https://docs.python.org/3/library/os.html#os.supports_bytes_environ "os.supports_bytes_environ") is
`True`.

Added in version 3.2.

Changed in version 3.9: Updated to support [**PEP 584**](https://peps.python.org/pep-0584/)’s merge (`|`) and update (`|=`) operators.

os.reload\_environ() [¶](https://docs.python.org/3/library/os.html#os.reload_environ "Link to this definition")

The [`os.environ`](https://docs.python.org/3/library/os.html#os.environ "os.environ") and [`os.environb`](https://docs.python.org/3/library/os.html#os.environb "os.environb") mappings are a cache of
environment variables at the time that Python started.
As such, changes to the current process environment are not reflected
if made outside Python, or by [`os.putenv()`](https://docs.python.org/3/library/os.html#os.putenv "os.putenv") or [`os.unsetenv()`](https://docs.python.org/3/library/os.html#os.unsetenv "os.unsetenv").
Use `os.reload_environ()` to update `os.environ` and `os.environb`
with any such changes to the current process environment.

Warning

This function is not thread-safe. Calling it while the environment is
being modified
```

**[tavily]** (4.72s, 32000 chars; wr=0.667, wo=None; hdr 2, code 0, links 29, lists 14)
```
### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](io.html "io — Core tools for working with streams") |
* [previous](allos.html "Generic Operating System Services") |
* [Python](https://www.python.org/) »
* [3.14.7 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Generic Operating System Services](allos.html) »
* `os` — Miscellaneous operating system interfaces
* |
* |

# `os` — Miscellaneous operating system interfaces[¶](#module-os "Link to this heading")

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

---

This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see [`open()`](functions.html#open "open"), if you want to manipulate paths, see the [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.") module, and if you want to read all the lines in all the files on the command line see the [`fileinput`](fileinput.html#module-fileinput "fileinput: Loop over standard input or a list of files.") module. For creating temporary files and directories see the [`tempfile`](tempfile.html#module-tempfile "tempfile: Generate temporary files and directories.") module, and for high-level file and directory handling see the [`shutil`](shutil.html#module-shutil "shutil: High-level file operations, including copying.") module.

Notes on the availability of these functions:

* The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat information about *path* in the same format (which happens to 

[…середина…]

a file system path, e.g. [`pathlib.PurePath`](pathlib.html#pathlib.PurePath "pathlib.PurePath").

    Added in version 3.6.

    *abstractmethod* \_\_fspath\_\_()[¶](#os.PathLike.__fspath__ "Link to this definition")
    :   Return the file system path representation of the object.

        The method should only return a [`str`](stdtypes.html#str "str") or [`bytes`](stdtypes.html#bytes "bytes") object, with the preference being for `str`.

os.getenv(*key*, *default=None*)[¶](#os.getenv "Link to this definition")
:   Return the value of the environment variable *key* as a string if it exists, or *default* if it doesn’t. *key* is a string. Note that since `getenv()` uses [`os.environ`](#os.environ "os.environ"), the mapping of `getenv()` is similarly also captured on import, and the function may not reflect future environment changes.

    On Unix, keys and values are decoded with [`sys.getfilesystemencoding()`](sys.html#sys.getfilesystemencoding "sys.getfilesystemencoding") and `'surrogateescape'` error handler. Use [`os.getenvb()`](#os.getenvb "os.getenvb") if you would like to use a different encoding.

    [Availability](intro.html#availability): Unix, Windows.

os.getenvb(*key*
```

**[jina]** (5.07s, 32000 chars; wr=0.333, wo=None; hdr 0, code 0, links 23, lists 5)
```
Title: os — Miscellaneous operating system interfaces

URL Source: https://docs.python.org/3/library/os.html

Published Time: Thu, 27 Aug 2026 11:52:47 GMT

Markdown Content:
**Source code:**[Lib/os.py](https://github.com/python/cpython/tree/3.14/Lib/os.py)

* * *

This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see [`open()`](https://docs.python.org/3/library/functions.html#open "open"), if you want to manipulate paths, see the [`os.path`](https://docs.python.org/3/library/os.path.html#module-os.path "os.path: Operations on pathnames.") module, and if you want to read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/3/library/fileinput.html#module-fileinput "fileinput: Loop over standard input or a list of files.") module. For creating temporary files and directories see the [`tempfile`](https://docs.python.org/3/library/tempfile.html#module-tempfile "tempfile: Generate temporary files and directories.") module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/3/library/shutil.html#module-shutil "shutil: High-level file operations, including copying.") module.

Notes on the availability of these functions:

*   The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat information about _path_ in the same format (which happens to have originated with the POSIX interface).

*   Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a threat to portability.

*   All functions accept

[…середина…]

fined behavior. Reading from [`os.environ`](https://docs.python.org/3/library/os.html#os.environ "os.environ") or [`os.environb`](https://docs.python.org/3/library/os.html#os.environb "os.environb"), or calling [`os.getenv()`](https://docs.python.org/3/library/os.html#os.getenv "os.getenv") while reloading, may return an empty result.

Added in version 3.14.

os.chdir(_path_)os.fchdir(_fd_)os.getcwd()
These functions are described in [Files and Directories](https://docs.python.org/3/library/os.html#os-file-dir).

os.fsencode(_filename_)[¶](https://docs.python.org/3/library/os.html#os.fsencode "Link to this definition")
Encode [path-like](https://docs.python.org/3/glossary.html#term-path-like-object)_filename_ to the [filesystem encoding and error handler](https://docs.python.org/3/glossary.html#term-filesystem-encoding-and-error-handler); return [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "bytes") unchanged.

[`fsdecode()`](https://docs.python.org/3/library/os.html#os.fsdecode "os.fsdecode") is the reverse function.

Added in version 3.2.

Changed in version 3.6: Support added to accept objects implementing the [`os.PathLike`](https://docs.python.org/3/library/o
```

**[parallel]** (6.65s, 15342 chars; wr=0.333, wo=None; hdr 2, code 0, links 2, lists 1)
```
# `os` — Miscellaneous operating system interfaces ¶
This module provides a portable way of using operating system dependent
functionality. If you just want to read or write a file see `open()` , if
you want to manipulate paths, see the `os.path` module, and if you want to

...

* On WebAssembly platforms, Android and iOS, large parts of the `os` module are
not available or behave differently. APIs related to processes (e.g. `fork()` , `execve()` ) and resources (e.g. `nice()` )
are not available. Others like `getuid()` and `getpid()` are
emulated or stubs.

...

Note
All functions in this module raise `OSError` (or subclasses thereof) in
the case of invalid or inaccessible file names and paths, or other arguments
that have the correct type, but are not accepted by the operating system.
_exception_ os. error ¶
An alias for the built-in `OSError` exception.
os. name ¶
The name of the operating system dependent module imported. The following
names have currently been registered: `'posix'` , `'nt'` , `'java'` .
See also
`sys.platform` has a finer granularity. `os.uname()` gives
system-dependent version information.
The `platform` module provides detailed checks for the
system’s identity.

...

## Process Parameters ¶
See also the `os.reload_environ()` function.
Note
On some platforms, including FreeBSD and macOS, setting `environ` may
cause memory leaks. Refer to the system documentation for `putenv()` .
Raises an auditing event `os.putenv` with arguments `key` , `value` .

...

On macOS, the length of _groups_ may not exceed the
system-defined maximum number of effective group ids, typically 16.
See the documentation for `getgroups()` for cases where it may not
return the same group list set by calling setgroups().
os. setns ( _fd_ , _nstype = 0_ ) ¶
Reassociate the curre

[…середина…]

 a file descriptor ; the file descriptor must refer to a directory.
Raises an auditing event `os.scandir` with argument `path` .
The `scandir()` iterator supports the context manager protocol
and has the following method:

...

Added in version 3.5.
Changed in version 3.6: Added support for the context manager protocol and the `close()` method. If a `scandir()` iterator is neither
exhausted nor explicitly closed a `ResourceWarning` will be emitted
in its destructor.
The function accepts a path-like object .

...

Because the `os.DirEntry` methods can make operating system calls, they may
also raise `OSError` . If you need very fine-grained
control over errors, you can catch `OSError` when calling one of the `os.DirEntry` methods and handle as appropriate.
To be directly usable as a path-like object , `os.DirEntry` implements the `PathLike` interface.
`DirEntry` objects are generic over the type of the
path ( `str` or `bytes` ).
Attributes and methods on a `os.DirEntry` instance are as follows:

...

This method can raise `OSError` , such as `PermissionError` ,
but `FileNotFoundError` is caught and not raised.

...

This method can raise `OSError` , such as `PermissionError` ,
but `
```

## U3: https://www.rfc-editor.org/rfc/rfc9110.html
_(note: RFC, 1.2MB html, чистая статика)_

**[local-auto]** (2.16s, 9140 chars, tier http; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
```
---
title: HTTP Semantics
author: Roy T Fielding; Mark Nottingham; Julian Reschke
url: https://www.rfc-editor.org/rfc/rfc9110.html
hostname: rfc-editor.org
description: The Hypertext Transfer Protocol (HTTP) is a stateless application-level protocol for distributed, collaborative, hypertext information systems. This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the protocol that are shared by all versions. In this definition are core protocol elements, extensibility mechanisms, and the "http" and "https" Uniform Resource Identifier (URI) schemes. This document updates RFC 3864 and obsoletes RFCs 2818, 7231, 7232, 7233, 7235, 7538, 7615, 7694, and portions of 7230.
sitename: rfc-editor.org
date: "1998-04-01"
---
### 
[6.4.](https://www.rfc-editor.org#section-6.4) [Content](https://www.rfc-editor.org#name-content)
        

        
   HTTP messages often transfer a complete or partial representation as the
   message "content": a stream of octets sent after the header
   section, as delineated by the message framing.[¶](https://www.rfc-editor.org#section-6.4-1)

   This abstract definition of content reflects the data after it has been
   extracted from the message framing. For example, an HTTP/1.1 message body
   ([Section 6](https://www.rfc-editor.org/rfc/rfc9112#section-6) of [[HTTP/1.1](https://www.rfc-editor.org#HTTP11)]) might consist of a stream of data encoded
   with the chunked transfer coding -- a sequence of data chunks, one
   zero-length chunk, and a trailer section -- whereas
   the content of that same message
   includes only the data stream after the transfer coding has been decoded;
   it does not include the chunk lengths, chunked framing syntax, nor the
   trailer fields ([Section 6.5](htt

[…середина…]

itor.org#status.206) response to GET
   contains either a single part of the selected representation or a
   multipart message body containing multiple parts of that representation,
   as described in [Section 15.3.7](https://www.rfc-editor.org#status.206).[¶](https://www.rfc-editor.org#section-6.4.1-4)

   Response messages with an error status code usually contain content that
   represents the error condition, such that the content describes the
   error state and what steps are suggested for resolving it.[¶](https://www.rfc-editor.org#section-6.4.1-5)

   Responses to the HEAD request method ([Section 9.3.2](https://www.rfc-editor.org#HEAD)) never include
   content; the associated response header fields indicate only
   what their values would have been if the request method had been GET
   ([Section 9.3.1](https://www.rfc-editor.org#GET)).[¶](https://www.rfc-editor.org#section-6.4.1-6)

                  [2xx (Successful)](https://www.rfc-editor.org#status.2xx) responses to a CONNECT request method
   ([Section 9.3.6](https://www.rfc-editor.org#CONNECT)) switch the connection to tunnel mode instead of
   having content.[¶](https://www.rfc-editor.org#section-6.4.1-7)

   All [
```

**[local-http]** (2.24s, 9140 chars, tier http; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
```
---
title: HTTP Semantics
author: Roy T Fielding; Mark Nottingham; Julian Reschke
url: https://www.rfc-editor.org/rfc/rfc9110.html
hostname: rfc-editor.org
description: The Hypertext Transfer Protocol (HTTP) is a stateless application-level protocol for distributed, collaborative, hypertext information systems. This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the protocol that are shared by all versions. In this definition are core protocol elements, extensibility mechanisms, and the "http" and "https" Uniform Resource Identifier (URI) schemes. This document updates RFC 3864 and obsoletes RFCs 2818, 7231, 7232, 7233, 7235, 7538, 7615, 7694, and portions of 7230.
sitename: rfc-editor.org
date: "1998-04-01"
---
### 
[6.4.](https://www.rfc-editor.org#section-6.4) [Content](https://www.rfc-editor.org#name-content)
        

        
   HTTP messages often transfer a complete or partial representation as the
   message "content": a stream of octets sent after the header
   section, as delineated by the message framing.[¶](https://www.rfc-editor.org#section-6.4-1)

   This abstract definition of content reflects the data after it has been
   extracted from the message framing. For example, an HTTP/1.1 message body
   ([Section 6](https://www.rfc-editor.org/rfc/rfc9112#section-6) of [[HTTP/1.1](https://www.rfc-editor.org#HTTP11)]) might consist of a stream of data encoded
   with the chunked transfer coding -- a sequence of data chunks, one
   zero-length chunk, and a trailer section -- whereas
   the content of that same message
   includes only the data stream after the transfer coding has been decoded;
   it does not include the chunk lengths, chunked framing syntax, nor the
   trailer fields ([Section 6.5](htt

[…середина…]

itor.org#status.206) response to GET
   contains either a single part of the selected representation or a
   multipart message body containing multiple parts of that representation,
   as described in [Section 15.3.7](https://www.rfc-editor.org#status.206).[¶](https://www.rfc-editor.org#section-6.4.1-4)

   Response messages with an error status code usually contain content that
   represents the error condition, such that the content describes the
   error state and what steps are suggested for resolving it.[¶](https://www.rfc-editor.org#section-6.4.1-5)

   Responses to the HEAD request method ([Section 9.3.2](https://www.rfc-editor.org#HEAD)) never include
   content; the associated response header fields indicate only
   what their values would have been if the request method had been GET
   ([Section 9.3.1](https://www.rfc-editor.org#GET)).[¶](https://www.rfc-editor.org#section-6.4.1-6)

                  [2xx (Successful)](https://www.rfc-editor.org#status.2xx) responses to a CONNECT request method
   ([Section 9.3.6](https://www.rfc-editor.org#CONNECT)) switch the connection to tunnel mode instead of
   having content.[¶](https://www.rfc-editor.org#section-6.4.1-7)

   All [
```

**[local-curl]** (2.16s, 9140 chars, tier curl; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
```
---
title: HTTP Semantics
author: Roy T Fielding; Mark Nottingham; Julian Reschke
url: https://www.rfc-editor.org/rfc/rfc9110.html
hostname: rfc-editor.org
description: The Hypertext Transfer Protocol (HTTP) is a stateless application-level protocol for distributed, collaborative, hypertext information systems. This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the protocol that are shared by all versions. In this definition are core protocol elements, extensibility mechanisms, and the "http" and "https" Uniform Resource Identifier (URI) schemes. This document updates RFC 3864 and obsoletes RFCs 2818, 7231, 7232, 7233, 7235, 7538, 7615, 7694, and portions of 7230.
sitename: rfc-editor.org
date: "1998-04-01"
---
### 
[6.4.](https://www.rfc-editor.org#section-6.4) [Content](https://www.rfc-editor.org#name-content)
        

        
   HTTP messages often transfer a complete or partial representation as the
   message "content": a stream of octets sent after the header
   section, as delineated by the message framing.[¶](https://www.rfc-editor.org#section-6.4-1)

   This abstract definition of content reflects the data after it has been
   extracted from the message framing. For example, an HTTP/1.1 message body
   ([Section 6](https://www.rfc-editor.org/rfc/rfc9112#section-6) of [[HTTP/1.1](https://www.rfc-editor.org#HTTP11)]) might consist of a stream of data encoded
   with the chunked transfer coding -- a sequence of data chunks, one
   zero-length chunk, and a trailer section -- whereas
   the content of that same message
   includes only the data stream after the transfer coding has been decoded;
   it does not include the chunk lengths, chunked framing syntax, nor the
   trailer fields ([Section 6.5](htt

[…середина…]

itor.org#status.206) response to GET
   contains either a single part of the selected representation or a
   multipart message body containing multiple parts of that representation,
   as described in [Section 15.3.7](https://www.rfc-editor.org#status.206).[¶](https://www.rfc-editor.org#section-6.4.1-4)

   Response messages with an error status code usually contain content that
   represents the error condition, such that the content describes the
   error state and what steps are suggested for resolving it.[¶](https://www.rfc-editor.org#section-6.4.1-5)

   Responses to the HEAD request method ([Section 9.3.2](https://www.rfc-editor.org#HEAD)) never include
   content; the associated response header fields indicate only
   what their values would have been if the request method had been GET
   ([Section 9.3.1](https://www.rfc-editor.org#GET)).[¶](https://www.rfc-editor.org#section-6.4.1-6)

                  [2xx (Successful)](https://www.rfc-editor.org#status.2xx) responses to a CONNECT request method
   ([Section 9.3.6](https://www.rfc-editor.org#CONNECT)) switch the connection to tunnel mode instead of
   having content.[¶](https://www.rfc-editor.org#section-6.4.1-7)

   All [
```

**[local-browser]** (3.85s, 9140 chars, tier browser; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
```
---
title: HTTP Semantics
author: Roy T Fielding; Mark Nottingham; Julian Reschke
url: https://www.rfc-editor.org/rfc/rfc9110.html
hostname: rfc-editor.org
description: The Hypertext Transfer Protocol (HTTP) is a stateless application-level protocol for distributed, collaborative, hypertext information systems. This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the protocol that are shared by all versions. In this definition are core protocol elements, extensibility mechanisms, and the "http" and "https" Uniform Resource Identifier (URI) schemes. This document updates RFC 3864 and obsoletes RFCs 2818, 7231, 7232, 7233, 7235, 7538, 7615, 7694, and portions of 7230.
sitename: rfc-editor.org
date: "1998-04-01"
---
### 
[6.4.](https://www.rfc-editor.org#section-6.4) [Content](https://www.rfc-editor.org#name-content)
        

        
   HTTP messages often transfer a complete or partial representation as the
   message "content": a stream of octets sent after the header
   section, as delineated by the message framing.[¶](https://www.rfc-editor.org#section-6.4-1)

   This abstract definition of content reflects the data after it has been
   extracted from the message framing. For example, an HTTP/1.1 message body
   ([Section 6](https://www.rfc-editor.org/rfc/rfc9112#section-6) of [[HTTP/1.1](https://www.rfc-editor.org#HTTP11)]) might consist of a stream of data encoded
   with the chunked transfer coding -- a sequence of data chunks, one
   zero-length chunk, and a trailer section -- whereas
   the content of that same message
   includes only the data stream after the transfer coding has been decoded;
   it does not include the chunk lengths, chunked framing syntax, nor the
   trailer fields ([Section 6.5](htt

[…середина…]

itor.org#status.206) response to GET
   contains either a single part of the selected representation or a
   multipart message body containing multiple parts of that representation,
   as described in [Section 15.3.7](https://www.rfc-editor.org#status.206).[¶](https://www.rfc-editor.org#section-6.4.1-4)

   Response messages with an error status code usually contain content that
   represents the error condition, such that the content describes the
   error state and what steps are suggested for resolving it.[¶](https://www.rfc-editor.org#section-6.4.1-5)

   Responses to the HEAD request method ([Section 9.3.2](https://www.rfc-editor.org#HEAD)) never include
   content; the associated response header fields indicate only
   what their values would have been if the request method had been GET
   ([Section 9.3.1](https://www.rfc-editor.org#GET)).[¶](https://www.rfc-editor.org#section-6.4.1-6)

                  [2xx (Successful)](https://www.rfc-editor.org#status.2xx) responses to a CONNECT request method
   ([Section 9.3.6](https://www.rfc-editor.org#CONNECT)) switch the connection to tunnel mode instead of
   having content.[¶](https://www.rfc-editor.org#section-6.4.1-7)

   All [
```

**[firecrawl]** (8.01s, 32000 chars; wr=0.0, wo=0.0; hdr 4, code 0, links 41, lists 0)
```
| RFC 9110 | HTTP Semantics | June 2022 |
| --- | --- | --- |
| Fielding, et al. | Standards Track | \[Page\] |

Status:Internet StandardObsoletes:[2818](https://www.rfc-editor.org/rfc/rfc2818), [7230](https://www.rfc-editor.org/rfc/rfc7230), [7231](https://www.rfc-editor.org/rfc/rfc7231), [7232](https://www.rfc-editor.org/rfc/rfc7232), [7233](https://www.rfc-editor.org/rfc/rfc7233), [7235](https://www.rfc-editor.org/rfc/rfc7235), [7538](https://www.rfc-editor.org/rfc/rfc7538), [7615](https://www.rfc-editor.org/rfc/rfc7615), [7694](https://www.rfc-editor.org/rfc/rfc7694)Updates:[3864](https://www.rfc-editor.org/rfc/rfc3864)More info:[Errata exist](https://www.rfc-editor.org/errata/rfc9110) \| [Datatracker](https://datatracker.ietf.org/doc/rfc9110) \| [IPR](https://datatracker.ietf.org/ipr/search/?rfc=9110&submit=rfc) \| [Info page](https://www.rfc-editor.org/info/rfc9110)

Stream:Internet Engineering Task Force (IETF)RFC:[9110](https://www.rfc-editor.org/rfc/rfc9110)STD:97Obsoletes:[2818](https://www.rfc-editor.org/rfc/rfc2818), [7230](https://www.rfc-editor.org/rfc/rfc7230), [7231](https://www.rfc-editor.org/rfc/rfc7231), [7232](https://www.rfc-editor.org/rfc/rfc7232), [7233](https://www.rfc-editor.org/rfc/rfc7233), [7235](https://www.rfc-editor.org/rfc/rfc7235), [7538](https://www.rfc-editor.org/rfc/rfc7538), [7615](https://www.rfc-editor.org/rfc/rfc7615), [7694](https://www.rfc-editor.org/rfc/rfc7694)Updates:[3864](https://www.rfc-editor.org/rfc/rfc3864)Category:Standards TrackPublished:June 2022ISSN:2070-1721Authors:

R. Fielding, Ed.

Adobe

M. Nottingham, Ed.

Fastly

J. Reschke, Ed.

greenbytes

# RFC 9110

# HTTP Semantics

## [Abstract](https://www.rfc-editor.org/rfc/rfc9110.html\#abstract)

The Hypertext Transfer Protocol (HTTP) is a stateless application-leve

[…середина…]

mance](https://www.rfc-editor.org/rfc/rfc9110.html\#name-conformance)

### [2.1.](https://www.rfc-editor.org/rfc/rfc9110.html\#section-2.1) [Syntax Notation](https://www.rfc-editor.org/rfc/rfc9110.html\#name-syntax-notation)

This specification uses the Augmented Backus-Naur Form (ABNF) notation of
\[ [RFC5234](https://www.rfc-editor.org/rfc/rfc9110.html#RFC5234)\], extended with the notation for case-sensitivity
in strings defined in \[ [RFC7405](https://www.rfc-editor.org/rfc/rfc9110.html#RFC7405)\]. [¶](https://www.rfc-editor.org/rfc/rfc9110.html#section-2.1-1)

It also uses a list extension, defined in [Section 5.6.1](https://www.rfc-editor.org/rfc/rfc9110.html#abnf.extension),
that allows for compact definition of comma-separated lists using a "#"
operator (similar to how the "\*" operator indicates repetition). [Appendix A](https://www.rfc-editor.org/rfc/rfc9110.html#collected.abnf) shows the collected grammar with all list
operators expanded to standard ABNF notation. [¶](https://www.rfc-editor.org/rfc/rfc9110.html#section-2.1-2)

As a convention, ABNF rule names prefixed with "obs-" denote
obsolete grammar rules that appear for historical reasons. [¶](https://www.rfc-editor
```

**[tavily]** (7.53s, 0 chars; wr=0.0, wo=0.0; hdr 0, code 0, links 0, lists 0)
```
(пустой вывод, <200 симв.)
```

**[jina]** (2.37s, 32000 chars; wr=0.0, wo=0.0; hdr 4, code 0, links 34, lists 12)
```
Title: RFC 9110: HTTP Semantics

URL Source: https://www.rfc-editor.org/rfc/rfc9110.html

Markdown Content:
RFC 9110 HTTP Semantics June 2022
Fielding, et al.Standards Track[Page]

## HTTP Semantics

## [Abstract](https://www.rfc-editor.org/rfc/rfc9110.html#abstract)

The Hypertext Transfer Protocol (HTTP) is a stateless application-level protocol for distributed, collaborative, hypertext information systems. This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the protocol that are shared by all versions. In this definition are core protocol elements, extensibility mechanisms, and the "http" and "https" Uniform Resource Identifier (URI) schemes.[¶](https://www.rfc-editor.org/rfc/rfc9110.html#section-abstract-1)

This document updates RFC 3864 and obsoletes RFCs 2818, 7231, 7232, 7233, 7235, 7538, 7615, 7694, and portions of 7230.[¶](https://www.rfc-editor.org/rfc/rfc9110.html#section-abstract-2)

## [Status of This Memo](https://www.rfc-editor.org/rfc/rfc9110.html#name-status-of-this-memo)

This is an Internet Standards Track document.[¶](https://www.rfc-editor.org/rfc/rfc9110.html#section-boilerplate.1-1)

This document is a product of the Internet Engineering Task Force (IETF). It represents the consensus of the IETF community. It has received public review and has been approved for publication by the Internet Engineering Steering Group (IESG). Further information on Internet Standards is available in Section 2 of RFC 7841.[¶](https://www.rfc-editor.org/rfc/rfc9110.html#section-boilerplate.1-2)

Information about the current status of this document, any errata, and how to provide feedback on it may be obtained at [https://www.rfc-editor.org/info/rfc9110](https://www.rfc-editor.org/info/rfc9110).[¶](https://w

[…середина…]

 Proxy](https://www.rfc-editor.org/rfc/rfc9110.html#name-to-a-proxy)

        *   [7.3.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.3.3).[To the Origin](https://www.rfc-editor.org/rfc/rfc9110.html#name-to-the-origin)

    *   [7.4](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.4).[Rejecting Misdirected Requests](https://www.rfc-editor.org/rfc/rfc9110.html#name-rejecting-misdirected-reque)

    *   [7.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.5).[Response Correlation](https://www.rfc-editor.org/rfc/rfc9110.html#name-response-correlation)

    *   [7.6](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.6).[Message Forwarding](https://www.rfc-editor.org/rfc/rfc9110.html#name-message-forwarding)

        *   [7.6.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.6.1).[Connection](https://www.rfc-editor.org/rfc/rfc9110.html#name-connection)

        *   [7.6.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.6.2).[Max-Forwards](https://www.rfc-editor.org/rfc/rfc9110.html#name-max-forwards)

        *   [7.6.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.6.3).[Via](https://www.rfc-editor.org/rfc/rfc9110.html#name-via)

    *  
```

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U4: https://www.sqlite.org/changes.html
_(note: длинный changelog, плотный текст)_

**[local-auto]** (1.69s, 32000 chars, tier http; wr=1.0, wo=None; hdr 5, code 0, links 21, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-07-24"
---
![SQLite](images/sqlite370_banner.svg) 

Small. Fast. Reliable.

Choose any three.

 
# Release History

This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at
[https://sqlite.org/src/timeline](https://sqlite.org/src/timeline) and
[https://sqlite.org/src/timeline?t=release](https://sqlite.org/src/timeline?t=release).
See the [chronology](https://www.sqlite.org/chronology.html) a succinct listing of releases.

### 2026-07-24 (3.53.4)

1.  Fixes for problems in 3.53.0 (and 3.53.1, 3.53.2, and 3.53.3) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.4&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc
3. SHA3-256 for sqlite3.c: 67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16

### 2026-06-26 (3.53.3)

1.  Fixes for problems in 3.53.0 (and 3.53.1 and 3.53.2) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.3&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-26 20:14:12 d4c0e51e4aeb96955b99185ab9cde75c339e2c29c3f3f12428d364a10d782c62
3. SHA3-256 for sqlite3.c: 28e484abdaa43630e34040ef6ed92be973a1ad54107803d8af5145b889c23ed7

### 2026-06-03 (3.53.2)

1.  Fixes for problems in 3.53.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.2&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-03 19:12:13 d6e03d8c777c

[…середина…]

.  Faster window function queries when using 
         "`BETWEEN :x FOLLOWING AND :y FOLLOWING` " with a large :y.
7. Add the [PRAGMA wal_checkpoint=NOOP;](https://www.sqlite.org/pragma.html#pragma_wal_checkpoint) command and the[SQLITE_CHECKPOINT_NOOP](https://www.sqlite.org/c3ref/c_checkpoint_full.html) argument for[sqlite3_wal_checkpoint_v2()](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html) .
8. Add the [sqlite3_set_errmsg()](https://www.sqlite.org/c3ref/set_errmsg.html) API for use by extensions.
9. Add the [sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) API, which works just like the existing[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) API except that it returns 64-bit results.
10. Add the [SQLITE_DBSTATUS_TEMPBUF_SPILL](https://www.sqlite.org/c3ref/c_dbstatus_options.html) option to the[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) and[sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) interfaces.
11. In the [session extension](https://www.sqlite.org/sessionintro.html) add the[sqlite3changeset_apply_v3()](https://www.sqlite.org/session/sqlite3changeset_apply.html) interface.
12. For the [buil
```

**[local-http]** (1.71s, 32000 chars, tier http; wr=1.0, wo=None; hdr 5, code 0, links 21, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-07-24"
---
![SQLite](images/sqlite370_banner.svg) 

Small. Fast. Reliable.

Choose any three.

 
# Release History

This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at
[https://sqlite.org/src/timeline](https://sqlite.org/src/timeline) and
[https://sqlite.org/src/timeline?t=release](https://sqlite.org/src/timeline?t=release).
See the [chronology](https://www.sqlite.org/chronology.html) a succinct listing of releases.

### 2026-07-24 (3.53.4)

1.  Fixes for problems in 3.53.0 (and 3.53.1, 3.53.2, and 3.53.3) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.4&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc
3. SHA3-256 for sqlite3.c: 67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16

### 2026-06-26 (3.53.3)

1.  Fixes for problems in 3.53.0 (and 3.53.1 and 3.53.2) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.3&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-26 20:14:12 d4c0e51e4aeb96955b99185ab9cde75c339e2c29c3f3f12428d364a10d782c62
3. SHA3-256 for sqlite3.c: 28e484abdaa43630e34040ef6ed92be973a1ad54107803d8af5145b889c23ed7

### 2026-06-03 (3.53.2)

1.  Fixes for problems in 3.53.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.2&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-03 19:12:13 d6e03d8c777c

[…середина…]

.  Faster window function queries when using 
         "`BETWEEN :x FOLLOWING AND :y FOLLOWING` " with a large :y.
7. Add the [PRAGMA wal_checkpoint=NOOP;](https://www.sqlite.org/pragma.html#pragma_wal_checkpoint) command and the[SQLITE_CHECKPOINT_NOOP](https://www.sqlite.org/c3ref/c_checkpoint_full.html) argument for[sqlite3_wal_checkpoint_v2()](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html) .
8. Add the [sqlite3_set_errmsg()](https://www.sqlite.org/c3ref/set_errmsg.html) API for use by extensions.
9. Add the [sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) API, which works just like the existing[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) API except that it returns 64-bit results.
10. Add the [SQLITE_DBSTATUS_TEMPBUF_SPILL](https://www.sqlite.org/c3ref/c_dbstatus_options.html) option to the[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) and[sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) interfaces.
11. In the [session extension](https://www.sqlite.org/sessionintro.html) add the[sqlite3changeset_apply_v3()](https://www.sqlite.org/session/sqlite3changeset_apply.html) interface.
12. For the [buil
```

**[local-curl]** (1.74s, 32000 chars, tier curl; wr=1.0, wo=None; hdr 5, code 0, links 21, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-07-24"
---
![SQLite](images/sqlite370_banner.svg) 

Small. Fast. Reliable.

Choose any three.

 
# Release History

This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at
[https://sqlite.org/src/timeline](https://sqlite.org/src/timeline) and
[https://sqlite.org/src/timeline?t=release](https://sqlite.org/src/timeline?t=release).
See the [chronology](https://www.sqlite.org/chronology.html) a succinct listing of releases.

### 2026-07-24 (3.53.4)

1.  Fixes for problems in 3.53.0 (and 3.53.1, 3.53.2, and 3.53.3) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.4&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc
3. SHA3-256 for sqlite3.c: 67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16

### 2026-06-26 (3.53.3)

1.  Fixes for problems in 3.53.0 (and 3.53.1 and 3.53.2) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.3&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-26 20:14:12 d4c0e51e4aeb96955b99185ab9cde75c339e2c29c3f3f12428d364a10d782c62
3. SHA3-256 for sqlite3.c: 28e484abdaa43630e34040ef6ed92be973a1ad54107803d8af5145b889c23ed7

### 2026-06-03 (3.53.2)

1.  Fixes for problems in 3.53.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.2&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-03 19:12:13 d6e03d8c777c

[…середина…]

.  Faster window function queries when using 
         "`BETWEEN :x FOLLOWING AND :y FOLLOWING` " with a large :y.
7. Add the [PRAGMA wal_checkpoint=NOOP;](https://www.sqlite.org/pragma.html#pragma_wal_checkpoint) command and the[SQLITE_CHECKPOINT_NOOP](https://www.sqlite.org/c3ref/c_checkpoint_full.html) argument for[sqlite3_wal_checkpoint_v2()](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html) .
8. Add the [sqlite3_set_errmsg()](https://www.sqlite.org/c3ref/set_errmsg.html) API for use by extensions.
9. Add the [sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) API, which works just like the existing[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) API except that it returns 64-bit results.
10. Add the [SQLITE_DBSTATUS_TEMPBUF_SPILL](https://www.sqlite.org/c3ref/c_dbstatus_options.html) option to the[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) and[sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) interfaces.
11. In the [session extension](https://www.sqlite.org/sessionintro.html) add the[sqlite3changeset_apply_v3()](https://www.sqlite.org/session/sqlite3changeset_apply.html) interface.
12. For the [buil
```

**[local-browser]** (3.17s, 32000 chars, tier browser; wr=1.0, wo=None; hdr 5, code 0, links 21, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-07-24"
---
![SQLite](images/sqlite370_banner.svg) 

Small. Fast. Reliable.

Choose any three.

 
# Release History

This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at
[https://sqlite.org/src/timeline](https://sqlite.org/src/timeline) and
[https://sqlite.org/src/timeline?t=release](https://sqlite.org/src/timeline?t=release).
See the [chronology](https://www.sqlite.org/chronology.html) a succinct listing of releases.

### 2026-07-24 (3.53.4)

1.  Fixes for problems in 3.53.0 (and 3.53.1, 3.53.2, and 3.53.3) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.4&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc
3. SHA3-256 for sqlite3.c: 67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16

### 2026-06-26 (3.53.3)

1.  Fixes for problems in 3.53.0 (and 3.53.1 and 3.53.2) mostly coming from AIs.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.3&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-26 20:14:12 d4c0e51e4aeb96955b99185ab9cde75c339e2c29c3f3f12428d364a10d782c62
3. SHA3-256 for sqlite3.c: 28e484abdaa43630e34040ef6ed92be973a1ad54107803d8af5145b889c23ed7

### 2026-06-03 (3.53.2)

1.  Fixes for problems in 3.53.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.2&to2=branch-3.53&y=ci) for details.**Hashes:**
2. SQLITE_SOURCE_ID: 2026-06-03 19:12:13 d6e03d8c777c

[…середина…]

.  Faster window function queries when using 
         "`BETWEEN :x FOLLOWING AND :y FOLLOWING` " with a large :y.
7. Add the [PRAGMA wal_checkpoint=NOOP;](https://www.sqlite.org/pragma.html#pragma_wal_checkpoint) command and the[SQLITE_CHECKPOINT_NOOP](https://www.sqlite.org/c3ref/c_checkpoint_full.html) argument for[sqlite3_wal_checkpoint_v2()](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html) .
8. Add the [sqlite3_set_errmsg()](https://www.sqlite.org/c3ref/set_errmsg.html) API for use by extensions.
9. Add the [sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) API, which works just like the existing[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) API except that it returns 64-bit results.
10. Add the [SQLITE_DBSTATUS_TEMPBUF_SPILL](https://www.sqlite.org/c3ref/c_dbstatus_options.html) option to the[sqlite3_db_status()](https://www.sqlite.org/c3ref/db_status.html) and[sqlite3_db_status64()](https://www.sqlite.org/c3ref/db_status.html) interfaces.
11. In the [session extension](https://www.sqlite.org/sessionintro.html) add the[sqlite3changeset_apply_v3()](https://www.sqlite.org/session/sqlite3changeset_apply.html) interface.
12. For the [buil
```

**[firecrawl]** (4.31s, 32000 chars; wr=0.667, wo=None; hdr 5, code 0, links 22, lists 0)
```
[![SQLite](https://www.sqlite.org/images/sqlite370_banner.svg)](https://www.sqlite.org/index.html)

Small. Fast. Reliable.

Choose any three.

Search DocumentationSearch Changelog

# Release History

This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at
[https://sqlite.org/src/timeline](https://sqlite.org/src/timeline) and
[https://sqlite.org/src/timeline?t=release](https://sqlite.org/src/timeline?t=release).
See the [chronology](https://www.sqlite.org/chronology.html) a succinct listing of releases.

### 2026-07-24 (3.53.4)

1. Fixes for problems in 3.53.0 (and 3.53.1, 3.53.2, and 3.53.3) mostly coming from AIs. See the
    [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.4&to2=branch-3.53&y=ci)
    for details.

   **Hashes:**

2. SQLITE\_SOURCE\_ID: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc

3. SHA3-256 for sqlite3.c: 67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16


### 2026-06-26 (3.53.3)

1. Fixes for problems in 3.53.0 (and 3.53.1 and 3.53.2) mostly coming from AIs. See the
    [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.3&to2=branch-3.53&y=ci)
    for details.

   **Hashes:**

2. SQLITE\_SOURCE\_ID: 2026-06-26 20:14:12 d4c0e51e4aeb96955b99185ab9cde75c339e2c29c3f3f12428d364a10d782c62

3. SHA3-256 for sqlite3.c: 28e484abdaa43630e34040ef6ed92be973a1ad54107803d8af5145b889c23ed7


### 2026-06-03 (3.53.2)

1. Fixes for problems in 3.53.0 reported by users. See the
    [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.2&to2=branch-3.53&y=ci)
    for details.

   **Hashes:**

2. SQLITE\_SOURCE\_ID: 2026-06-03 19:12:13 d6e03d8c777cfa2d35e

[…середина…]

ression.

    4. Faster window function queries when using
        " `BETWEEN :x FOLLOWING AND :y FOLLOWING`" with a large :y.
07. Add the [PRAGMA wal\_checkpoint=NOOP;](https://www.sqlite.org/pragma.html#pragma_wal_checkpoint) command and the
     [SQLITE\_CHECKPOINT\_NOOP](https://www.sqlite.org/c3ref/c_checkpoint_full.html) argument for [sqlite3\_wal\_checkpoint\_v2()](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html).

08. Add the [sqlite3\_set\_errmsg()](https://www.sqlite.org/c3ref/set_errmsg.html) API for use by extensions.

09. Add the [sqlite3\_db\_status64()](https://www.sqlite.org/c3ref/db_status.html) API, which works just like the existing
     [sqlite3\_db\_status()](https://www.sqlite.org/c3ref/db_status.html) API except that it returns 64-bit results.

10. Add the [SQLITE\_DBSTATUS\_TEMPBUF\_SPILL](https://www.sqlite.org/c3ref/c_dbstatus_options.html) option to the [sqlite3\_db\_status()](https://www.sqlite.org/c3ref/db_status.html)
     and [sqlite3\_db\_status64()](https://www.sqlite.org/c3ref/db_status.html) interfaces.

11. In the [session extension](https://www.sqlite.org/sessionintro.html) add the [sqlite3changeset\_apply\_v3()](https://www.sqlite.org/sessi
```

**[tavily]** (14.01s, 32000 chars; wr=0.333, wo=None; hdr 7, code 0, links 24, lists 14)
```
[![SQLite](images/sqlite370_banner.svg)](index.html) 

Small. Fast. Reliable.  
Choose any three.

* [Home](index.html)
* [Menu](javascript:void(0))
* [About](about.html)
* [Documentation](docs.html)
* [Download](download.html)
* [License](copyright.html)
* [Support](support.html)
* [Purchase](prosupport.html)
* [Search](javascript:void(0))

* [About](about.html)
* [Documentation](docs.html)
* [Download](download.html)
* [Support](support.html)
* [Purchase](prosupport.html)

# Release History

This page provides a high-level summary of changes to SQLite. For more detail, see the Fossil checkin logs at <https://sqlite.org/src/timeline> and <https://sqlite.org/src/timeline?t=release>. See the [chronology](chronology.html) a succinct listing of releases.

### 2026-07-24 (3.53.4)

1. Fixes for problems in 3.53.0 (and 3.53.1, 3.53.2, and 3.53.3) mostly coming from AIs. See the [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.4&to2=branch-3.53&y=ci) for details.

   **Hashes:**
2. SQLITE\_SOURCE\_ID: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc
3. SHA3-256 for sqlite3.c: 67f423e9ebbbdc473cbc4772c872ee6b89f31fde4ed0279a5c25d5f65c043a16

### 2026-06-26 (3.53.3)

1. Fixes for problems in 3.53.0 (and 3.53.1 and 3.53.2) mostly coming from AIs. See the [check-in timeline](https://sqlite.org/src/timeline?from=version-3.53.0&to=version-3.53.3&to2=branch-3.53&y=ci) for details.

   **Hashes:**
2. SQLITE\_SOURCE\_ID: 2026-06-26 20:14:12 d4c0e51e4aeb96955b99185ab9cde75c339e2c29c3f3f12428d364a10d782c62
3. SHA3-256 for sqlite3.c: 28e484abdaa43630e34040ef6ed92be973a1ad54107803d8af5145b889c23ed7

### 2026-06-03 (3.53.2)

1. Fixes for problems in 3.53.0 reported by users. See the [check-in timeline](https://sqlite

[…середина…]

3587cadd1b2684defb4f39fa58dca14b16162d4237e50af9afa

### 2025-07-30 (3.50.4)

1. Fix two long-standings cases of the use of uninitialized variables in obscure circumstances.

   **Hashes:**
2. SQLITE\_SOURCE\_ID: 2025-07-30 19:33:53 4d8adfb30e03f9cf27f800a2c1ba3c48fb4ca1b08b0f5ed59a4d5ecbf45e20a3
3. SHA3-256 for sqlite3.c: 9145255e83da6529e70121ee4d7a4c88fe83ca4511da0c9ed13d10842df36782

### 2025-07-17 (3.50.3)

1. Fix a possible memory error that can occur if a query is made against against FTS5 index that has been deliberately corrupted in a very specific way.
2. Fix the parser so that it ignored SQL comments in all places of a CREATE TRIGGER statement. This resolves a problem that was introduced by the introduction of the SQLITE\_DBCONFIG\_ENABLE\_COMMENTS feature in version 3.49.0.
3. Fix an incorrect answer due to over-optimization of an AND operator. [Forum post f4878de3e](https://sqlite.org/forum/forumpost/f4878de3e7dd4764).
4. Fix minor makefile issues and documentation typos.

   **Hashes:**
5. SQLITE\_SOURCE\_ID: 2025-07-17 13:25:10 3ce993b8657d6d9deda380a93cdd6404a8c8ba1b185b2bc423703e41ae5f2543
6. SHA3-256 for sqlite3.c: 934fafe96caa7f4c16e82e0c2b674441a715c038acc9780bf
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://www.sqlite.org/changes.html: jina: jina 422"}

**[parallel]** (7.43s, 17363 chars; wr=0.333, wo=None; hdr 10, code 0, links 4, lists 0)
```
# Release History
This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at https://sqlite.org/src/timeline and https://sqlite.org/src/timeline?t=release .
See the chronology a succinct listing of releases.

...

## 2026-07-24 (3.53.4)
### 2025-06-28 (3.50.2)
Avoid writing frames with no checksums into the wal file if a savepoint
is rolled back after dirty pages have already been spilled into the
wal file. [Forum post b490f726db](https://sqlite.org/forum/forumpost/b490f726db) .
4. Fix the Bitvec object to avoid stack overflow when the database is within
60 pages of its maximum size.
5. Fix a problem with UPDATEs on fts5 tables that contain BLOB values.
6. Fix an issue with transitive IS constraints on a RIGHT JOIN.
7. Raise an error early if the number of aggregate terms in a query
exceeds the maximum number of columns, to avoid downstream assertion
faults.
8.

...

### 2025-06-06 (3.50.1)
page not being transferred for the replicate database.
4. Query planner optimization: Allow the right-hand side of a LEFT JOIN
to be flattened even if it is a virtual table.
5. Fix sqlite3_setlk_timeout() to use a blocking lock when opening a
snapshot transaction and when blocked by another process running recovery.
6.

...

### 2025-05-29 (3.50.0)
the full pathname of the sqlite3_rsync executable on the remote side
as long as you install the sqlite3_rsync executable in
one of these directories: $HOME/bin:/usr/local/bin:/opt/homebrew/bin
7. Changes to JSON functions:
1. Bug fix: Enforce the JSON5 restriction that the
"\0" escape must not be followed by a digit.
2.

...

JSONB object unchanged and to modify as few bytes as possible on the interior
of the object. This helps reduce I/O as it allows SQLite to write only
the page that con

[…середина…]

lite3_normalized_sql() interface works on any prepared statement
created using sqlite3_prepare_v2() or sqlite3_prepare_v3() . It is no

...

### 2018-09-15 (3.25.0)
"a=99 AND b=a" into "a=99 AND b=99".
4. Use a separate mutex on every inode in the unix VFS , rather than
a single mutex shared among them all, for slightly better concurrency
in multi-threaded environments.
5. Enhance the PRAGMA integrity_check command for improved detection
of problems on the page freelist.
6.

...

### 2018-06-04 (3.24.0)
13. UPDATE avoids unnecessary low-level disk writes when the contents
of the database file do not actually change.
For example, "UPDATE t1 SET x=25 WHERE y=?" generates no extra
disk I/O if the value in column x is already 25. Similarly,
when doing UPDATE on records that span multiple pages, only
the subset of pages that actually change are written to disk.
This is a low-level performance optimization only and does not
affect the behavior of TRIGGERs or other higher level SQL
structures.
14. Queries that use ORDER BY and LIMIT now try to avoid computing
rows that cannot possibly come in under the LIMIT.

...

### 2018-04-02 (3.23.0)
sqlite_sequence table root page is really a btree-
```
