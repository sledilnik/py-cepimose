# cepimose

Small library to parse raw data from NIJZ's PowerBI [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTg2ODI4MGYtMTMyMi00YmUyLWExOWEtZTlmYzIxMTI2MDlmIiwidCI6ImFkMjQ1ZGFlLTQ0YTAtNGQ5NC04OTY3LTVjNjk5MGFmYTQ2MyIsImMiOjl9&pageName=ReportSectionf7478503942700dada61) displaying vaccination stats fro Slovenia

## Examples

```
import pandas as pd
import cepimose

data = cepimose.vaccinations_by_day()
df_by_day = pd.DataFrame.from_dict(data)

print(df_by_day)

data = cepimose.vaccinations_by_age()
df_by_age = pd.DataFrame.from_dict(data)
print(df_by_age)

```

## Dev

```
pipenv install -d
pipenv run test
```