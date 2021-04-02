# cepimose

[![PyPI version](https://badge.fury.io/py/cepimose.svg)](https://pypi.org/project/cepimose)
[![Tests](https://github.com/sledilnik/py-cepimose/actions/workflows/test.yml/badge.svg)](https://github.com/sledilnik/py-cepimose/actions/workflows/test.yml)

Small library to parse raw data from NIJZ's PowerBI [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTg2ODI4MGYtMTMyMi00YmUyLWExOWEtZTlmYzIxMTI2MDlmIiwidCI6ImFkMjQ1ZGFlLTQ0YTAtNGQ5NC04OTY3LTVjNjk5MGFmYTQ2MyIsImMiOjl9&pageName=ReportSectionf7478503942700dada61) displaying vaccination stats fro Slovenia


## Examples

Prepare environment
```
python3 -mvenv env
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

## Dev

```
pipenv install -d
pipenv run test
```