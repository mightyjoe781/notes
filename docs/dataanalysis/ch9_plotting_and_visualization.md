# Plotting and Visualization

`matplotlib` is a desktop plotting package designed for creating plots and figures suitable for publication. The project was started by John Hunter in 2002 to enable a MATLAB-like plotting interface in Python.
## Brief matplotlib API Primer

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.arange(10)
plt.plot(data)
```

![](assets/Pasted%20image%2020260306155010.png)

### Figures and Subplots

Plots in matplotlib reside within a `Figure` object. You can create a new figure with `plt.figure`.

```python
fig = plt.figure()
# fig # should be empty
# you can pass figsize setting size and aspect size

# add subplots to empty figure
ax1 = fig.add_subplot(2, 2, 1) # 2x2 figure, 1st of these figure
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
# ax4 = fig.add_subplot(2, 2, 4) # keep commented to have empty figure

ax3.plot(np.random.standard_normal(50).cumsum(), color = "black", linestyle="dashed")
```

![](assets/Pasted%20image%2020260306155631.png)

```python

# add these 2 lines under same block
ax1.hist(np.random.standard_normal(100), bins=20, color="black", alpha=0.3)
ax2.scatter(np.arange(30), np.arange(30) + 3 * np.random.standard_normal(30))
```

NOTE: `alpha=0.3` sets transparency of the overlaid plot.

![](assets/Pasted%20image%2020260306155917.png)

```python
fig, axes = plt.subplots(2, 3)
axes
# creates 2x3 plots
# axes[0, 1] ~ refers to subplot in the top center
```

#### Adjusting Spacing around subplots

```python
subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=None)
```

`wspace` and `hspace` control the percent of the figure width and figure height, respectively, to use as spacing between subplots.

```python
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for i in range(2):
    for j in range(2):
        axes[i, j].hist(np.random.standard_normal(500), bins=50,
                        color="black", alpha=0.5)
fig.subplots_adjust(wspace=0, hspace=0)
```

![](assets/Pasted%20image%2020260306161321.png)
### Colors, Markers, and Line Styles

```python
ax.plot(x, y, linestyle="--", color="green") # dashed green line is plotted
```

```python
fig = plt.figure()
ax = fig.add_subplot()
ax.plot(np.random.standard_normal(30).cumsum(), color="black", linestyle="dashed", marker="o")
```

![](assets/Pasted%20image%2020260306164316.png)

Line plots are interpolated by default.

```python
fig = plt.figure()

ax = fig.add_subplot()

data = np.random.standard_normal(30).cumsum()

ax.plot(data, color="black", linestyle="dashed", label="Default");
ax.plot(data, color="black", linestyle="dashed",
        drawstyle="steps-post", label="steps-post");
ax.legend()
```

![](assets/Pasted%20image%2020260306164512.png)

### Tick, Labels and Legends

Most kinds of plot decorations can be accessed through methods on matplotlib axes objects. Methods `xlim`, `xticks`, `xticklabels`. 

- called with no arguments returns the current parameter values (`ax.xlim()` returns current x-axis plotting range)
- called with parameters sets the parameter value (e.g., `ax.xlim([0, 10])` sets the x-axis range to 0 to 10

#### Setting the title, axis labels, ticks and tick labels

```python
fig, ax = plt.subplots()
ax.plot(np.random.standard_normal(1000).cumsum())
```

![](assets/Pasted%20image%2020260306165034.png)

```python
ticks = ax.set_xticks([0, 250, 500, 750, 1000])
labels = ax.set_xticklabels(["one", "two", "three", "four", "five"], rotation=30, fontsize=8)
```

![](assets/Pasted%20image%2020260306165322.png)

```python
ax.set_xlabel("Stages")
ax.set_title("My first matplotlib plot")

# or 
ax.set(title="My first matplotlib plot", xlabel="Stages")
```

![](assets/Pasted%20image%2020260306165405.png)

#### Adding Legends

```python
fig, ax = plt.subplots()

ax.plot(np.random.randn(1000).cumsum(), color="black", label="one")
ax.plot(np.random.randn(1000).cumsum(), color="black", linestyle="dashed",
        label="two")
ax.plot(np.random.randn(1000).cumsum(), color="black", linestyle="dotted",
        label="three")
ax.legend() # default loc=best, 
```

![](assets/Pasted%20image%2020260306165543.png)

### Annotations and Drawing on a Subplot

```python
ax.text(x, y, "Hello world!", family="monospace", fontsize=10)
```

Example

```python
from datetime import datetime

fig, ax = plt.subplots()

data = pd.read_csv("examples/spx.csv", index_col=0, parse_dates=True)
spx = data["SPX"]

spx.plot(ax=ax, color="black")

crisis_data = [
    (datetime(2007, 10, 11), "Peak of bull market"),
    (datetime(2008, 3, 12), "Bear Stearns Fails"),
    (datetime(2008, 9, 15), "Lehman Bankruptcy")
]

for date, label in crisis_data:
    ax.annotate(label, xy=(date, spx.asof(date) + 75),
                xytext=(date, spx.asof(date) + 225),
                arrowprops=dict(facecolor="black", headwidth=4, width=2,
                                headlength=4),
                horizontalalignment="left", verticalalignment="top")

# Zoom in on 2007-2010
ax.set_xlim(["1/1/2007", "1/1/2011"])
ax.set_ylim([600, 1800])

ax.set_title("Important dates in the 2008-2009 financial crisis")
```

![](assets/Pasted%20image%2020260306185517.png)

### Saving Plots to File

```python
fig.savefig("figpath.svg")

# or
fig.savefig("figpath.png", dpi = 400)

```

### matplotlib Configuration

A lot of matplotlib Configuration default to primarily for publication usecases.

Can be customized using `rc` method on `plt`

```python
plt.rc("figure", figsize=(10, 10))

# to see all settings
plt.rcParams

# to restore all settings to default
plt.rcdefaults()
```

## Plotting with Pandas and Seaborn

`matplotlib` is a low-level tool. We assemble our base components to make a plot.

`seaborn` is a high-level statistical graphics library built-on matplotlib simplifying common visualization types.
### Line Plots

Using default `plot()` in pandas, (default is line-plots)

```python
s = pd.Series(np.random.standard_normal(10).cumsum())

s.plot()
```

![](assets/Pasted%20image%2020260306190036.png)

Generally index is passed to matplotlib for plotting on `x-axis`. to avoid this `use_index=False`.

X-axis ticks and limits can be adjusted with `xticks` and `xlim` options and the y-axis respectively with `yticks`, and `ylim`

Most of pandas plotting methods accept an optional `ax` parameter which can be a matplotlib subplot obj.

For DataFrame each column is plotted with different line.

```python
df = pd.DataFrame(np.random.standard_normal((10, 4)).cumsum(0),
                  columns=["A", "B", "C", "D"],
                  index=np.arange(0, 100, 10))

plt.style.use('grayscale')

df.plot()
```

![](assets/Pasted%20image%2020260306190645.png)

DataFrame support following methods for plotting : `subplots`, `layouts`, `sharex`, `sharey`, `legend`, `sort_columns`

### Bar Plots

```python
fig, axes = plt.subplots(2, 1)

data = pd.Series(np.random.uniform(size=16), index=list("abcdefghijklmnop"))

data.plot.bar(ax=axes[0], color="black", alpha=0.7)
data.plot.barh(ax=axes[1], color="black", alpha=0.7)
```

![](assets/Pasted%20image%2020260306190855.png)

For a DataFrame, bar plots group the values in each row in bars, side by side, for each value.

```python
df = pd.DataFrame(np.random.uniform(size=(6, 4)),
                  index=["one", "two", "three", "four", "five", "six"],
                  columns=pd.Index(["A", "B", "C", "D"], name="Genus"))

df.plot.bar()

```

![](assets/Pasted%20image%2020260306220715.png)

Another Example

```python
tips = pd.read_csv("examples/tips.csv")

# ---- tips.csv ----
   total_bill   tip smoker  day    time  size
0       16.99  1.01     No  Sun  Dinner     2
1       10.34  1.66     No  Sun  Dinner     3
2       21.01  3.50     No  Sun  Dinner     3
3       23.68  3.31     No  Sun  Dinner     2
4       24.59  3.61     No  Sun  Dinner     4

party_counts = pd.crosstab(tips["day"], tips["size"])

party_counts = party_counts.reindex(index=["Thur", "Fri", "Sat", "Sun"])

# ------
size  1   2   3   4  5  6
day                      
Thur  1  48   4   5  1  3
Fri   1  16   1   1  0  0
Sat   2  53  18  13  1  0
Sun   0  39  15  18  3  1

party_counts = party_counts.loc[:, 2:5]
party_pcts = party_counts.div(party_counts.sum(axis="columns"), axis="index")

# -----
size         2         3         4         5
day                                         
Thur  0.827586  0.068966  0.086207  0.017241
Fri   0.888889  0.055556  0.055556  0.000000
Sat   0.623529  0.211765  0.152941  0.011765
Sun   0.520000  0.200000  0.240000  0.040000

# ----- plot
party_pcts.plot.bar(stacked=True)

```

![](assets/Pasted%20image%2020260307000031.png)

```python
import seaborn as sns

tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])

tips.head()

# -----
   total_bill   tip smoker  day    time  size   tip_pct
0       16.99  1.01     No  Sun  Dinner     2  0.063204
1       10.34  1.66     No  Sun  Dinner     3  0.191244
2       21.01  3.50     No  Sun  Dinner     3  0.199886
3       23.68  3.31     No  Sun  Dinner     2  0.162494
4       24.59  3.61     No  Sun  Dinner     4  0.172069
# ------

sns.barplot(x="tip_pct", y="day", data=tips, orient="h")
```

![](assets/Pasted%20image%2020260307002228.png)

Plotting functions in seaborn take a data argument, which can be a pandas DataFrame. The other arguments refer to column names. Because there are multiple observations for each value in the day, the bars are the average value of tip_pct. The black lines drawn on the bars represent the 95% confidence interval (this can be configured through optional arguments).

### Histograms and Density Plots

```python
tips["tip_pct"].plot.hist(bins=50)
```

![](assets/Pasted%20image%2020260307002036.png)

A related plot type is a density plot, which is formed by computing an estimate of a continuous probability distribution that might have generated the observed data.

```python
tips["tip_pct"].plot.density()
```

![](assets/Pasted%20image%2020260307002103.png)

### Scatter or Point Plots

```python
macro = pd.read_csv("examples/macrodata.csv")

data = macro[["cpi", "m1", "tbilrate", "unemp"]]

trans_data = np.log(data).diff().dropna()

trans_data.tail()

## -----
          cpi        m1  tbilrate     unemp
198 -0.007904  0.045361 -0.396881  0.105361
199 -0.021979  0.066753 -2.277267  0.139762
200  0.002340  0.010286  0.606136  0.160343
201  0.008419  0.037461 -0.200671  0.127339
202  0.008894  0.012202 -0.405465  0.042560


# ------
ax = sns.regplot(x="m1", y="unemp", data=trans_data)
ax.title("Changes in log(m1) versus log(unemp)")


```

![](assets/Pasted%20image%2020260307001341.png)

Often we want to take a look at all dimensions.

```python
sns.pairplot(trans_data, diag_kind="kde", plot_kws={"alpha": 0.2})
```

![](assets/Pasted%20image%2020260307001451.png)
### Facet Grids and Categorical Data

One way to visualize data with many categorical variables is to use a facet grid, which is a two-dimensional layout of plots where the data is split across the plots on each axis based on the distinct values of a certain variable.

```python
sns.catplot(x="day", y="tip_pct", hue="time", col="smoker",
            kind="bar", data=tips[tips.tip_pct < 1])
```


![](assets/Pasted%20image%2020260307001742.png)

Instead of grouping by "time" by different bar colors within a facet, we can also expand the facet grid by adding one row per time 

```python
sns.catplot(x="day", y="tip_pct", row="time",
            col="smoker",
            kind="bar", data=tips[tips.tip_pct < 1])
```

![](assets/Pasted%20image%2020260307001841.png)

`catplot` also supports other multiple types of plots, most notably *box plots* (which show the median, quartiles, and outliers)

```python
sns.catplot(x="tip_pct", y="day", kind="box",
            data=tips[tips.tip_pct < 0.5])
```

![](assets/Pasted%20image%2020260307001945.png)