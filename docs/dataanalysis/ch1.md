### What is this Book About ?

This is a book about the parts of the Python language and libraries you’ll need to effectively solve a broad set of data analysis problems. This book is not an exposition on analytical methods using Python as the implementation language.

### Why python for Data Analysis ?

- Most popular dynamic language along with Perl, Ruby and others.
- Large and active scientific community.
- Adoption of language in research and industry has increased significantly.
- Improved library support (primarly pandas) has made it strong for data manipulation tasks.

#### Python as a Glue

Part of python’s success as a scientific computing platform is the ease of integrating C, C++ and FORTRAN code.

See [Cython](http://cython.org) project.

#### Solving the “Two-Language Problem”

Usually in many organizations, it is common to research, prototype, and test new ideas on a domain-specific computing language like MATLAB, or R then port these ideas to be part of larger production systems written in Java, C# or C++.

Python effectively servers both the purposes of research and prototying but also building the production systems.

#### Why not Python ?

As python is interpreted language, in general most Python code will run substantially slower than code written in a compiled language like Java or C++. As *programmer time* is more valuable than *CPU Time*, many are happy to make this tradeoff. Application those require very low latency ( for example high frequency trading ), C++ is more preffered.

Python is not ideal for highly concurrent, multithreaded application, particularly application with many CPU-boun threads. The reason for this is global interpreter lock (GIL), a mechanism to prevent interpreter from executing more than one python bytecode instruction at a time.

Note : Cython project features easy integration with OpenMP, a C framework for parallel computing, in order to do parallelize loops and thus significantly speed up numerical algorithms.

### Essential Python Libraries

#### NumPy

foundational package for scientific computing in Python.

- a fast and effiecient multidimensional array object *ndarray*
- function for performing element-wise computation with arrays or mathematical operations between arrays
- tools for reading and writing array-based data sets to disk
- linear algebra, fourier transform and random number generation
- tools for integrating connecting C, C++ and Fortran code to python

Beyond array processing capabilities it acts as primary container for data to be passed between algorithm for the purpose of data analysis.

#### pandas

pandas provide rich data structures and functions designed to make working with structured data fast, easy, and expressive. It is, as you will see, one of the critical ingridients enabling Python to be a powerful and productive data analysis environment.

Primary object in pandas that will be used in this book is the `DataFrame`, a two dimensional tabular, column-oriented data structure with both row and column labels: Basically pandas combine high performance array-computing features of NumPy with flexible data manipulation capabilities of spreadsheets and relation databases.

For financial users, pandas features rich, high-performance time series functionality and tools well-suited for working with financial data. Infact it was designed to be an ideal toll for financial data analysis applications.

#### matplotlib

matplotlib is the most popular Python library for producing plots and other 2D data visulizations. It was originally created by John D Hunter and is now maintained by large team of developers. It is well-suited for creating plots suitable for publication.

#### IPython

Ipython is the component in standard scientific Python toolset that ties everything together. It provides a robust and productive environment for interactive and exploratory computing. It is enhanced python shell. It is primarly used for running, debuging and testing code.

-  A Mathematica-like HTML notebook for connecting to IPython through a web browser (more on this later).
- A Qt framework-based GUI console with inline plotting, multiline editing, and syntax highlighting
- An infrastructure for interactive parallel and distributed computing

#### SciPy

Collection of packages addressing a number of different standard problem domain in scientific computing.

`scipy.integrate` : numerical integration routines and differential equation solvers.

`scipy.linalg` : linear algebra routines and matrix decompositions extending beyond those provided in `numpy.linalg`

`scipy.optimize` : functions optimizers and root finding algorithms

`scipy.signal` : signal processing tools

`scipy.sparse`: sparse matrices and sparse linear system solvers

`scipy.special` : wrapper around SPECFUN, a Fortran library implementing many common mathematical functions, such as gamma function

`scipy.stats` : standard continuous and discrete probability distributions ( density functions, samplers, continuous distribution functions), variable statistical tests, and more descriptive statistics.

`scipy.weave` : tools for using inline C++ code to accelerate array computations.

#### Setup for MacOS



