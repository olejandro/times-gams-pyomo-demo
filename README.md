# TIMES GAMS-Pyomo Demo

This demo was originally developed for the *TIMES Migration Feasibility Study* funded by [IEA-ETSAP](https://iea-etsap.org). Final project presentation is available [here](https://www.iea-etsap.org/workshop/gothenburgh_june2018/11-TIMES-Migration_v03.pdf).

In order to test it, create a virtual environment in the root of the repository, activate it and install the dependencies (on Windows):

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -U pip
.venv\Scripts\activate
pip install -r requirements.txt
```

To execute GAMS only example run:

```
python -m gamsrun
```

To execute GAMS/PYOMO example run:

```
python -m gamspyomorun
```
