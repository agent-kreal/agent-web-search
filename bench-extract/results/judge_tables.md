# scenario: tables

## U1: https://pandas.pydata.org/docs/user_guide/10min.html
_(note: таблицы в доках)_

**[local-auto]** (1.75s, 32000 chars, tier http; wr=1.0, wo=0.0; hdr 4, code 15, links 12, lists 0)
```
---
title: "10 minutes to pandas#"
url: https://pandas.pydata.org/docs/user_guide/10min.html
hostname: pydata.org
sitename: pandas 3.0.6 documentation
date: "2013-01-02"
---
# 10 minutes to pandas[#](https://pandas.pydata.org#minutes-to-pandas)

This is a short introduction to pandas, geared mainly for new users.
You can see more complex recipes in the [Cookbook](https://pandas.pydata.org/cookbook.html#cookbook).

Customarily, we import as follows:

```
In [1]: import numpy as np
In [2]: import pandas as pd
```
## Basic data structures in pandas[#](https://pandas.pydata.org#basic-data-structures-in-pandas)

pandas provides two types of classes for handling data:

## Object creation[#](https://pandas.pydata.org#object-creation)

See the [Intro to data structures section](https://pandas.pydata.org/dsintro.html#dsintro).

Creating a [`Series`](https://pandas.pydata.org/reference/api/pandas.Series.html#pandas.Series) by passing a list of values, letting pandas create
a default [`RangeIndex`](https://pandas.pydata.org/reference/api/pandas.RangeIndex.html#pandas.RangeIndex).

```
In [3]: s = pd.Series([1, 3, 5, np.nan, 6, 8])
In [4]: s
Out[4]: 
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64
```
Creating a [`DataFrame`](https://pandas.pydata.org/reference/api/pandas.DataFrame.html#pandas.DataFrame) by passing a NumPy array with a datetime index using [`date_range()`](https://pandas.pydata.org/reference/api/pandas.date_range.html#pandas.date_range)
and labeled columns:

```
In [5]: dates = pd.date_range("20130101", periods=6)
In [6]: dates
Out[6]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
               '2013-01-05', '2013-01-06'],
              dtype='datetime64[us]', freq='D')
In [7]: df = pd.DataFrame(np.random.randn(6, 4),

[…середина…]


2013-01-04 -0.706771 -1.039575
2013-01-05  0.567020  0.276232
2013-01-06  0.113648 -1.478427
```
For getting a value explicitly:

```
In [39]: df.iloc[1, 1]
Out[39]: np.float64(-0.17321464905330858)
```
For getting fast access to a scalar (equivalent to the prior method):

```
In [40]: df.iat[1, 1]
Out[40]: np.float64(-0.17321464905330858)
```
### Boolean indexing[#](https://pandas.pydata.org#boolean-indexing)

Select rows where `df.A` is greater than `0`.

```
In [41]: df[df["A"] > 0]
Out[41]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```
Selecting values from a [`DataFrame`](https://pandas.pydata.org/reference/api/pandas.DataFrame.html#pandas.DataFrame) where a boolean condition is met:

```
In [42]: df[df > 0]
Out[42]: 
                   A         B         C         D
2013-01-01  0.469112       NaN       NaN       NaN
2013-01-02  1.212112       NaN  0.119209       NaN
2013-01-03       NaN       NaN       NaN  1.071804
2013-01-04  0.721555       NaN       NaN  0.271860
2013-01-05       NaN  0.567020  0.276232       N
```

**[local-http]** (1.19s, 32000 chars, tier http; wr=1.0, wo=0.0; hdr 4, code 15, links 12, lists 0)
```
---
title: "10 minutes to pandas#"
url: https://pandas.pydata.org/docs/user_guide/10min.html
hostname: pydata.org
sitename: pandas 3.0.6 documentation
date: "2013-01-02"
---
# 10 minutes to pandas[#](https://pandas.pydata.org#minutes-to-pandas)

This is a short introduction to pandas, geared mainly for new users.
You can see more complex recipes in the [Cookbook](https://pandas.pydata.org/cookbook.html#cookbook).

Customarily, we import as follows:

```
In [1]: import numpy as np
In [2]: import pandas as pd
```
## Basic data structures in pandas[#](https://pandas.pydata.org#basic-data-structures-in-pandas)

pandas provides two types of classes for handling data:

## Object creation[#](https://pandas.pydata.org#object-creation)

See the [Intro to data structures section](https://pandas.pydata.org/dsintro.html#dsintro).

Creating a [`Series`](https://pandas.pydata.org/reference/api/pandas.Series.html#pandas.Series) by passing a list of values, letting pandas create
a default [`RangeIndex`](https://pandas.pydata.org/reference/api/pandas.RangeIndex.html#pandas.RangeIndex).

```
In [3]: s = pd.Series([1, 3, 5, np.nan, 6, 8])
In [4]: s
Out[4]: 
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64
```
Creating a [`DataFrame`](https://pandas.pydata.org/reference/api/pandas.DataFrame.html#pandas.DataFrame) by passing a NumPy array with a datetime index using [`date_range()`](https://pandas.pydata.org/reference/api/pandas.date_range.html#pandas.date_range)
and labeled columns:

```
In [5]: dates = pd.date_range("20130101", periods=6)
In [6]: dates
Out[6]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
               '2013-01-05', '2013-01-06'],
              dtype='datetime64[us]', freq='D')
In [7]: df = pd.DataFrame(np.random.randn(6, 4),

[…середина…]


2013-01-04 -0.706771 -1.039575
2013-01-05  0.567020  0.276232
2013-01-06  0.113648 -1.478427
```
For getting a value explicitly:

```
In [39]: df.iloc[1, 1]
Out[39]: np.float64(-0.17321464905330858)
```
For getting fast access to a scalar (equivalent to the prior method):

```
In [40]: df.iat[1, 1]
Out[40]: np.float64(-0.17321464905330858)
```
### Boolean indexing[#](https://pandas.pydata.org#boolean-indexing)

Select rows where `df.A` is greater than `0`.

```
In [41]: df[df["A"] > 0]
Out[41]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```
Selecting values from a [`DataFrame`](https://pandas.pydata.org/reference/api/pandas.DataFrame.html#pandas.DataFrame) where a boolean condition is met:

```
In [42]: df[df > 0]
Out[42]: 
                   A         B         C         D
2013-01-01  0.469112       NaN       NaN       NaN
2013-01-02  1.212112       NaN  0.119209       NaN
2013-01-03       NaN       NaN       NaN  1.071804
2013-01-04  0.721555       NaN       NaN  0.271860
2013-01-05       NaN  0.567020  0.276232       N
```

**[local-curl]** (1.19s, 32000 chars, tier curl; wr=1.0, wo=0.0; hdr 4, code 15, links 12, lists 0)
```
---
title: "10 minutes to pandas#"
url: https://pandas.pydata.org/docs/user_guide/10min.html
hostname: pydata.org
sitename: pandas 3.0.6 documentation
date: "2013-01-02"
---
# 10 minutes to pandas[#](https://pandas.pydata.org#minutes-to-pandas)

This is a short introduction to pandas, geared mainly for new users.
You can see more complex recipes in the [Cookbook](https://pandas.pydata.org/cookbook.html#cookbook).

Customarily, we import as follows:

```
In [1]: import numpy as np
In [2]: import pandas as pd
```
## Basic data structures in pandas[#](https://pandas.pydata.org#basic-data-structures-in-pandas)

pandas provides two types of classes for handling data:

## Object creation[#](https://pandas.pydata.org#object-creation)

See the [Intro to data structures section](https://pandas.pydata.org/dsintro.html#dsintro).

Creating a [`Series`](https://pandas.pydata.org/reference/api/pandas.Series.html#pandas.Series) by passing a list of values, letting pandas create
a default [`RangeIndex`](https://pandas.pydata.org/reference/api/pandas.RangeIndex.html#pandas.RangeIndex).

```
In [3]: s = pd.Series([1, 3, 5, np.nan, 6, 8])
In [4]: s
Out[4]: 
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64
```
Creating a [`DataFrame`](https://pandas.pydata.org/reference/api/pandas.DataFrame.html#pandas.DataFrame) by passing a NumPy array with a datetime index using [`date_range()`](https://pandas.pydata.org/reference/api/pandas.date_range.html#pandas.date_range)
and labeled columns:

```
In [5]: dates = pd.date_range("20130101", periods=6)
In [6]: dates
Out[6]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
               '2013-01-05', '2013-01-06'],
              dtype='datetime64[us]', freq='D')
In [7]: df = pd.DataFrame(np.random.randn(6, 4),

[…середина…]


2013-01-04 -0.706771 -1.039575
2013-01-05  0.567020  0.276232
2013-01-06  0.113648 -1.478427
```
For getting a value explicitly:

```
In [39]: df.iloc[1, 1]
Out[39]: np.float64(-0.17321464905330858)
```
For getting fast access to a scalar (equivalent to the prior method):

```
In [40]: df.iat[1, 1]
Out[40]: np.float64(-0.17321464905330858)
```
### Boolean indexing[#](https://pandas.pydata.org#boolean-indexing)

Select rows where `df.A` is greater than `0`.

```
In [41]: df[df["A"] > 0]
Out[41]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```
Selecting values from a [`DataFrame`](https://pandas.pydata.org/reference/api/pandas.DataFrame.html#pandas.DataFrame) where a boolean condition is met:

```
In [42]: df[df > 0]
Out[42]: 
                   A         B         C         D
2013-01-01  0.469112       NaN       NaN       NaN
2013-01-02  1.212112       NaN  0.119209       NaN
2013-01-03       NaN       NaN       NaN  1.071804
2013-01-04  0.721555       NaN       NaN  0.271860
2013-01-05       NaN  0.567020  0.276232       N
```

**[local-browser]** ERROR: network/

**[firecrawl]** (4.35s, 32000 chars; wr=0.667, wo=1.0; hdr 4, code 13, links 27, lists 3)
```
[Skip to main content](https://pandas.pydata.org/docs/user_guide/10min.html#main-content)

Back to top`Ctrl` + `K`

3.0 (stable)

[dev](https://pandas.pydata.org/docs/dev/user_guide/10min.html) [3.1 (rc)](https://pandas.pydata.org/pandas-docs/version/3.1/user_guide/10min.html) [3.0 (stable)](https://pandas.pydata.org/docs/user_guide/10min.html) [2.3](https://pandas.pydata.org/pandas-docs/version/2.3/user_guide/10min.html) [2.2](https://pandas.pydata.org/pandas-docs/version/2.2/user_guide/10min.html) [2.1](https://pandas.pydata.org/pandas-docs/version/2.1/user_guide/10min.html) [2.0](https://pandas.pydata.org/pandas-docs/version/2.0/user_guide/10min.html) [1.5](https://pandas.pydata.org/pandas-docs/version/1.5/user_guide/10min.html) [1.4](https://pandas.pydata.org/pandas-docs/version/1.4/user_guide/10min.html) [1.3](https://pandas.pydata.org/pandas-docs/version/1.3/user_guide/10min.html) [1.2](https://pandas.pydata.org/pandas-docs/version/1.2/user_guide/10min.html) [1.1](https://pandas.pydata.org/pandas-docs/version/1.1/user_guide/10min.html) [1.0](https://pandas.pydata.org/pandas-docs/version/1.0/user_guide/10min.html)

LightDarkSystem Settings

- [GitHub](https://github.com/pandas-dev/pandas)
- [X](https://x.com/pandas_dev)
- [Mastodon](https://fosstodon.org/@pandas_dev)

# 10 minutes to pandas [\#](https://pandas.pydata.org/docs/user_guide/10min.html\#minutes-to-pandas "Link to this heading")

This is a short introduction to pandas, geared mainly for new users.
You can see more complex recipes in the [Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html#cookbook).

Customarily, we import as follows:

```
In [1]: import numpy as np

In [2]: import pandas as pd
```

Copy to clipboard

## Basic data structures in pandas [\#](https://pandas.pydata.org/docs/us

[…середина…]

-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```

Copy to clipboard

### Selection by label [\#](https://pandas.pydata.org/docs/user_guide/10min.html\#selection-by-label "Link to this heading")

See more in [Selection by Label](https://pandas.pydata.org/docs/user_guide/indexing.html#indexing-label) using [`DataFrame.loc()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html#pandas.DataFrame.loc "pandas.DataFrame.loc") or [`DataFrame.at()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html#pandas.DataFrame.at "pandas.DataFrame.at").

Selecting a row matching a label:

```
In [29]: df.loc[dates[0]]
Out[29]:
A    0.469112
B   -0.282863
C   -1.509059
D   -1.135632
Name: 2013-01-01 00:00:00, dtype: float64
```

Copy to clipboard

Selecting all rows (`:`) with a select column labels:

```
In [30]: df.loc[:, ["A", "B"]]
Out[30]:
                   A         B
2013-01-01  0.469112 -0.282863
2013-01-02  1.212112 -0.173215
2013-01-03 -0.861849 -2.104569
2013-01-04  0.721555 -0.706771
2013-01-05 -0.424972  0.567020
2013-01-06 -0.673690  0.113648
```

Cop
```

**[tavily]** (1.34s, 32000 chars; wr=0.333, wo=0.0; hdr 4, code 18, links 18, lists 6)
```
* [GitHub](https://github.com/pandas-dev/pandas "GitHub")
* [X](https://x.com/pandas_dev "X")
* [Mastodon](https://fosstodon.org/@pandas_dev "Mastodon")

* [GitHub](https://github.com/pandas-dev/pandas "GitHub")
* [X](https://x.com/pandas_dev "X")
* [Mastodon](https://fosstodon.org/@pandas_dev "Mastodon")

# 10 minutes to pandas[#](#minutes-to-pandas "Link to this heading")

This is a short introduction to pandas, geared mainly for new users. You can see more complex recipes in the [Cookbook](cookbook.html#cookbook).

Customarily, we import as follows:

```
In [1]: import  numpy  as  npIn [2]: import  pandas  as  pd
```

## Basic data structures in pandas[#](#basic-data-structures-in-pandas "Link to this heading")

pandas provides two types of classes for handling data:

1. [`Series`](../reference/api/pandas.Series.html#pandas.Series "pandas.Series"): a one-dimensional labeled array holding data of any type
   :   such as integers, strings, Python objects etc.
2. [`DataFrame`](../reference/api/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame"): a two-dimensional data structure that holds data like a two-dimension array or a table with rows and columns.

## Object creation[#](#object-creation "Link to this heading")

See the [Intro to data structures section](dsintro.html#dsintro).

Creating a [`Series`](../reference/api/pandas.Series.html#pandas.Series "pandas.Series") by passing a list of values, letting pandas create a default [`RangeIndex`](../reference/api/pandas.RangeIndex.html#pandas.RangeIndex "pandas.RangeIndex").

```
In [3]: s = pd. Series([1, 3, 5, np. nan, 6, 8])In [4]: sOut[4]: 0 1.01 3.02 5.0 3 NaN4 6.05 8.0dtype: float64
```

Creating a [`DataFrame`](../reference/api/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame") by passing a NumPy arr

[…середина…]

erence/api/pandas.Series.isin.html#pandas.Series.isin "pandas.Series.isin") method for filtering:

```
In [43]: df2 = df. copy()In [44]: df2["E"] =["one", "one", "two", "three", "four", "three"]In [45]: df2Out[45]:  A B C D E2013-01-01 0.469112 -0.282863 -1.509059 -1.135632 one2013-01-02 1.212112 -0.173215 0.119209 -1.044236 one2013-01-03 -0.861849 -2.104569 -0.494929 1.071804 two2013-01-04 0.721555 -0.706771 -1.039575 0.271860 three2013-01-05 -0.424972 0.567020 0.276232 -1.087401 four2013-01-06 -0.673690 0.113648 -1.478427 0.524988 threeIn [46]: df2[df2["E"]. isin(["two", "four"])]Out[46]:  A B C D E2013-01-03 -0.861849 -2.104569 -0.494929 1.071804 two2013-01-05 -0.424972 0.567020 0.276232 -1.087401 four
```

### Setting[#](#setting "Link to this heading")

Setting a new column automatically aligns the data by the indexes:

```
In [47]: s1 = pd. Series( ....: [1, 2, 3, 4, 5, 6], ....: index = pd. date_range("20130102", periods = 6)) ....: In [48]: s1Out[48]: 2013-01-02 12013-01-03 22013-01-04 32013-01-05 42013-01-06 52013-01-07 6Freq: D, dtype: int64In [49]: df["F"] = s1
```

Setting values by label:

```
In [50]: df. at[dates[0], "A"] = 0
```

Setting values by position:

```
In 
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://pandas.pydata.org/docs/user_guide/10min.html: jina: jina network: [SSL

**[parallel]** ERROR: {"error": "all fetch providers failed for https://pandas.pydata.org/docs/user_guide/10min.html: parallel: parallel fetch

## U2: https://www.postgresql.org/docs/current/sql-select.html
_(note: таблицы параметров)_

**[local-auto]** (1.2s, 32000 chars, tier http; wr=1.0, wo=None; hdr 0, code 0, links 1, lists 0)
```
---
title: SELECT
url: https://www.postgresql.org/docs/18/sql-select.html
hostname: postgresql.org
description: SELECT SELECT, TABLE, WITH — retrieve rows from a table or view Synopsis [ WITH [ RECURSIVE ] with_query [, …
sitename: PostgreSQL Documentation
date: "2026-08-13"
---
SELECT, TABLE, WITH — retrieve rows from a table or view

[ WITH [ RECURSIVE ] *`with_query`* [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( *`expression`* [, ...] ) ] ]
    [ { * | *`expression`* [ [ AS ] *`output_name`* ] } [, ...] ]
    [ FROM *`from_item`* [, ...] ]
    [ WHERE *`condition`* ]
    [ GROUP BY [ ALL | DISTINCT ] *`grouping_element`* [, ...] ]
    [ HAVING *`condition`* ]
    [ WINDOW *`window_name`* AS ( *`window_definition`* ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] *`select`* ]
    [ ORDER BY *`expression`* [ ASC | DESC | USING *`operator`* ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { *`count`* | ALL } ]
    [ OFFSET *`start`* [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ *`count`* ] { ROW | ROWS } { ONLY | WITH TIES } ]
    [ FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF *`from_reference`* [, ...] ] [ NOWAIT | SKIP LOCKED ] [...] ]
where *`from_item`* can be one of:
    [ ONLY ] *`table_name`* [ * ] [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
                [ TABLESAMPLE *`sampling_method`* ( *`argument`* [, ...] ) [ REPEATABLE ( *`seed`* ) ] ]
    [ LATERAL ] ( *`select`* ) [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    *`with_query_name`* [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    [ LATERAL ] *`function_name`* ( [ *`argument`* [, ...] ] )
                [ WITH ORDINALITY ] [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    [ LATERAL ] *`function_name`* ( [ *`argument`* [, ...] ] ) [ AS ] 

[…середина…]

 in the database via extensions.

The `BERNOULLI` and `SYSTEM` sampling methods each accept a single *`argument`* which is the fraction of the table to sample, expressed as a percentage between 0 and 100. This argument can be any `real`-valued expression. (Other sampling methods might accept more or different arguments.) These two methods each return a randomly-chosen sample of the table that will contain approximately the specified percentage of the table's rows. The `BERNOULLI` method scans the whole table and selects or ignores individual rows independently with the specified probability. The `SYSTEM` method does block-level sampling with each block having the specified chance of being selected; all rows in each selected block are returned. The `SYSTEM` method is significantly faster than the `BERNOULLI` method when small sampling percentages are specified, but it may return a less-random sample of the table as a result of clustering effects.

The optional `REPEATABLE` clause specifies a *`seed`* number or expression to use for generating random numbers within the sampling method. The seed value can be any non-null floating-point value. Two queries that specify the same seed and
```

**[local-http]** (0.93s, 32000 chars, tier http; wr=1.0, wo=None; hdr 0, code 0, links 1, lists 0)
```
---
title: SELECT
url: https://www.postgresql.org/docs/18/sql-select.html
hostname: postgresql.org
description: SELECT SELECT, TABLE, WITH — retrieve rows from a table or view Synopsis [ WITH [ RECURSIVE ] with_query [, …
sitename: PostgreSQL Documentation
date: "2026-08-13"
---
SELECT, TABLE, WITH — retrieve rows from a table or view

[ WITH [ RECURSIVE ] *`with_query`* [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( *`expression`* [, ...] ) ] ]
    [ { * | *`expression`* [ [ AS ] *`output_name`* ] } [, ...] ]
    [ FROM *`from_item`* [, ...] ]
    [ WHERE *`condition`* ]
    [ GROUP BY [ ALL | DISTINCT ] *`grouping_element`* [, ...] ]
    [ HAVING *`condition`* ]
    [ WINDOW *`window_name`* AS ( *`window_definition`* ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] *`select`* ]
    [ ORDER BY *`expression`* [ ASC | DESC | USING *`operator`* ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { *`count`* | ALL } ]
    [ OFFSET *`start`* [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ *`count`* ] { ROW | ROWS } { ONLY | WITH TIES } ]
    [ FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF *`from_reference`* [, ...] ] [ NOWAIT | SKIP LOCKED ] [...] ]
where *`from_item`* can be one of:
    [ ONLY ] *`table_name`* [ * ] [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
                [ TABLESAMPLE *`sampling_method`* ( *`argument`* [, ...] ) [ REPEATABLE ( *`seed`* ) ] ]
    [ LATERAL ] ( *`select`* ) [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    *`with_query_name`* [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    [ LATERAL ] *`function_name`* ( [ *`argument`* [, ...] ] )
                [ WITH ORDINALITY ] [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    [ LATERAL ] *`function_name`* ( [ *`argument`* [, ...] ] ) [ AS ] 

[…середина…]

 in the database via extensions.

The `BERNOULLI` and `SYSTEM` sampling methods each accept a single *`argument`* which is the fraction of the table to sample, expressed as a percentage between 0 and 100. This argument can be any `real`-valued expression. (Other sampling methods might accept more or different arguments.) These two methods each return a randomly-chosen sample of the table that will contain approximately the specified percentage of the table's rows. The `BERNOULLI` method scans the whole table and selects or ignores individual rows independently with the specified probability. The `SYSTEM` method does block-level sampling with each block having the specified chance of being selected; all rows in each selected block are returned. The `SYSTEM` method is significantly faster than the `BERNOULLI` method when small sampling percentages are specified, but it may return a less-random sample of the table as a result of clustering effects.

The optional `REPEATABLE` clause specifies a *`seed`* number or expression to use for generating random numbers within the sampling method. The seed value can be any non-null floating-point value. Two queries that specify the same seed and
```

**[local-curl]** (1.09s, 32000 chars, tier curl; wr=1.0, wo=None; hdr 0, code 0, links 1, lists 0)
```
---
title: SELECT
url: https://www.postgresql.org/docs/18/sql-select.html
hostname: postgresql.org
description: SELECT SELECT, TABLE, WITH — retrieve rows from a table or view Synopsis [ WITH [ RECURSIVE ] with_query [, …
sitename: PostgreSQL Documentation
date: "2026-08-13"
---
SELECT, TABLE, WITH — retrieve rows from a table or view

[ WITH [ RECURSIVE ] *`with_query`* [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( *`expression`* [, ...] ) ] ]
    [ { * | *`expression`* [ [ AS ] *`output_name`* ] } [, ...] ]
    [ FROM *`from_item`* [, ...] ]
    [ WHERE *`condition`* ]
    [ GROUP BY [ ALL | DISTINCT ] *`grouping_element`* [, ...] ]
    [ HAVING *`condition`* ]
    [ WINDOW *`window_name`* AS ( *`window_definition`* ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] *`select`* ]
    [ ORDER BY *`expression`* [ ASC | DESC | USING *`operator`* ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { *`count`* | ALL } ]
    [ OFFSET *`start`* [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ *`count`* ] { ROW | ROWS } { ONLY | WITH TIES } ]
    [ FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF *`from_reference`* [, ...] ] [ NOWAIT | SKIP LOCKED ] [...] ]
where *`from_item`* can be one of:
    [ ONLY ] *`table_name`* [ * ] [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
                [ TABLESAMPLE *`sampling_method`* ( *`argument`* [, ...] ) [ REPEATABLE ( *`seed`* ) ] ]
    [ LATERAL ] ( *`select`* ) [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    *`with_query_name`* [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    [ LATERAL ] *`function_name`* ( [ *`argument`* [, ...] ] )
                [ WITH ORDINALITY ] [ [ AS ] *`alias`* [ ( *`column_alias`* [, ...] ) ] ]
    [ LATERAL ] *`function_name`* ( [ *`argument`* [, ...] ] ) [ AS ] 

[…середина…]

 in the database via extensions.

The `BERNOULLI` and `SYSTEM` sampling methods each accept a single *`argument`* which is the fraction of the table to sample, expressed as a percentage between 0 and 100. This argument can be any `real`-valued expression. (Other sampling methods might accept more or different arguments.) These two methods each return a randomly-chosen sample of the table that will contain approximately the specified percentage of the table's rows. The `BERNOULLI` method scans the whole table and selects or ignores individual rows independently with the specified probability. The `SYSTEM` method does block-level sampling with each block having the specified chance of being selected; all rows in each selected block are returned. The `SYSTEM` method is significantly faster than the `BERNOULLI` method when small sampling percentages are specified, but it may return a less-random sample of the table as a result of clustering effects.

The optional `REPEATABLE` clause specifies a *`seed`* number or expression to use for generating random numbers within the sampling method. The seed value can be any non-null floating-point value. Two queries that specify the same seed and
```

**[local-browser]** ERROR: network/

**[firecrawl]** (1.86s, 32000 chars; wr=0.0, wo=None; hdr 1, code 0, links 24, lists 0)
```
October 15, 2026: [PostgreSQL 19 RC 1 Released!](https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/)

[Documentation](https://www.postgresql.org/docs/ "Documentation") → [PostgreSQL 18](https://www.postgresql.org/docs/18/index.html)

Supported Versions:



[Current](https://www.postgresql.org/docs/current/sql-select.html "PostgreSQL 18 - SELECT")
( [18](https://www.postgresql.org/docs/18/sql-select.html "PostgreSQL 18 - SELECT"))


/

[17](https://www.postgresql.org/docs/17/sql-select.html "PostgreSQL 17 - SELECT")


/

[16](https://www.postgresql.org/docs/16/sql-select.html "PostgreSQL 16 - SELECT")


/

[15](https://www.postgresql.org/docs/15/sql-select.html "PostgreSQL 15 - SELECT")


/

[14](https://www.postgresql.org/docs/14/sql-select.html "PostgreSQL 14 - SELECT")

Development Versions:


[19](https://www.postgresql.org/docs/19/sql-select.html "PostgreSQL 19 - SELECT")

/
[devel](https://www.postgresql.org/docs/devel/sql-select.html "PostgreSQL devel - SELECT")

Unsupported versions:


[13](https://www.postgresql.org/docs/13/sql-select.html "PostgreSQL 13 - SELECT")

/
[12](https://www.postgresql.org/docs/12/sql-select.html "PostgreSQL 12 - SELECT")

/
[11](https://www.postgresql.org/docs/11/sql-select.html "PostgreSQL 11 - SELECT")

/
[10](https://www.postgresql.org/docs/10/sql-select.html "PostgreSQL 10 - SELECT")

/
[9.6](https://www.postgresql.org/docs/9.6/sql-select.html "PostgreSQL 9.6 - SELECT")

/
[9.5](https://www.postgresql.org/docs/9.5/sql-select.html "PostgreSQL 9.5 - SELECT")

/
[9.4](https://www.postgresql.org/docs/9.4/sql-select.html "PostgreSQL 9.4 - SELECT")

/
[9.3](https://www.postgresql.org/docs/9.3/sql-select.html "PostgreSQL 9.3 - SELECT")

/
[9.2](https://www.postgresql.org/docs/9.2/sql-select.html "PostgreSQL 9.2 - SEL

[…середина…]

tements are guaranteed to be executed once and only once, regardless of whether the primary query reads all or any of their output.

However, a `WITH` query can be marked `NOT MATERIALIZED` to remove this guarantee. In that case, the `WITH` query can be folded into the primary query much as though it were a simple sub-`SELECT` in the primary query's `FROM` clause. This results in duplicate computations if the primary query refers to that `WITH` query more than once; but if each such use requires only a few rows of the `WITH` query's total output, `NOT MATERIALIZED` can provide a net savings by allowing the queries to be optimized jointly. `NOT MATERIALIZED` is ignored if it is attached to a `WITH` query that is recursive or is not side-effect-free (i.e., is not a plain `SELECT` containing no volatile functions).

By default, a side-effect-free `WITH` query is folded into the primary query if it is used exactly once in the primary query's `FROM` clause. This allows joint optimization of the two query levels in situations where that should be semantically invisible. However, such folding can be prevented by marking the `WITH` query as `MATERIALIZED`. That might be useful, for example
```

**[tavily]** (1.67s, 32000 chars; wr=1.0, wo=None; hdr 3, code 0, links 7, lists 0)
```
![PostgreSQL Elephant Logo](/media/img/about/press/elephant.png)

| SELECT | | | | |
| --- | --- | --- | --- | --- |
| [Prev](sql-security-label.html "SECURITY LABEL") | [Up](sql-commands.html "SQL Commands") | SQL Commands | [Home](index.html "PostgreSQL 18.6 Documentation") | [Next](sql-selectinto.html "SELECT INTO") |

## SELECT

SELECT, TABLE, WITH — retrieve rows from a table or view

## Synopsis

`with_query`
`expression`
`expression`
`output_name`
`from_item`
`condition`
`grouping_element`
`condition`
`window_name`
`window_definition`
`select`
`expression`
`operator`
`count`
`start`
`count`
`from_reference`
`from_item`
`table_name`
`alias`
`column_alias`
`sampling_method`
`argument`
`seed`
`select`
`alias`
`column_alias`
`with_query_name`
`alias`
`column_alias`
`function_name`
`argument`
`alias`
`column_alias`
`function_name`
`argument`
`alias`
`column_definition`
`function_name`
`argument`
`column_definition`
`function_name`
`argument`
`column_definition`
`alias`
`column_alias`
`from_item`
`join_type`
`from_item`
`join_condition`
`join_column`
`join_using_alias`
`from_item`
`join_type`
`from_item`
`from_item`
`from_item`
`grouping_element`
`expression`
`expression`
`expression`
`expression`
`expression`
`expression`
`grouping_element`
`with_query`
`with_query_name`
`column_name`
`select`
`values`
`insert`
`update`
`delete`
`merge`
`column_name`
`search_seq_col_name`
`column_name`
`cycle_mark_col_name`
`cycle_mark_value`
`cycle_mark_default`
`cycle_path_col_name`
`table_name`

## Description

`SELECT` retrieves rows from zero or more tables. The general processing of `SELECT` is as follows:

`SELECT`
`SELECT`

All queries in the `WITH` list are computed. These effectively serve as temporary tables that can be referenced in the `FROM` list. A `WITH` query that is 

[…середина…]

the fraction of the table to sample, expressed as a percentage between 0 and 100. This argument can be any `real`-valued expression. (Other sampling methods might accept more or different arguments.) These two methods each return a randomly-chosen sample of the table that will contain approximately the specified percentage of the table's rows. The `BERNOULLI` method scans the whole table and selects or ignores individual rows independently with the specified probability. The `SYSTEM` method does block-level sampling with each block having the specified chance of being selected; all rows in each selected block are returned. The `SYSTEM` method is significantly faster than the `BERNOULLI` method when small sampling percentages are specified, but it may return a less-random sample of the table as a result of clustering effects.

`BERNOULLI`
`SYSTEM`
`argument`
`real`
`BERNOULLI`
`SYSTEM`
`SYSTEM`
`BERNOULLI`

The optional `REPEATABLE` clause specifies a *`seed`* number or expression to use for generating random numbers within the sampling method. The seed value can be any non-null floating-point value. Two queries that specify the same seed and *`argument`* values will select the same
```

**[jina]** ERROR: {"error": "all fetch providers failed for https://www.postgresql.org/docs/current/sql-select.html: jina: jina 451", "tri

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)

## U3: https://numpy.org/doc/stable/user/absolute_beginners.html
_(note: numpy-гайд с таблицами)_

**[local-auto]** (4.16s, 32000 chars, tier http; wr=1.0, wo=0.333; hdr 5, code 18, links 9, lists 0)
```
---
title: "NumPy: the absolute basics for beginners#"
url: https://numpy.org/doc/stable/user/absolute_beginners.html
hostname: numpy.org
sitename: NumPy v2.5 Manual
date: "2026-06-28"
---
# NumPy: the absolute basics for beginners[#](https://numpy.org#numpy-the-absolute-basics-for-beginners)

Welcome to the absolute beginner’s guide to NumPy!

NumPy (**Num**erical **Py**thon) is an open source Python library that’s
widely used in science and engineering. The NumPy library contains
multidimensional array data structures, such as the homogeneous, N-dimensional
`ndarray`, and a large library of functions that operate efficiently on these
data structures. Learn more about NumPy at [What is NumPy](https://numpy.org/whatisnumpy.html#whatisnumpy),
and if you have comments or suggestions, please
[reach out](https://numpy.org/community/)!

## How to import NumPy[#](https://numpy.org#how-to-import-numpy)

After [installing NumPy](https://numpy.org/install/), it may be imported
into Python code like:

```
import numpy as np
```
This widespread convention allows access to NumPy features with a short,
recognizable prefix (`np.`) while distinguishing NumPy features from others
that have the same name.

## Reading the example code[#](https://numpy.org#reading-the-example-code)

Throughout the NumPy documentation, you will find blocks that look like:

```
>>> a = np.array([[1, 2, 3],
...               [4, 5, 6]])
>>> a.shape
(2, 3)
```
Text preceded by `>>>` or `...` is **input**, the code that you would
enter in a script or at a Python prompt. Everything else is **output**, the
results of running your code. Note that `>>>` and `...` are not part of the
code and may cause an error if entered at a Python prompt.

To run the code in the examples, you can copy and paste it into a Python 

[…середина…]

s a **Column-major language**.
In C on the other hand, the **last** index changes
the most rapidly. The matrix is stored by rows, making it a **Row-major
language**. What you do for C or Fortran depends on whether it’s more important
to preserve the indexing convention or not reorder the data.

## How to convert a 1D array into a 2D array (how to add a new axis to an array)[#](https://numpy.org#how-to-convert-a-1d-array-into-a-2d-array-how-to-add-a-new-axis-to-an-array)

*This section covers* `np.newaxis`, `np.expand_dims`

You can use `np.newaxis` and `np.expand_dims` to increase the dimensions of
your existing array.

Using `np.newaxis` will increase the dimensions of your array by one dimension
when used once. This means that a **1D** array will become a **2D** array, a
**2D** array will become a **3D** array, and so on.

For example, if you start with this array:

```
>>> a = np.array([1, 2, 3, 4, 5, 6])
>>> a.shape
(6,)
```
You can use `np.newaxis` to add a new axis:

```
>>> a2 = a[np.newaxis, :]
>>> a2.shape
(1, 6)
```
You can explicitly convert a 1D array to either a row vector or a column
vector using `np.newaxis`. For example, you can convert a 1D array to a row
vector by
```

**[local-http]** (3.77s, 32000 chars, tier http; wr=1.0, wo=0.333; hdr 5, code 18, links 9, lists 0)
```
---
title: "NumPy: the absolute basics for beginners#"
url: https://numpy.org/doc/stable/user/absolute_beginners.html
hostname: numpy.org
sitename: NumPy v2.5 Manual
date: "2026-06-28"
---
# NumPy: the absolute basics for beginners[#](https://numpy.org#numpy-the-absolute-basics-for-beginners)

Welcome to the absolute beginner’s guide to NumPy!

NumPy (**Num**erical **Py**thon) is an open source Python library that’s
widely used in science and engineering. The NumPy library contains
multidimensional array data structures, such as the homogeneous, N-dimensional
`ndarray`, and a large library of functions that operate efficiently on these
data structures. Learn more about NumPy at [What is NumPy](https://numpy.org/whatisnumpy.html#whatisnumpy),
and if you have comments or suggestions, please
[reach out](https://numpy.org/community/)!

## How to import NumPy[#](https://numpy.org#how-to-import-numpy)

After [installing NumPy](https://numpy.org/install/), it may be imported
into Python code like:

```
import numpy as np
```
This widespread convention allows access to NumPy features with a short,
recognizable prefix (`np.`) while distinguishing NumPy features from others
that have the same name.

## Reading the example code[#](https://numpy.org#reading-the-example-code)

Throughout the NumPy documentation, you will find blocks that look like:

```
>>> a = np.array([[1, 2, 3],
...               [4, 5, 6]])
>>> a.shape
(2, 3)
```
Text preceded by `>>>` or `...` is **input**, the code that you would
enter in a script or at a Python prompt. Everything else is **output**, the
results of running your code. Note that `>>>` and `...` are not part of the
code and may cause an error if entered at a Python prompt.

To run the code in the examples, you can copy and paste it into a Python 

[…середина…]

s a **Column-major language**.
In C on the other hand, the **last** index changes
the most rapidly. The matrix is stored by rows, making it a **Row-major
language**. What you do for C or Fortran depends on whether it’s more important
to preserve the indexing convention or not reorder the data.

## How to convert a 1D array into a 2D array (how to add a new axis to an array)[#](https://numpy.org#how-to-convert-a-1d-array-into-a-2d-array-how-to-add-a-new-axis-to-an-array)

*This section covers* `np.newaxis`, `np.expand_dims`

You can use `np.newaxis` and `np.expand_dims` to increase the dimensions of
your existing array.

Using `np.newaxis` will increase the dimensions of your array by one dimension
when used once. This means that a **1D** array will become a **2D** array, a
**2D** array will become a **3D** array, and so on.

For example, if you start with this array:

```
>>> a = np.array([1, 2, 3, 4, 5, 6])
>>> a.shape
(6,)
```
You can use `np.newaxis` to add a new axis:

```
>>> a2 = a[np.newaxis, :]
>>> a2.shape
(1, 6)
```
You can explicitly convert a 1D array to either a row vector or a column
vector using `np.newaxis`. For example, you can convert a 1D array to a row
vector by
```

**[local-curl]** (3.76s, 32000 chars, tier curl; wr=1.0, wo=0.333; hdr 5, code 18, links 9, lists 0)
```
---
title: "NumPy: the absolute basics for beginners#"
url: https://numpy.org/doc/stable/user/absolute_beginners.html
hostname: numpy.org
sitename: NumPy v2.5 Manual
date: "2026-06-28"
---
# NumPy: the absolute basics for beginners[#](https://numpy.org#numpy-the-absolute-basics-for-beginners)

Welcome to the absolute beginner’s guide to NumPy!

NumPy (**Num**erical **Py**thon) is an open source Python library that’s
widely used in science and engineering. The NumPy library contains
multidimensional array data structures, such as the homogeneous, N-dimensional
`ndarray`, and a large library of functions that operate efficiently on these
data structures. Learn more about NumPy at [What is NumPy](https://numpy.org/whatisnumpy.html#whatisnumpy),
and if you have comments or suggestions, please
[reach out](https://numpy.org/community/)!

## How to import NumPy[#](https://numpy.org#how-to-import-numpy)

After [installing NumPy](https://numpy.org/install/), it may be imported
into Python code like:

```
import numpy as np
```
This widespread convention allows access to NumPy features with a short,
recognizable prefix (`np.`) while distinguishing NumPy features from others
that have the same name.

## Reading the example code[#](https://numpy.org#reading-the-example-code)

Throughout the NumPy documentation, you will find blocks that look like:

```
>>> a = np.array([[1, 2, 3],
...               [4, 5, 6]])
>>> a.shape
(2, 3)
```
Text preceded by `>>>` or `...` is **input**, the code that you would
enter in a script or at a Python prompt. Everything else is **output**, the
results of running your code. Note that `>>>` and `...` are not part of the
code and may cause an error if entered at a Python prompt.

To run the code in the examples, you can copy and paste it into a Python 

[…середина…]

s a **Column-major language**.
In C on the other hand, the **last** index changes
the most rapidly. The matrix is stored by rows, making it a **Row-major
language**. What you do for C or Fortran depends on whether it’s more important
to preserve the indexing convention or not reorder the data.

## How to convert a 1D array into a 2D array (how to add a new axis to an array)[#](https://numpy.org#how-to-convert-a-1d-array-into-a-2d-array-how-to-add-a-new-axis-to-an-array)

*This section covers* `np.newaxis`, `np.expand_dims`

You can use `np.newaxis` and `np.expand_dims` to increase the dimensions of
your existing array.

Using `np.newaxis` will increase the dimensions of your array by one dimension
when used once. This means that a **1D** array will become a **2D** array, a
**2D** array will become a **3D** array, and so on.

For example, if you start with this array:

```
>>> a = np.array([1, 2, 3, 4, 5, 6])
>>> a.shape
(6,)
```
You can use `np.newaxis` to add a new axis:

```
>>> a2 = a[np.newaxis, :]
>>> a2.shape
(1, 6)
```
You can explicitly convert a 1D array to either a row vector or a column
vector using `np.newaxis`. For example, you can convert a 1D array to a row
vector by
```

**[local-browser]** ERROR: network/

**[firecrawl]** (4.6s, 32000 chars; wr=0.333, wo=0.333; hdr 2, code 13, links 25, lists 2)
```
[Skip to main content](https://numpy.org/doc/stable/user/absolute_beginners.html#main-content)

Back to top`Ctrl` + `K`

LightDarkSystem Settings

2.5 (stable)

[dev](https://numpy.org/devdocs/user/absolute_beginners.html) [2.5 (stable)](https://numpy.org/doc/stable/user/absolute_beginners.html) [2.4](https://numpy.org/doc/2.4/user/absolute_beginners.html) [2.3](https://numpy.org/doc/2.3/user/absolute_beginners.html) [2.2](https://numpy.org/doc/2.2/user/absolute_beginners.html) [2.1](https://numpy.org/doc/2.1/user/absolute_beginners.html) [2.0](https://numpy.org/doc/2.0/user/absolute_beginners.html) [1.26](https://numpy.org/doc/1.26/user/absolute_beginners.html) [1.25](https://numpy.org/doc/1.25/user/absolute_beginners.html) [1.24](https://numpy.org/doc/1.24/user/absolute_beginners.html) [1.23](https://numpy.org/doc/1.23/user/absolute_beginners.html) [1.22](https://numpy.org/doc/1.22/user/absolute_beginners.html) [1.21](https://numpy.org/doc/1.21/user/absolute_beginners.html) [1.20](https://numpy.org/doc/1.20/user/absolute_beginners.html) [1.19](https://numpy.org/doc/1.19/user/absolute_beginners.html) [1.18](https://numpy.org/doc/1.18/user/absolute_beginners.html) [1.17](https://numpy.org/doc/1.17/user/absolute_beginners.html) [1.16](https://numpy.org/doc/1.16/user/absolute_beginners.html) [1.15](https://numpy.org/doc/1.15/user/absolute_beginners.html) [1.14](https://numpy.org/doc/1.14/user/absolute_beginners.html) [1.13](https://numpy.org/doc/1.13/user/absolute_beginners.html)

- [GitHub](https://github.com/numpy/numpy)

Collapse SidebarExpand Sidebar

# NumPy: the absolute basics for beginners [\#](https://numpy.org/doc/stable/user/absolute_beginners.html\#numpy-the-absolute-basics-for-beginners "Link to this heading")

Welcome to the absolute beginner’s guide to NumP

[…середина…]

f elements of the array. This
is the _product_ of the elements of the array’s shape.

`ndarray.shape` will display a tuple of integers that indicate the number of
elements stored along each dimension of the array. If, for example, you have a
2-D array with 2 rows and 3 columns, the shape of your array is `(2, 3)`.

For example, if you create this array:

```
>>> array_example = np.array([[[0, 1, 2, 3],\
...                            [4, 5, 6, 7]],\
...\
...                           [[0, 1, 2, 3],\
...                            [4, 5, 6, 7]],\
...\
...                           [[0 ,1 ,2, 3],\
...                            [4, 5, 6, 7]]])
```

Copy to clipboard

To find the number of dimensions of the array, run:

```
>>> array_example.ndim
3
```

Copy to clipboard

To find the total number of elements in the array, run:

```
>>> array_example.size
24
```

Copy to clipboard

And to find the shape of your array, run:

```
>>> array_example.shape
(3, 2, 4)
```

Copy to clipboard

## Can you reshape an array? [\#](https://numpy.org/doc/stable/user/absolute_beginners.html\#can-you-reshape-an-array "Link to this heading")

_This section covers_`arr.reshape()`

* * *

**Yes!**

Using 
```

**[tavily]** (1.4s, 32000 chars; wr=1.0, wo=0.333; hdr 5, code 14, links 13, lists 1)
```
[![NumPy v2.5 Manual - Home](../_static/numpylogo.svg) ![NumPy v2.5 Manual - Home](../_static/numpylogo_dark.svg)](../index.html)

* [GitHub](https://github.com/numpy/numpy "GitHub")

# NumPy: the absolute basics for beginners[#](#numpy-the-absolute-basics-for-beginners "Link to this heading")

Welcome to the absolute beginner’s guide to NumPy!

NumPy (**Num**erical **Py**thon) is an open source Python library that’s widely used in science and engineering. The NumPy library contains multidimensional array data structures, such as the homogeneous, N-dimensional `ndarray`, and a large library of functions that operate efficiently on these data structures. Learn more about NumPy at [What is NumPy](whatisnumpy.html#whatisnumpy), and if you have comments or suggestions, please [reach out](https://numpy.org/community/)!

## How to import NumPy[#](#how-to-import-numpy "Link to this heading")

After [installing NumPy](https://numpy.org/install/), it may be imported into Python code like:

```
 import  numpy  as  np
```

This widespread convention allows access to NumPy features with a short, recognizable prefix (`np.`) while distinguishing NumPy features from others that have the same name.

## Reading the example code[#](#reading-the-example-code "Link to this heading")

Throughout the NumPy documentation, you will find blocks that look like:

```
>>> a = np. array([[1, 2, 3],... [4, 5, 6]])>>> a. shape(2, 3)
```

Text preceded by `>>>` or `...` is **input**, the code that you would enter in a script or at a Python prompt. Everything else is **output**, the results of running your code. Note that `>>>` and `...` are not part of the code and may cause an error if entered at a Python prompt.

To run the code in the examples, you can copy and paste it into a Python script or REPL

[…середина…]

dly varying index. As the first index moves to the next row as it changes, the matrix is stored one column at a time. This is why Fortran is thought of as a **Column-major language**. In C on the other hand, the **last** index changes the most rapidly. The matrix is stored by rows, making it a **Row-major language**. What you do for C or Fortran depends on whether it’s more important to preserve the indexing convention or not reorder the data.

[Learn more about shape manipulation here](quickstart.html#quickstart-shape-manipulation).

## How to convert a 1D array into a 2D array (how to add a new axis to an array)[#](#how-to-convert-a-1d-array-into-a-2d-array-how-to-add-a-new-axis-to-an-array "Link to this heading")

*This section covers* `np.newaxis`, `np.expand_dims`

---

You can use `np.newaxis` and `np.expand_dims` to increase the dimensions of your existing array.

Using `np.newaxis` will increase the dimensions of your array by one dimension when used once. This means that a **1D** array will become a **2D** array, a **2D** array will become a **3D** array, and so on.

For example, if you start with this array:

```
>>> a = np. array([1, 2, 3, 4, 5, 6])>>> a. shape(6,)
```


```

**[jina]** ERROR: {"error": "all fetch providers failed for https://numpy.org/doc/stable/user/absolute_beginners.html: jina: jina network:

**[parallel]** — не прогонялся (для parallel — норм, если нет пометки)
