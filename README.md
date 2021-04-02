# cepimose

Small library to parse raw data from NIJZ's PowerBI [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTg2ODI4MGYtMTMyMi00YmUyLWExOWEtZTlmYzIxMTI2MDlmIiwidCI6ImFkMjQ1ZGFlLTQ0YTAtNGQ5NC04OTY3LTVjNjk5MGFmYTQ2MyIsImMiOjl9&pageName=ReportSectionf7478503942700dada61) displaying vaccination stats fro Slovenia

## Examples

```
import pandas as pd
import cepimose

data = cepimose.vaccinations_by_day()
df = pd.DataFrame.from_dict(data)

print(df)
```

## Dev

```
pipenv install -d
pipenv run test
```