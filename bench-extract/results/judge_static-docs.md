# scenario: static-docs

## U1: https://example.com
_(note: тривиальная крошечная страница)_

**[local-auto]** ERROR: network/

**[local-http]** ERROR: extract_failed/

**[local-curl]** ERROR: extract_failed/

**[local-browser]** ERROR: network/

**[firecrawl]** (1.13s, 959 chars; wr=0.5, wo=1.0; hdr 0, code 0, links 1, lists 0)
```
This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring purposes.

هذا النطاق مُخصص للاستخدام في أمثلة التوثيق دون الحاجة إلى إذن. هذه ليست خدمة، يُرجى تجنب الاعتماد عليها لأغراض الاختبار والمراقبة.

该域名仅用于文档示例，无需获得许可。这并非一项服务，请勿将其用于测试和监控目的。

L’usage de ce domaine est réservé à des exemples de documentation, sans autorisation préalable. Il ne s’agit pas d’un service ; son utilisation à des fins de test ou de surveillance est à éviter.

Данный домен предназначен для использования в примерах документации без необходимости получения предварительного разрешения. Это не сервис; не рекомендуется его использование для тестирования и мониторинга.

Este dominio está destinado al uso en ejemplos de documentación sin necesidad de permiso. Esto no es un servicio; evitar utilizarlo para realizar pruebas o monitoreos.

 [Learn more](https://iana.org/help/example-domains)
```

**[tavily]** (0.84s, 958 chars; wr=0.5, wo=1.0; hdr 0, code 0, links 1, lists 0)
```
This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring purposes.

هذا النطاق مُخصص للاستخدام في أمثلة التوثيق دون الحاجة إلى إذن. هذه ليست خدمة، يُرجى تجنب الاعتماد عليها لأغراض الاختبار والمراقبة.

该域名仅用于文档示例，无需获得许可。这并非一项服务，请勿将其用于测试和监控目的。

L’usage de ce domaine est réservé à des exemples de documentation, sans autorisation préalable. Il ne s’agit pas d’un service ; son utilisation à des fins de test ou de surveillance est à éviter.

Данный домен предназначен для использования в примерах документации без необходимости получения предварительного разрешения. Это не сервис; не рекомендуется его использование для тестирования и мониторинга.

Este dominio está destinado al uso en ejemplos de documentación sin necesidad de permiso. Esto no es un servicio; evitar utilizarlo para realizar pruebas o monitoreos.

[Learn more](https://iana.org/help/example-domains)
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://example.com: jina: jina 451", "tried": [{"name": "jina", "error": "jin

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U2: https://docs.python.org/3/library/os.html
_(note: большие EN-доки, много код-блоков)_

**[local-auto]** (2.98s, 32000 chars, tier http; wr=1.0, wo=None; hdr 1, code 0, links 24, lists 10)
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

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.15/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/builtins/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a 

[…середина…]

e [path-like](https://docs.python.org/glossary.html#term-path-like-object)*filename* from the[filesystem encoding and error handler](https://docs.python.org/glossary.html#term-filesystem-encoding-and-error-handler) ; return[`str`](https://docs.python.org/builtins/stdtypes.html#str) unchanged.[`fsencode()`](https://docs.python.org#os.fsencode) is the reverse function.Added in version 3.2. Changed in version 3.6: Support added to accept objects implementing the [`os.PathLike`](https://docs.python.org#os.PathLike) interface.

- 
os.fspath(*path* )[¶](https://docs.python.org#os.fspath)
- Return the file system representation of the path. If [`str`](https://docs.python.org/builtins/stdtypes.html#str) or[`bytes`](https://docs.python.org/builtins/stdtypes.html#bytes) is passed in, it is returned unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/builtins/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.o
```

**[local-http]** (2.22s, 32000 chars, tier http; wr=1.0, wo=None; hdr 1, code 0, links 24, lists 10)
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

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.15/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/builtins/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a 

[…середина…]

e [path-like](https://docs.python.org/glossary.html#term-path-like-object)*filename* from the[filesystem encoding and error handler](https://docs.python.org/glossary.html#term-filesystem-encoding-and-error-handler) ; return[`str`](https://docs.python.org/builtins/stdtypes.html#str) unchanged.[`fsencode()`](https://docs.python.org#os.fsencode) is the reverse function.Added in version 3.2. Changed in version 3.6: Support added to accept objects implementing the [`os.PathLike`](https://docs.python.org#os.PathLike) interface.

- 
os.fspath(*path* )[¶](https://docs.python.org#os.fspath)
- Return the file system representation of the path. If [`str`](https://docs.python.org/builtins/stdtypes.html#str) or[`bytes`](https://docs.python.org/builtins/stdtypes.html#bytes) is passed in, it is returned unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/builtins/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.o
```

**[local-curl]** (2.37s, 32000 chars, tier curl; wr=1.0, wo=None; hdr 1, code 0, links 24, lists 10)
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

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.15/Lib/os.py)

This module provides a portable way of using operating system dependent
functionality.  If you just want to read or write a file see [`open()`](https://docs.python.org/builtins/functions.html#open), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/os.path.html#module-os.path) module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](https://docs.python.org/fileinput.html#module-fileinput)
module.  For creating temporary files and directories see the [`tempfile`](https://docs.python.org/tempfile.html#module-tempfile)
module, and for high-level file and directory handling see the [`shutil`](https://docs.python.org/shutil.html#module-shutil)
module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat
information about*path* in the same format (which happens to have originated
with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `os` module, but using them is of course a 

[…середина…]

e [path-like](https://docs.python.org/glossary.html#term-path-like-object)*filename* from the[filesystem encoding and error handler](https://docs.python.org/glossary.html#term-filesystem-encoding-and-error-handler) ; return[`str`](https://docs.python.org/builtins/stdtypes.html#str) unchanged.[`fsencode()`](https://docs.python.org#os.fsencode) is the reverse function.Added in version 3.2. Changed in version 3.6: Support added to accept objects implementing the [`os.PathLike`](https://docs.python.org#os.PathLike) interface.

- 
os.fspath(*path* )[¶](https://docs.python.org#os.fspath)
- Return the file system representation of the path. If [`str`](https://docs.python.org/builtins/stdtypes.html#str) or[`bytes`](https://docs.python.org/builtins/stdtypes.html#bytes) is passed in, it is returned unchanged.
Otherwise[`__fspath__()`](https://docs.python.org#os.PathLike.__fspath__) is called and its value is
returned as long as it is a`str` or`bytes` object.
In all other cases,[`TypeError`](https://docs.python.org/builtins/exceptions.html#TypeError) is raised.Added in version 3.6.

- 
*class* os.PathLike[¶](https://docs.python.org#os.PathLike)
- An [abstract base class](https://docs.python.o
```

**[local-browser]** ERROR: network/

**[firecrawl]** (2.77s, 32000 chars; wr=0.333, wo=None; hdr 2, code 0, links 28, lists 14)
```
### Navigation

- [index](https://docs.python.org/3/genindex.html "General Index")
- [modules](https://docs.python.org/3/py-modindex.html "Python Module Index") \|
- [next](https://docs.python.org/3/library/io.html "io — Core tools for working with streams") \|
- [previous](https://docs.python.org/3/library/allos.html "Generic Operating System Services") \|
- ![Python logo](https://docs.python.org/3/_static/py.svg)
- [Python](https://www.python.org/) »
- German \| DeutschGreek \| ΕλληνικάEnglishSpanish \| españolPersian \| فارسیFrench \| françaisItalian \| italianoJapanese \| 日本語Korean \| 한국어Polish \| polskiBrazilian Portuguese \| Português brasileiroRomanian \| RomâneșteRussian \| РусскийTurkish \| TürkçeSimplified Chinese \| 简体中文Traditional Chinese \| 繁體中文

dev (3.16)3.15.03.143.133.123.113.103.93.83.73.63.53.43.33.23.13.02.72.6

- [3.15.0 Documentation](https://docs.python.org/3/index.html) »

- [The Python standard library](https://docs.python.org/3/library/index.html) »
- [Generic Operating System Services](https://docs.python.org/3/library/allos.html) »
- [`os` — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html)
- \|

- Theme
AutoLightDark \|

# `os` — Miscellaneous operating system interfaces [¶](https://docs.python.org/3/library/os.html\#module-os "Link to this heading")

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.15/Lib/os.py)

* * *

This module provides a portable way of using operating system dependent
functionality. If you just want to read or write a file see [`open()`](https://docs.python.org/3/builtins/functions.html#open "open"), if
you want to manipulate paths, see the [`os.path`](https://docs.python.org/3/library/os.path.html#module-os.path "os.path: Operations on pathnames.") module, and 

[…середина…]

Changed in version 3.9: Updated to support [**PEP 584**](https://peps.python.org/pep-0584/)’s merge (`|`) and update (`|=`) operators.

Changed in version 3.15: The [`clear()`](https://docs.python.org/3/builtins/stdtypes.html#dict.clear "dict.clear") method can now emit an `os._clearenv` audit
event.

os.environb [¶](https://docs.python.org/3/library/os.html#os.environb "Link to this definition")

Bytes version of [`environ`](https://docs.python.org/3/library/os.html#os.environ "os.environ"): a [mapping](https://docs.python.org/3/glossary.html#term-mapping) object where both keys
and values are [`bytes`](https://docs.python.org/3/builtins/stdtypes.html#bytes "bytes") objects representing the process environment.
`environ` and `environb` are synchronized (modifying
`environb` updates `environ`, and vice versa).

`environb` is only available if [`supports_bytes_environ`](https://docs.python.org/3/library/os.html#os.supports_bytes_environ "os.supports_bytes_environ") is
`True`.

Added in version 3.2.

Changed in version 3.9: Updated to support [**PEP 584**](https://peps.python.org/pep-0584/)’s merge (`|`) and update (`|=`) operators.

os.reload\_environ() [¶](https://docs.python.org/3
```

**[tavily]** (1.64s, 32000 chars; wr=1.0, wo=None; hdr 2, code 0, links 32, lists 13)
```
### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](io.html "io — Core tools for working with streams") |
* [previous](allos.html "Generic Operating System Services") |
* [Python](https://www.python.org/) »
* [3.15.0 Documentation](../index.html) »
* [The Python standard library](index.html) »
* [Generic Operating System Services](allos.html) »
* `os` — Miscellaneous operating system interfaces
* |
* |

# `os` — Miscellaneous operating system interfaces[¶](#module-os "Link to this heading")

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.15/Lib/os.py)

---

This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see [`open()`](../builtins/functions.html#open "open"), if you want to manipulate paths, see the [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.") module, and if you want to read all the lines in all the files on the command line see the [`fileinput`](fileinput.html#module-fileinput "fileinput: Loop over standard input or a list of files.") module. For creating temporary files and directories see the [`tempfile`](tempfile.html#module-tempfile "tempfile: Generate temporary files and directories.") module, and for high-level file and directory handling see the [`shutil`](shutil.html#module-shutil "shutil: High-level file operations, including copying.") module.

Notes on the availability of these functions:

* The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat information about *path* in the same format (which

[…середина…]

 added to accept objects implementing the [`os.PathLike`](#os.PathLike "os.PathLike") interface.

os.fspath(*path*)[¶](#os.fspath "Link to this definition")
:   Return the file system representation of the path.

    If [`str`](../builtins/stdtypes.html#str "str") or [`bytes`](../builtins/stdtypes.html#bytes "bytes") is passed in, it is returned unchanged. Otherwise [`__fspath__()`](#os.PathLike.__fspath__ "os.PathLike.__fspath__") is called and its value is returned as long as it is a `str` or `bytes` object. In all other cases, [`TypeError`](../builtins/exceptions.html#TypeError "TypeError") is raised.

    Added in version 3.6.

*class* os.PathLike[¶](#os.PathLike "Link to this definition")
:   An [abstract base class](../glossary.html#term-abstract-base-class) for objects representing a file system path, e.g. [`pathlib.PurePath`](pathlib.html#pathlib.PurePath "pathlib.PurePath").

    Added in version 3.6.

    *abstractmethod* \_\_fspath\_\_()[¶](#os.PathLike.__fspath__ "Link to this definition")
    :   Return the file system path representation of the object.

        The method should only return a [`str`](../builtins/stdtypes.html#str "str") or [`bytes`](../builtins/stdtyp
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://docs.python.org/3/library/os.html: jina: jina 451", "tried": [{"name":

**[parallel]** ERROR: {"error": "all fetch providers failed for https://docs.python.org/3/library/os.html: parallel: parallel fetch: network e

## U3: https://www.rfc-editor.org/rfc/rfc9110.html
_(note: RFC, 1.2MB html, чистая статика)_

**[local-auto]** (2.24s, 9140 chars, tier http; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
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

**[local-http]** (1.87s, 9140 chars, tier http; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
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

**[local-curl]** (2.0s, 9140 chars, tier curl; wr=1.0, wo=0.0; hdr 3, code 0, links 25, lists 0)
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

**[local-browser]** ERROR: network/

**[firecrawl]** (3.78s, 32000 chars; wr=0.0, wo=0.0; hdr 4, code 0, links 41, lists 0)
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

**[tavily]** (7.87s, 0 chars; wr=0.0, wo=0.0; hdr 0, code 0, links 0, lists 0)
```
(пустой вывод, <200 симв.)
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://www.rfc-editor.org/rfc/rfc9110.html: jina: jina 451", "tried": [{"name

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U4: https://www.sqlite.org/changes.html
_(note: длинный changelog, плотный текст)_

**[local-auto]** (3.13s, 32000 chars, tier http; wr=0.333, wo=None; hdr 3, code 0, links 25, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-10-16"
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

### 2026-10-16 (3.54.1)

1.  Fix a possible heap-buffer overflow on 32-bit builds.
     (64-bit builds are not affected by this problem.)
2.  Fixes other problems in 3.54.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.54.0&to=version-3.54.1&y=ci) for details.**Hashes:**
3. SQLITE_SOURCE_ID: 2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76
4. SHA3-256 for sqlite3.c: e2b869d3003b33c942b7dd7063604fbc53553e1b66609570df39b9b7b558ee81

### 2026-10-09 (3.54.0)

1.  [CLI](https://www.sqlite.org/cli.html) enhancements:  1.  CLI prompt strings may contain [escape sequences](https://www.sqlite.org/cliprompt.html#esccd) that
          expand to show state information.  The initial CLI
          prompt is now be initialized the values of the
          SQLITE_PS1 and SQLITE_PS2 environment variables, if
          those variables exist.
  2.  The [default CLI prompt](https://www.sqlite.org/cliprompt.html#dfltprompt) has been enhanced to take
          advantage of the new escape sequences described in
          the previous.
  3.  For [columnar output modes](https://www.sqlite.org/climode.html#clmnr) , the

[…середина…]

et of a query does not exactly match the ORDER BY clause.
     
8.  Add new interfaces to the [session extension](https://www.sqlite.org/sessionintro.html) that enable an application to add changes one at
     a time to the sqlite3_changegroup object:  1.  [sqlite3changegroup_change_begin()](https://www.sqlite.org/session/sqlite3changegroup_change_begin.html)
  2.  [sqlite3changegroup_change_blob()](https://www.sqlite.org/session/sqlite3changegroup_change_blob.html)
  3.  [sqlite3changegroup_change_double()](https://www.sqlite.org/session/sqlite3changegroup_change_double.html)
  4.  [sqlite3changegroup_change_int64()](https://www.sqlite.org/session/sqlite3changegroup_change_int64.html)
  5.  [sqlite3changegroup_change_null()](https://www.sqlite.org/session/sqlite3changegroup_change_null.html)
  6.  [sqlite3changegroup_change_text()](https://www.sqlite.org/session/sqlite3changegroup_change_text.html)
  7.  [sqlite3changegroup_change_finish()](https://www.sqlite.org/session/sqlite3changegroup_change_finish.html)
  8.  [sqlite3changegroup_config()](https://www.sqlite.org/session/sqlite3changegroup_config.html)
9.  Improvements to floating-point ↔ text conversions.
       1.  Reimpleme
```

**[local-http]** (2.6s, 32000 chars, tier http; wr=0.333, wo=None; hdr 3, code 0, links 25, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-10-16"
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

### 2026-10-16 (3.54.1)

1.  Fix a possible heap-buffer overflow on 32-bit builds.
     (64-bit builds are not affected by this problem.)
2.  Fixes other problems in 3.54.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.54.0&to=version-3.54.1&y=ci) for details.**Hashes:**
3. SQLITE_SOURCE_ID: 2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76
4. SHA3-256 for sqlite3.c: e2b869d3003b33c942b7dd7063604fbc53553e1b66609570df39b9b7b558ee81

### 2026-10-09 (3.54.0)

1.  [CLI](https://www.sqlite.org/cli.html) enhancements:  1.  CLI prompt strings may contain [escape sequences](https://www.sqlite.org/cliprompt.html#esccd) that
          expand to show state information.  The initial CLI
          prompt is now be initialized the values of the
          SQLITE_PS1 and SQLITE_PS2 environment variables, if
          those variables exist.
  2.  The [default CLI prompt](https://www.sqlite.org/cliprompt.html#dfltprompt) has been enhanced to take
          advantage of the new escape sequences described in
          the previous.
  3.  For [columnar output modes](https://www.sqlite.org/climode.html#clmnr) , the

[…середина…]

et of a query does not exactly match the ORDER BY clause.
     
8.  Add new interfaces to the [session extension](https://www.sqlite.org/sessionintro.html) that enable an application to add changes one at
     a time to the sqlite3_changegroup object:  1.  [sqlite3changegroup_change_begin()](https://www.sqlite.org/session/sqlite3changegroup_change_begin.html)
  2.  [sqlite3changegroup_change_blob()](https://www.sqlite.org/session/sqlite3changegroup_change_blob.html)
  3.  [sqlite3changegroup_change_double()](https://www.sqlite.org/session/sqlite3changegroup_change_double.html)
  4.  [sqlite3changegroup_change_int64()](https://www.sqlite.org/session/sqlite3changegroup_change_int64.html)
  5.  [sqlite3changegroup_change_null()](https://www.sqlite.org/session/sqlite3changegroup_change_null.html)
  6.  [sqlite3changegroup_change_text()](https://www.sqlite.org/session/sqlite3changegroup_change_text.html)
  7.  [sqlite3changegroup_change_finish()](https://www.sqlite.org/session/sqlite3changegroup_change_finish.html)
  8.  [sqlite3changegroup_config()](https://www.sqlite.org/session/sqlite3changegroup_config.html)
9.  Improvements to floating-point ↔ text conversions.
       1.  Reimpleme
```

**[local-curl]** (2.64s, 32000 chars, tier curl; wr=0.333, wo=None; hdr 3, code 0, links 25, lists 0)
```
---
title: Release History
url: https://www.sqlite.org/changes.html
hostname: sqlite.org
sitename: sqlite.org
date: "2026-10-16"
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

### 2026-10-16 (3.54.1)

1.  Fix a possible heap-buffer overflow on 32-bit builds.
     (64-bit builds are not affected by this problem.)
2.  Fixes other problems in 3.54.0 reported by users.  See the
     [check-in timeline](https://sqlite.org/src/timeline?from=version-3.54.0&to=version-3.54.1&y=ci) for details.**Hashes:**
3. SQLITE_SOURCE_ID: 2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76
4. SHA3-256 for sqlite3.c: e2b869d3003b33c942b7dd7063604fbc53553e1b66609570df39b9b7b558ee81

### 2026-10-09 (3.54.0)

1.  [CLI](https://www.sqlite.org/cli.html) enhancements:  1.  CLI prompt strings may contain [escape sequences](https://www.sqlite.org/cliprompt.html#esccd) that
          expand to show state information.  The initial CLI
          prompt is now be initialized the values of the
          SQLITE_PS1 and SQLITE_PS2 environment variables, if
          those variables exist.
  2.  The [default CLI prompt](https://www.sqlite.org/cliprompt.html#dfltprompt) has been enhanced to take
          advantage of the new escape sequences described in
          the previous.
  3.  For [columnar output modes](https://www.sqlite.org/climode.html#clmnr) , the

[…середина…]

et of a query does not exactly match the ORDER BY clause.
     
8.  Add new interfaces to the [session extension](https://www.sqlite.org/sessionintro.html) that enable an application to add changes one at
     a time to the sqlite3_changegroup object:  1.  [sqlite3changegroup_change_begin()](https://www.sqlite.org/session/sqlite3changegroup_change_begin.html)
  2.  [sqlite3changegroup_change_blob()](https://www.sqlite.org/session/sqlite3changegroup_change_blob.html)
  3.  [sqlite3changegroup_change_double()](https://www.sqlite.org/session/sqlite3changegroup_change_double.html)
  4.  [sqlite3changegroup_change_int64()](https://www.sqlite.org/session/sqlite3changegroup_change_int64.html)
  5.  [sqlite3changegroup_change_null()](https://www.sqlite.org/session/sqlite3changegroup_change_null.html)
  6.  [sqlite3changegroup_change_text()](https://www.sqlite.org/session/sqlite3changegroup_change_text.html)
  7.  [sqlite3changegroup_change_finish()](https://www.sqlite.org/session/sqlite3changegroup_change_finish.html)
  8.  [sqlite3changegroup_config()](https://www.sqlite.org/session/sqlite3changegroup_config.html)
9.  Improvements to floating-point ↔ text conversions.
       1.  Reimpleme
```

**[local-browser]** ERROR: network/

**[firecrawl]** (2.77s, 32000 chars; wr=0.333, wo=None; hdr 3, code 0, links 26, lists 0)
```
[![SQLite](https://sqlite.org/images/sqlite370_banner.svg)](https://sqlite.org/index.html)

Small. Fast. Reliable.

Choose any three.

Search DocumentationSearch Changelog

# Release History

This page provides a high-level summary of changes to SQLite.
For more detail, see the Fossil checkin logs at
[https://sqlite.org/src/timeline](https://sqlite.org/src/timeline) and
[https://sqlite.org/src/timeline?t=release](https://sqlite.org/src/timeline?t=release).
See the [chronology](https://sqlite.org/chronology.html) a succinct listing of releases.

### 2026-10-16 (3.54.1)

1. Fix a possible heap-buffer overflow on 32-bit builds.
    (64-bit builds are not affected by this problem.)

2. Fixes other problems in 3.54.0 reported by users. See the
    [check-in timeline](https://sqlite.org/src/timeline?from=version-3.54.0&to=version-3.54.1&y=ci)
    for details.

   **Hashes:**

3. SQLITE\_SOURCE\_ID: 2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76

4. SHA3-256 for sqlite3.c: e2b869d3003b33c942b7dd7063604fbc53553e1b66609570df39b9b7b558ee81


### 2026-10-09 (3.54.0)

01. [CLI](https://sqlite.org/cli.html)enhancements:

    01. CLI prompt strings may contain [escape sequences](https://sqlite.org/cliprompt.html#esccd) that
         expand to show state information. The initial CLI
         prompt is now be initialized the values of the
         SQLITE\_PS1 and SQLITE\_PS2 environment variables, if
         those variables exist.

    02. The [default CLI prompt](https://sqlite.org/cliprompt.html#dfltprompt) has been enhanced to take
         advantage of the new escape sequences described in
         the previous.

    03. For [columnar output modes](https://sqlite.org/climode.html#clmnr), the CLI now shows the column name header
         by def

[…середина…]

   1. [sqlite3changegroup\_change\_begin()](https://sqlite.org/session/sqlite3changegroup_change_begin.html)
    2. [sqlite3changegroup\_change\_blob()](https://sqlite.org/session/sqlite3changegroup_change_blob.html)
    3. [sqlite3changegroup\_change\_double()](https://sqlite.org/session/sqlite3changegroup_change_double.html)
    4. [sqlite3changegroup\_change\_int64()](https://sqlite.org/session/sqlite3changegroup_change_int64.html)
    5. [sqlite3changegroup\_change\_null()](https://sqlite.org/session/sqlite3changegroup_change_null.html)
    6. [sqlite3changegroup\_change\_text()](https://sqlite.org/session/sqlite3changegroup_change_text.html)
    7. [sqlite3changegroup\_change\_finish()](https://sqlite.org/session/sqlite3changegroup_change_finish.html)
    8. [sqlite3changegroup\_config()](https://sqlite.org/session/sqlite3changegroup_config.html)
09. Improvements to floating-point ↔ text conversions.
    1. Reimplemented to improve performance.

    2. Rounding is now done by [default to 17 significant digits](https://sqlite.org/floatingpoint.html#*fpdigits),
        instead of 15, as was the case for all prior versions.
        The [sqlite3\_db\_config](https://sqlite.org/c3r
```

**[tavily]** (1.99s, 32000 chars; wr=0.333, wo=None; hdr 7, code 0, links 24, lists 14)
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

**[jina]** ERROR: {"error": "all fetch providers failed for https://www.sqlite.org/changes.html: jina: jina 451", "tried": [{"name": "jina

**[parallel]** ERROR: {"error": "all fetch providers failed for https://www.sqlite.org/changes.html: parallel: parallel fetch: HTTP 403 from M
