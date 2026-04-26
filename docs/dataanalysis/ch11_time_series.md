# Time Series

Time series data is very important form of structured data, appearing in almost all fields of life. Any kind of measurement/experiment observed over time will always yield Time Series data.

Many time series are *fixed-frequency*, and many are *irregular*

- Timestamps : Specific instants in time
- Fixed Periods : such as whole of Jan 2017, or whole year 2022
- Interval of time : indicated by start and end timestamps. Periods can be special case of intervals.
- Experiment or elapsed time : Timestamp is measure of time relative to a particular start time.

Following notes deals with first 3 types of data.

## Date and Time Data Types and Tools

Python has `datetime`, `time` and `calendar` modules. The `datetime.datetime` type or simply `datetime` is widely used.

```python
from datetime import datetime

now = datetime.now()
now

# datetime.datetime(2026, 3, 7, 15, 6, 38, 803325)
# microsecond precision here ^
```

`datetime.timedelta` measures temporal difference between two `datetime` objects.

```python
delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)

# datetime.timedelta(days=926, seconds=56700)

now + timedelta(12) # default is days
# datetime.datetime(2026, 3, 19, 15, 9, 51, 191217)

```

### Converting Between String and DateTime

```python
stamp = datetime(2011, 1, 3)

str(stamp) # '2011-01-03 00:00:00'
stamp.strftime("%Y-%m-%d") # '2011-01-03'

```

Converting string to datetime

```python
value = "2011-01-03"
datetime.strptime(value, "%Y-%m-%d")
```

In Pandas

```python
datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]

pd.to_datetime(datestrs)
# DatetimeIndex(['2011-07-06 12:00:00', '2011-08-06 00:00:00'], dtype='datetime64[ns]', freq=None)
```

Above functions handles None passed to it, product `NaT` in response

## Time Series Basics

```python
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5),
         datetime(2011, 1, 7), datetime(2011, 1, 8),
         datetime(2011, 1, 10), datetime(2011, 1, 12)]

ts = pd.Series(np.random.standard_normal(6), index=dates)

# ------
2011-01-02   -0.507327
2011-01-05   -1.098457
2011-01-07   -0.860981
2011-01-08   -2.028304
2011-01-10   -0.542983
2011-01-12   -1.274586
dtype: float64
# ------
ts.index # all datetime objects have been put into DatetimeIndex

# Like other series arithmetic operations, differently indexed time series automatically align on dates
ts + ts[::2] # every second element in ts

# ---------
2011-01-02   -1.014655
2011-01-05         NaN
2011-01-07   -1.721961
2011-01-08         NaN
2011-01-10   -1.085967
2011-01-12         NaN
dtype: float64

# ----------


```

pandas stores timestamps using NumPy's `datetime64` data type at the nanosecond resolution.

Scalar values from a `DatetimeIndex` are pandas `Timestamp` objects

```python
stamp = ts.index[0]

stamp # Timestamp('2011-01-02 00:00:00')
```

### Indexing, Selection, Subsetting

```python
stamp = ts.index[2]
ts[stamp] # access the object

ts["2011-01-10"] # accesses the ts

longer_ts = pd.Series(np.random.standard_normal(1000),
                      index=pd.date_range("2000-01-01", periods=1000))

longer_ts["2001"] # select slices of data matching 2001

2001-01-01    1.599534
2001-01-02    0.474071
2001-01-03    0.151326
2001-01-04   -0.542173
2001-01-05   -0.475496
                ...   
2001-12-27    0.057874
2001-12-28   -0.433739
2001-12-29    0.092698
2001-12-30   -1.397820
2001-12-31    1.457823
Freq: D, Length: 365, dtype: float64

longer_ts["2001-05"] # return selection with date and time

ts[datetime(2011, 1, 7):] # any time after this

ts[datetime(2011, 1, 7):datetime(2011, 1, 10)]


# since timeseries is sorted by timestamps

ts["2011-01-06":"2011-01-11"]

ts.truncate(after="2011-01-09")
```

DataFrame works as similar way.

```python
dates = pd.date_range("2000-01-01", periods=100, freq="W-WED")

long_df = pd.DataFrame(np.random.standard_normal((100, 4)),
                       index=dates,
                       columns=["Colorado", "Texas",
                                "New York", "Ohio"])

long_df.loc["2001-05"]

            Colorado     Texas  New York      Ohio
2001-05-02 -0.006045  0.490094 -0.277186 -0.707213
2001-05-09 -0.560107  2.735527  0.927335  1.513906
2001-05-16  0.538600  1.273768  0.667876 -0.969206
2001-05-23  1.676091 -0.817649  0.050188  1.951312
2001-05-30  3.260383  0.963301  1.201206 -1.852001
```

### Time Series with Duplicate Indices

There can be multiple data observations falling on a particular timestamp.

```python
dates = pd.DatetimeIndex(["2000-01-01", "2000-01-02", "2000-01-02",
                          "2000-01-02", "2000-01-03"])

dup_ts = pd.Series(np.arange(5), index=dates)

### ----
2000-01-01    0
2000-01-02    1
2000-01-02    2
2000-01-02    3
2000-01-03    4
dtype: int64

dup_ts.index.is_unique # False

dup_ts["2000-01-03"] # 4, not duplicated

dup_ts["2000-01-02"] # duplicated

2000-01-02    1
2000-01-02    2
2000-01-02    3
dtype: int64

```

Suppose you wanted to aggregate the data having non-unique timestamps.

```python
grouped = dup_ts.groupby(level = 0)
grouped.mean()
grouped.count()

## ---------
2000-01-01    1
2000-01-02    3
2000-01-03    1
## =------==--=
```

## Date Ranges, Frequencies, and Shifting

Generic Time Series in pandas are assumed to be irregular, that is, they have no fixed frequency. However it's often desirable to work relative to a fixed frequency, such as daily, monthly, every 15 min, even introducing fill values even if they are not present.

```python
ts
2011-01-02   -0.204708
2011-01-05    0.478943
2011-01-07   -0.519439
2011-01-08   -0.555730
2011-01-10    1.965781
2011-01-12    1.393406
dtype: float64

# sampler
resampler = ts.resample("D")
resampler # D ~ daily frequency

```

### Generating Date Ranges

```python
index = pd.date_range("2012-04-01", "2012-06-01")

index 
# DatetimeIndex(['2012-04-01', '2012-04-02', '2012-04-03', '2012-04-04',
#               '2012-04-05', '2012-04-06', '2012-04-07', '2012-04-08',
#               ....
#               '2012-05-31', '2012-06-01'],
#              dtype='datetime64[ns]', freq='D')

# default is daily timestamps, 
pd.date_range(start="2012-04-01", periods=20) # 20 next periods after the start

pd.date_range(end="2012-06-01", periods=20) # 20 periods before the end

pd.date_range("2000-01-01", "2000-12-01", freq="BME") # Business end of month
```

```python
pd.date_range("2012-05-02 12:56:31", periods=5) # by default time is preserved
pd.date_range("2012-05-02 12:56:31", periods=5, normalize=True) # time is normalized to midnight and truncated.
```

### Frequencies and Date Offsets

Frequencies in pandas are composed of base frequencies and a multiplier. Examples of base frequencies: `"h"` (hourly), `"ME"` (month end)

```python
from pandas.tseries.offsets import Hour, Minute

hour = Hour()
four_hours = Hour(4)

pd.date_range("2000-01-01", "2000-01-03 23:59", freq="4h") # mostly explicit offsets are not required

# combining offsets
Hour(2) + Minute(30)

pd.date_range("2000-01-01", periods=10, freq="1h30min")
```

#### Week of Month dates

One useful frequency class is `week of months` (WOM). Enables to get dates like third friday of each month.

```python
monthly_dates = pd.date_range("2012-01-01", "2012-09-01", freq="WOM-3FRI")
list(monthly_dates)
```

### Shifting (Leading and Lagging) Data

```python
ts = pd.Series(np.random.standard_normal(4),
               index=pd.date_range("2000-01-01", periods=4, freq="ME"))
ts

# ----
2000-01-31   -0.066748
2000-02-29    0.838639
2000-03-31   -0.117388
2000-04-30   -0.517795
Freq: ME, dtype: float64
# -----            
ts.shift(2)

2000-01-31         NaN
2000-02-29         NaN
2000-03-31   -0.066748
2000-04-30    0.838639

# similarily backward shift will produce NaN from bottom
```

A common use of shift is computing consecutive percent changes in a time series or multiple time series as DataFrame columns

```python
ts / ts.shift(1) - 1

# naive shift usually shifts data not indexes
# to shift indexes
ts.shift(2, freq="ME") # passing freq, shifts the index

2000-03-31   -0.066748
2000-04-30    0.838639
2000-05-31   -0.117388
2000-06-30   -0.517795
```

### Shifting Dates with Offsets

The pandas date offsets can also be used with datetime or Timestamp objects

```python
from pandas.tseries.offsets import Day, MonthEnd
now = datetime(2011, 11, 17)

now + 3 * Day() # Timestamp('2011-11-20 00:00:00')

now + MonthEnd() # Timestamp('2011-11-30 00:00:00')

now + MonthEnd(2) # Timestamp('2011-12-31 00:00:00')

offset = MonthEnd()
offset.rollforward(now) # Timestamp('2011-11-30 00:00:00')
offset.rollback(now) # Timestamp('2011-10-31 00:00:00')
```

Example collecting data with groupby MonthEnd

```python
ts.groupby(MonthEnd().rollforward).mean()

# faster way
ts.resample("M").mean()
```
## Time-Zone Handling

This is very hard problem to solve in general. Many time series users choose to work with time series in coordinated universal time or UTC, which is the geography-independent international standard.

Problem is standard have changed way too many times to get the conversions right. So you better off rely on libraries. [Explanation](https://www.youtube.com/watch?v=-5wpm-gesOY)

Use `pytz` for timezone in python.

```python
import pytz
pytz.common_timezones[-5:] # ['US/Eastern', 'US/Hawaii', 'US/Mountain', 'US/Pacific', 'UTC']

tz = pytz.timezone("America/New_York") # <DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>
```

### Time Zone Localization and Conversion

By default, time series in pandas are time zone naive.

```python
dates = pd.date_range("2012-03-09 09:30", periods=6)
ts = pd.Series(np.random.standard_normal(len(dates)), index=dates)

print(ts.index.tz) # None
dates = pd.date_range("2012-03-09 09:30", periods=6, tz = "UTC") # handled by `tz_localize` internally.

ts_utc = ts.tz_localize("UTC")
ts_utc.index
ts_utc.tz_convert("America/New_York")

ts_eastern = ts.tz_localize("America/New_York")

ts_eastern.tz_convert("Europe/Berlin")

```

Individual `Timestamp` objects can also be localized from naive to time-zone aware and converted from one time zone to another or could be passed during creation.

By Default Pandas will respect daylight saving time transitions wherever possible when performing offsets.

```python
stamp = pd.Timestamp("2012-03-11 01:30", tz="US/Eastern")

stamp + Hour()
# Timestamp('2012-03-11 03:30:00-0400', tz='US/Eastern')
```

If two timezones being operated on are in different timezones, results will always be UTC.

## Periods and Period Arithmetic

Periods represent time spans, like days, months, quarters, or years.

```python
p = pd.Period("2011", freq="A-DEC") # Period('2011', 'A-DEC')

p + 5 # Period('2016', 'A-DEC')

p - 2 # Period('2009', 'A-DEC')

pd.Period("2014", freq="A-DEC") - p # <3 * YearEnds: month=12> # notice the type is offset, when two periods are subtracted.

periods = pd.period_range("2000-01-01", "2000-06-30", freq="M")
# PeriodIndex(['2000-01', '2000-02', '2000-03', '2000-04', '2000-05', '2000-06'], dtype='period[M]')

```

```python
values = ["2001Q3", "2002Q2", "2003Q1"]

index = pd.PeriodIndex(values, freq="Q-DEC")
# PeriodIndex(['2001Q3', '2002Q2', '2003Q1'], dtype='period[Q-DEC]')

```

### Period Frequency Conversion

Periods and `PeriodIndex` objects can be converted into another frequency with their `asfreq` method.

```python
p = pd.Period("2011", freq="A-DEC") # Period('2011', 'A-DEC')

p.asfreq("M", how = "start") # Period('2011-01', 'M')
p.asfreq("M", how = "end")
p.asfreq("M") # Period('2011-12', 'M')

```

```python
p = pd.Period("2011", freq="A-JUN")

p.asfreq("M", how="start") # Period('2010-07', 'M') # fiscal year start on 07
p.asfreq("M", how="end") # Period('2011-06', 'M') # because fiscal year ends on 06
```

```python
# A-JUN frequency, the month Aug-2011 is actually part of the 2012 period
p = pd.Period("Aug-2011", "M")

p.asfreq("A-JUN") # Period('2012', 'A-JUN')

```
### Quarterly Period Frequencies

Quarterly data is standard in accounting, finance, and other fields. Much quarterly data is reported relative to a fiscal year end, typically the last calendar or business day of one of the 12 months of the year. Thus, the period `2012Q4` has a different meaning depending on fiscal year end. pandas supports all 12 possible quarterly frequencies as `Q-JAN` through `Q-DEC`

```python

p = pd.Period("2012Q4", freq="Q-JAN") # Period('2012Q4', 'Q-JAN')

p.asfreq("D", how="start") # Period('2011-11-01', 'D')

p.asfreq("D", how="end") # Period('2012-01-31', 'D')
```


The `to_timestamp` method returns the Timestamp at the start of the period by default.
You can generate quarterly ranges using `pandas.period_range`

```python
periods = pd.period_range("2011Q3", "2012Q4", freq="Q-JAN")
ts = pd.Series(np.arange(len(periods)), index=periods)

 # ------ ts
2011Q3    0
2011Q4    1
2012Q1    2
2012Q2    3
2012Q3    4
2012Q4    5
Freq: Q-JAN, dtype: int64

new_periods = (periods.asfreq("B", "end") - 1).asfreq("H", "start") + 16

ts.index = new_periods.to_timestamp()

# ----- ts
2010-10-28 16:00:00    0
2011-01-28 16:00:00    1
2011-04-28 16:00:00    2
2011-07-28 16:00:00    3
2011-10-28 16:00:00    4
2012-01-30 16:00:00    5
dtype: int64
```

### Converting Timestamps to Period

Series and DataFrame objects indexed by timestamps can be converted to periods with the `to_period` method

```python
dates = pd.date_range("2000-01-01", periods=3, freq="M")
ts = pd.Series(np.random.standard_normal(3), index=dates)

# ------- ts --------
2000-01-31    1.663261
2000-02-29   -0.996206
2000-03-31    1.521760
Freq: M, dtype: float64

pts = ts.to_period()

# ------- pts ------
2000-01    1.663261
2000-02   -0.996206
2000-03    1.521760
Freq: M, dtype: float64
```

Since periods refer to nonoverlapping time spans, a timestamp can only belong to a single period for a given frequency. While the frequency of the new `PeriodIndex` is inferred from the timestamps by default, you can specify any supported frequency

```python
dates = pd.date_range("2000-01-29", periods=6)
ts2 = pd.Series(np.random.standard_normal(6), index=dates)

# -------- ts2 ---------
2000-01-29    0.244175
2000-01-30    0.423331
2000-01-31   -0.654040
2000-02-01    2.089154
2000-02-02   -0.060220
2000-02-03   -0.167933
Freq: D, dtype: float64

ts2.to_period("M")

2000-01    0.244175
2000-01    0.423331
2000-01   -0.654040
2000-02    2.089154
2000-02   -0.060220
2000-02   -0.167933
Freq: M, dtype: float64
```

```python
pts = ts2.to_period()
pts.to_timestamp(how="end")
```

### Creating a PeriodIndex from Arrays

Fixed frequency datasets are sometimes stored with time span information spread across multiple columns.

```python
data = pd.read_csv("examples/macrodata.csv")
data.head(5)

   year  quarter   realgdp  realcons  realinv  realgovt  realdpi    cpi  \
0  1959        1  2710.349    1707.4  286.898   470.045   1886.9  28.98   
1  1959        2  2778.801    1733.7  310.859   481.301   1919.7  29.15   
2  1959        3  2775.488    1751.8  289.226   491.260   1916.4  29.35   
3  1959        4  2785.204    1753.7  299.356   484.052   1931.3  29.37   
4  1960        1  2847.699    1770.5  331.722   462.199   1955.5  29.54   
      m1  tbilrate  unemp      pop  infl  realint  
0  139.7      2.82    5.8  177.146  0.00     0.00  
1  141.7      3.08    5.1  177.830  2.34     0.74  
2  140.5      3.82    5.3  178.657  2.74     1.09  
3  140.0      4.33    5.6  179.386  0.27     4.06  
4  139.6      3.50    5.2  180.007  2.31     1.19  
```

By passing these arrays to PeriodIndex with a frequency, you can combine them to form an index for the DataFrame:

```python
index = pd.PeriodIndex(year=data["year"], quarter=data["quarter"],
                       freq="Q-DEC")

data.index = index
data["infl"]
```
## Resampling and Frequency Conversion

Resampling refers to conversion of time series from one frequency to another, *upsampling* refers to increasing frequency either by more observations or interpolation. *downsampling* refers to decreasing frequency by dropping or aggregating data in the intervals.

pandas object generally have `resample` method, handling all frequency conversions. `resample` has similar API to `groupby`

```python
dates = pd.date_range("2000-01-01", periods=100)
ts = pd.Series(np.random.standard_normal(len(dates)), index=dates)

ts.resample("ME").mean()

2000-01-31   -0.165893
2000-02-29    0.078606
2000-03-31    0.223811
2000-04-30   -0.063643
Freq: M, dtype: float64

ts.resample("M", kind="period").mean() # ~ deprecated, defaults to type of index

```

### Downsampling

Generally each interval is said to be *half-open*; a data can belong only to one interval, and union of frame should make up the entire time frame.

```python

dates = pd.date_range("2000-01-01", periods=12, freq="min")
ts = pd.Series(np.arange(len(dates)), index=dates)

## aggregating in 5 min bars # [0, 5), [5, 10), [10] ~ 3 intervals
ts.resample("5min").sum()

2000-01-01 00:00:00    10
2000-01-01 00:05:00    35
2000-01-01 00:10:00    21
Freq: 5min, dtype: int64

ts.resample("5min", closed="right").sum() # label is from left edge now, 

1999-12-31 23:55:00     0
2000-01-01 00:00:00    15
2000-01-01 00:05:00    40
2000-01-01 00:10:00    11
Freq: 5min, dtype: int64

ts.resample("5min", closed="right", label="right").sum()
2000-01-01 00:00:00     0
2000-01-01 00:05:00    15
2000-01-01 00:10:00    40
2000-01-01 00:15:00    11
Freq: 5T, dtype: int64
```

```python
# offsets
result.index = result.index + to_offset("-1s")
```

#### OHLC ~ Open High Low Close

In finance, a popular way to aggregate a time series is to compute four values for each bucket: the first (open), last (close), maximum (high), and minimal (low) values. By using the `ohlc` aggregate function, you will obtain a DataFrame having columns containing these four aggregates, which are efficiently computed in a single function call:

```python
ts = pd.Series(np.random.permutation(np.arange(len(dates))), index=dates)
ts.resample("5min").ohlc()

# ------
                     open  high  low  close
2000-01-01 00:00:00     8     8    1      5
2000-01-01 00:05:00     6    11    2      2
2000-01-01 00:10:00     0     7    0      7
```
### Upsampling and Interpolation

Upsampling is converting from a lower frequency to a higher frequency, where no aggregation is needed.

```python

frame = pd.DataFrame(np.random.standard_normal((2, 4)),
                     index=pd.date_range("2000-01-01", periods=2,
                                         freq="W-WED"),
                     columns=["Colorado", "Texas", "New York", "Ohio"])

# -- ---- -- - frame

            Colorado     Texas  New York      Ohio
2000-01-05 -0.896431  0.927238  0.482284 -0.867130
2000-01-12  0.493841 -0.155434  1.397286  1.507055
```

```python
df_daily = frame.resample("D").asfreq()

# ------
            Colorado     Texas  New York      Ohio
2000-01-05 -0.896431  0.927238  0.482284 -0.867130
2000-01-06       NaN       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN       NaN
2000-01-08       NaN       NaN       NaN       NaN
2000-01-09       NaN       NaN       NaN       NaN
2000-01-10       NaN       NaN       NaN       NaN
2000-01-11       NaN       NaN       NaN       NaN
2000-01-12  0.493841 -0.155434  1.397286  1.507055

frame.resample("D").ffill()

# ---
            Colorado     Texas  New York      Ohio
2000-01-05 -0.896431  0.927238  0.482284 -0.867130
2000-01-06 -0.896431  0.927238  0.482284 -0.867130
2000-01-07 -0.896431  0.927238  0.482284 -0.867130
2000-01-08 -0.896431  0.927238  0.482284 -0.867130
2000-01-09 -0.896431  0.927238  0.482284 -0.867130
2000-01-10 -0.896431  0.927238  0.482284 -0.867130
2000-01-11 -0.896431  0.927238  0.482284 -0.867130
2000-01-12  0.493841 -0.155434  1.397286  1.507055

frame.resample("D").ffill(limit=2) # only 2 values are filled forward

```

```python
frame.resample("W-THU").ffill()
            Colorado     Texas  New York      Ohio
2000-01-06 -0.896431  0.927238  0.482284 -0.867130
2000-01-13  0.493841 -0.155434  1.397286  1.507055
```
### Resampling and Periods

```python
frame = pd.DataFrame(np.random.standard_normal((24, 4)),
                     index=pd.period_range("1-2000", "12-2001",
                                           freq="M"),
                     columns=["Colorado", "Texas", "New York", "Ohio"])

frame.head()
# ------
         Colorado     Texas  New York      Ohio
2000-01 -1.179442  0.443171  1.395676 -0.529658
2000-02  0.787358  0.248845  0.743239  1.267746
2000-03  1.302395 -0.272154 -0.051532 -0.467740
2000-04 -1.040816  0.426419  0.312945 -1.115689
2000-05  1.234297 -1.893094 -1.661605 -0.005477

annual_frame = frame.resample("Y-DEC").mean()

annual_frame
# ------
      Colorado     Texas  New York      Ohio
2000  0.487329  0.104466  0.020495 -0.273945
2001  0.203125  0.162429  0.056146 -0.103794
```

Upsampling is more nuanced, as before resampling you must make a decision about which end of the time span in the new frequency to place the values. The `convention` argument defaults to `"start"` but can also be `"end"`

Since periods refer to time spans, the rules about upsampling and downsampling are more rigid:

- In downsampling, the target frequency must be a _subperiod_ of the source frequency.
- In upsampling, the target frequency must be a _superperiod_ of the source frequency.
### Grouped Time Resampling

For time series data, the `resample` method is semantically a group operation based on a time intervalization.

```python
times = pd.date_range("2017-05-20 00:00", freq="1min", periods= 15)
df = pd.DataFrame({"time": times,
                   "value": np.arange(15)})
                   
df.set_index("time").resample("5min").count()

# ------
                     value
time                      
2017-05-20 00:00:00      5
2017-05-20 00:05:00      5
2017-05-20 00:10:00      5

df2 = pd.DataFrame({"time": times.repeat(3),
                    "key": np.tile(["a", "b", "c"], N),
                    "value": np.arange(N * 3.)})

df2.head()

## -----
                 time key  value
0 2017-05-20 00:00:00   a    0.0
1 2017-05-20 00:00:00   b    1.0
2 2017-05-20 00:00:00   c    2.0
3 2017-05-20 00:01:00   a    3.0
4 2017-05-20 00:01:00   b    4.0
5 2017-05-20 00:01:00   c    5.0
6 2017-05-20 00:02:00   a    6.0

```

```python
time_key = pd.Grouper(freq="5min")
resampled = (df2.set_index("time")
             .groupby(["key", time_key])
             .sum())

                         value
key time                      
a   2017-05-20 00:00:00   30.0
    2017-05-20 00:05:00  105.0
    2017-05-20 00:10:00  180.0
b   2017-05-20 00:00:00   35.0
    2017-05-20 00:05:00  110.0
    2017-05-20 00:10:00  185.0
c   2017-05-20 00:00:00   40.0
    2017-05-20 00:05:00  115.0
    2017-05-20 00:10:00  190.0
    
resampled.reset_index()

  key                time  value
0   a 2017-05-20 00:00:00   30.0
1   a 2017-05-20 00:05:00  105.0
2   a 2017-05-20 00:10:00  180.0
3   b 2017-05-20 00:00:00   35.0
4   b 2017-05-20 00:05:00  110.0
5   b 2017-05-20 00:10:00  185.0
6   c 2017-05-20 00:00:00   40.0
7   c 2017-05-20 00:05:00  115.0
8   c 2017-05-20 00:10:00  190.0
```

One constraint with using `pandas.Grouper` is that the time must be the index of the Series or DataFrame.
## Moving Window Functions

These functions are useful for smoothing noisy or gappy data.

```python
close_px_all = pd.read_csv("examples/stock_px.csv",
                           parse_dates=True, index_col=0)

close_px = close_px_all[["AAPL", "MSFT", "XOM"]]

close_px = close_px.resample("B").ffill() # resampled data Business Weekly
```

the `rolling` operator, which behaves similarly to `resample` and `groupby`. It can be called on a Series or DataFrame along with a `window`

```python
close_px["AAPL"].plot()
<AxesSubplot:>

close_px["AAPL"].rolling(250).mean().plot()
```

![](assets/Pasted%20image%2020260308002053.png)

By default, rolling functions require all of the values in the window to be non-NA. This behavior can be changed to account for missing data and, in particular, the fact that you will have fewer than `window` periods of data at the beginning of the time series

```python
plt.figure()
<Figure size 1000x600 with 0 Axes>

std250 = close_px["AAPL"].pct_change().rolling(250, min_periods=10).std()

std250[5:12]

2003-01-09         NaN
2003-01-10         NaN
2003-01-13         NaN
2003-01-14         NaN
2003-01-15         NaN
2003-01-16    0.009628
2003-01-17    0.013818
Freq: B, Name: AAPL, dtype: float64

std250.plot()
```

![](assets/Pasted%20image%2020260308002231.png)

To compute an _expanding window mean_, use the `expanding` operator instead of `rolling`. The expanding mean starts the time window from the same point as the rolling window and increases the size of the window until it encompasses the whole series. An expanding window mean on the `std250` time series looks like this

```python
expanding_mean = std250.expanding().mean()
```

```python
plt.style.use('grayscale')

close_px.rolling(60).mean().plot(logy=True)
```

![](assets/Pasted%20image%2020260308002321.png)

The `rolling` function also accepts a string indicating a fixed-size time offset rolling() in moving window functions rather than a set number of periods. Using this notation can be useful for irregular time series. These are the same strings that you can pass to `resample`

```python
close_px.rolling("20D").mean()

                  AAPL       MSFT        XOM
2003-01-02    7.400000  21.110000  29.220000
2003-01-03    7.425000  21.125000  29.230000
2003-01-06    7.433333  21.256667  29.473333
2003-01-07    7.432500  21.425000  29.342500
2003-01-08    7.402000  21.402000  29.240000
...                ...        ...        ...
2011-10-10  389.351429  25.602143  72.527857
2011-10-11  388.505000  25.674286  72.835000
2011-10-12  388.531429  25.810000  73.400714
2011-10-13  388.826429  25.961429  73.905000
2011-10-14  391.038000  26.048667  74.185333
[2292 rows x 3 columns]
```
### Exponentially Weighted Functions

An alternative to using a fixed window size with equally weighted observations is to specify a constant _decay factor_ to give more weight to more recent observations. There are a couple of ways to specify the decay factor. A popular one is using a _span_, which makes the result comparable to a simple moving window function with window size equal to the span.

Since an exponentially weighted statistic places more weight on more recent observations, it “adapts” faster to changes compared with the equal-weighted version.

```python
aapl_px = close_px["AAPL"]["2006":"2007"]
ma30 = aapl_px.rolling(30, min_periods=20).mean()
ewma30 = aapl_px.ewm(span=30).mean()

aapl_px.plot(style="k-", label="Price")
# <AxesSubplot:>

ma30.plot(style="k--", label="Simple Moving Avg")
# <AxesSubplot:>

ewma30.plot(style="k-", label="EW MA")
# <AxesSubplot:>

plt.legend()

```

![](assets/Pasted%20image%2020260308002811.png)
### Binary Moving Window Functions

Some statistical operators, like correlation and covariance, need to operate on two time series. As an example, financial analysts are often interested in a stock’s correlation to a benchmark index like the S&P 500. 

```python
spx_px = close_px_all["SPX"]
spx_rets = spx_px.pct_change()
returns = close_px.pct_change()

corr = returns["AAPL"].rolling(125, min_periods=100).corr(spx_rets)

corr.plot()
```

![](assets/Pasted%20image%2020260308002657.png)

Suppose you wanted to compute the rolling correlation of the S&P 500 index with many stocks at once. You could write a loop computing this for each stock like we did for Apple above, but if each stock is a column in a single DataFrame, we can compute all of the rolling correlations in one shot by calling `rolling` on the DataFrame and passing the `spx_rets` Series.

```python
corr = returns.rolling(125, min_periods=100).corr(spx_rets)

corr.plot()
```

![](assets/Pasted%20image%2020260308002726.png)
### User-Defined Moving Window Functions

The `apply` method on `rolling` and related methods provides a way to apply an array function of your own creation over a moving window. The only requirement is that the function produce a single value (a reduction) from each piece of the array. For example, while we can compute sample quantiles using `rolling(...).quantile(q)`, we might be interested in the percentile rank of a particular value over the sample. The `scipy.stats.percentileofscore` function does just this

```python
def score_at_2percent(x):
    return percentileofscore(x, 0.02)

result = returns["AAPL"].rolling(250).apply(score_at_2percent)

result.plot()
```

![](assets/Pasted%20image%2020260308002506.png)