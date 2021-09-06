# cepimose

[![PyPI version](https://badge.fury.io/py/cepimose.svg)](https://pypi.org/project/cepimose)
[![Tests](https://github.com/sledilnik/py-cepimose/actions/workflows/test.yml/badge.svg)](https://github.com/sledilnik/py-cepimose/actions/workflows/test.yml)
[![Tests for Sledilnik.org](https://github.com/sledilnik/py-cepimose/actions/workflows/testSledilnik.yml/badge.svg)](https://github.com/sledilnik/py-cepimose/actions/workflows/testSledilnik.yml)

Small library to parse raw data from NIJZ's PowerBI dashboards embedded in [NIJZ stats page](https://www.nijz.si/sl/dnevno-spremljanje-okuzb-s-sars-cov-2-covid-19):
- [vaccination stats for Slovenia](https://app.powerbi.com/view?r=eyJrIjoiYWQ3NGE1NTMtZWJkMi00NzZmLWFiNDItZDc5YjU5MGRkOGMyIiwidCI6ImFkMjQ1ZGFlLTQ0YTAtNGQ5NC04OTY3LTVjNjk5MGFmYTQ2MyIsImMiOjl9)
- [latest epidemic data](https://app.powerbi.com/view?r=eyJrIjoiMDc3MDk4MmQtOGE4NS00YTRkLTgyYjktNWQzMjk5ODNlNjVhIiwidCI6ImFkMjQ1ZGFlLTQ0YTAtNGQ5NC04OTY3LTVjNjk5MGFmYTQ2MyIsImMiOjl9&pageName=ReportSection24198f7e6d06db643832) 


## Examples

Prepare environment
```
python -mvenv env
. ./env/bin/activate
pip install cepimose
```

Examples
```
import pandas as pd
import cepimose

data = cepimose.vaccinations_by_day()
df = pd.DataFrame.from_dict(data)
print(df)

data = cepimose.vaccinations_by_age()
df = pd.DataFrame.from_dict(data)
print(df)

data = cepimose.vaccines_supplied_and_used()
df = pd.DataFrame.from_dict(data)
print(df)

```

## Changelog

## 0.0.4

Added `vaccines_supplied_by_manufacturer()`

## 0.0.3

Added `vaccinations_by_region()`

## 0.0.2

Initial release

## Dev

```
git clone https://github.com/sledilnik/py-cepimose
cd py-cepimose
pipenv install -d # install dependencies (including dev)
pipenv run test # run all tests
pipenv run testForSledilnik # run just tests for sledilnik.org
pipenv shell # run virtualenv shell
pipenv run fmt # format the code (also available as VS Code task)
```
