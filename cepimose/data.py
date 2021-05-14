import json
from .enums import Region, AgeGroup, Manufacturer

_source = "https://wabi-west-europe-e-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

_models = {
    "ver1": {
        "headers": {
            "X-PowerBI-ResourceKey": "e868280f-1322-4be2-a19a-e9fc2112609f",
        },
        "modelId": 159824,
        "ApplicationContext": {
            "DatasetId": "7b40529e-a50e-4dd3-8fe8-997894b4cdaa",
            "Sources": [{"ReportId": "b201281d-b2e7-4470-9f4e-0b3063794c76"}],
        },
    },
    "ver2": {
        "headers": {
            "X-PowerBI-ResourceKey": "ad74a553-ebd2-476f-ab42-d79b590dd8c2",
        },
        "modelId": 175575,
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [{"ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee"}],
        },
    },
    "ver3": {
        "headers": {
            "X-PowerBI-ResourceKey": "ad74a553-ebd2-476f-ab42-d79b590dd8c2",
        },
        "modelId": 175575,
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "022fd838583336ee7f55",
                }
            ],
        },
    },
}


def _get_model_version(ver):
    x_power_bi_resource_key = _models[ver]["headers"]["X-PowerBI-ResourceKey"]
    model_id = _models[ver]["modelId"]
    application_context = _models[ver]["ApplicationContext"]
    return {
        "X-PowerBI-ResourceKey": x_power_bi_resource_key,
        "modelId": model_id,
        "ApplicationContext": application_context,
    }


_model_ver = _get_model_version("ver3")

_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Accept": "application/json, text/plain, */*",
    "X-PowerBI-ResourceKey": _model_ver["X-PowerBI-ResourceKey"],
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://app.powerbi.com",
    "Connection": "keep-alive",
    "Referer": "https://app.powerbi.com/",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}


def _get_default_req():
    return {
        "cancelQueries": [],
        "modelId": _model_ver["modelId"],
        "version": "1.0.0",
        "queries": [],
    }


def _get_default_query():
    return {
        "ApplicationContext": _model_ver["ApplicationContext"],
        "CacheKey": "",
        "Query": {"Commands": []},
        "QueryId": "",
    }


def _create_req(commands, cache_key=False):
    query = _get_default_query()
    for command in commands:
        query["Query"]["Commands"].append(command)
    if cache_key:
        query["CacheKey"] = json.dumps(query["Query"]["Commands"])
    req = _get_default_req()
    req["queries"].append(query)
    return req


# AGE RANGE (AGE GROUP)
def _get_default_by_age_group_command():
    return {
        "SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [
                    {"Name": "c1", "Entity": "Calendar", "Type": 0},
                    {"Name": "c", "Entity": "eRCO_podatki_ed", "Type": 0},
                    {"Name": "s", "Entity": "xls_SURS_starost", "Type": 0},
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c1"}},
                            "Property": "Date",
                        },
                        "Name": "Calendar.Date",
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": "Weight running total in Date",
                        },
                        "Name": "eRCO_podatki.Weight running total in Date",
                    },
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": "Odmerek",
                        },
                        "Name": "eRCO_podatki.Odmerek",
                    },
                ],
                "Where": [
                    {
                        "Condition": {
                            "In": {
                                "Expressions": [
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "s"}
                                            },
                                            "Property": "Starostni razred",
                                        }
                                    },
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "c"}
                                            },
                                            "Property": "Odmerek",
                                        }
                                    },
                                ],
                                "Values": [],
                            }
                        }
                    },
                    {
                        "Condition": {
                            "Not": {
                                "Expression": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "CepivoIme",
                                                }
                                            }
                                        ],
                                        "Values": [[{"Literal": {"Value": "null"}}]],
                                    }
                                }
                            }
                        }
                    },
                    {
                        "Condition": {
                            "Comparison": {
                                "ComparisonKind": 1,
                                "Left": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "c1"}},
                                        "Property": "Date",
                                    }
                                },
                                "Right": {
                                    "DateSpan": {
                                        "Expression": {
                                            "Literal": {
                                                "Value": "datetime'2020-12-26T01:00:00'"
                                            }
                                        },
                                        "TimeUnit": 5,
                                    }
                                },
                            }
                        }
                    },
                ],
            },
            "Binding": {
                "Primary": {"Groupings": [{"Projections": [0, 1]}]},
                "Secondary": {"Groupings": [{"Projections": [2]}]},
                "DataReduction": {
                    "DataVolume": 4,
                    "Intersection": {"BinnedLineSample": {}},
                },
                "Version": 1,
            },
            "ExecutionMetricsKind": 1,
        }
    }


def _get_by_age_group_first_condition_values(group="'90+'", dose="1L"):
    return [
        {"Literal": {"Value": group}},
        {"Literal": {"Value": dose}},
    ]


def _create_by_age_group_command(group="'90+'", dose="1L"):
    values = _get_by_age_group_first_condition_values(group, dose)
    command = _get_default_by_age_group_command()
    command["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["In"][
        "Values"
    ].append(values)
    return command


def _create_by_age_group_commands():
    obj = {}
    for el in AgeGroup:
        dose1_command = _create_by_age_group_command(el.value, "1L")
        dose2_command = _create_by_age_group_command(el.value, "2L")
        obj[el] = [dose1_command, dose2_command]

    return obj


def _create_by_age_group_requests():
    commands = _create_by_age_group_commands()
    key_value = commands.items()
    obj = {}
    for el in key_value:
        key = el[0]
        _commands = el[1]
        group_requests = []
        dose1_req = _create_req([_commands[0]])
        dose2_req = _create_req([_commands[1]])
        obj[key] = [dose1_req, dose2_req]

    return obj


# BY REGION BY DAY
def _get_default_by_region_by_day_command():
    return {
        "SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [
                    {"Name": "c1", "Entity": "Calendar", "Type": 0},
                    {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
                    {"Name": "s", "Entity": "Sifrant_regija", "Type": 0},
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c1"}},
                            "Property": "Date",
                        },
                        "Name": "Calendar.Date",
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": "Weight running total in Date",
                        },
                        "Name": "eRCO_podatki.Weight running total in Date",
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": "Tekoča vsota za mero Precepljenost v polju Date",
                        },
                        "Name": "eRCO_podatki_ed.Tekoča vsota za mero Precepljenost v polju Date",
                    },
                ],
                "Where": [
                    {
                        "Condition": {
                            "In": {
                                "Expressions": [
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "s"}
                                            },
                                            "Property": "Regija",
                                        }
                                    }
                                ],
                                "Values": [],
                            }
                        }
                    },
                    {
                        "Condition": {
                            "Comparison": {
                                "ComparisonKind": 1,
                                "Left": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "c1"}},
                                        "Property": "Date",
                                    }
                                },
                                "Right": {
                                    "DateSpan": {
                                        "Expression": {
                                            "Literal": {
                                                "Value": "datetime'2020-12-26T01:00:00'"
                                            }
                                        },
                                        "TimeUnit": 5,
                                    }
                                },
                            }
                        }
                    },
                ],
            },
            "Binding": {
                "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
                "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
                "Version": 1,
            },
            "ExecutionMetricsKind": 1,
        }
    }


def _get_default_by_region_by_day_condition_values(region):
    return [{"Literal": {"Value": region}}]


def _create_by_region_by_day_command(region):
    values = _get_default_by_region_by_day_condition_values(region)
    command = _get_default_by_region_by_day_command()
    command["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["In"][
        "Values"
    ].append(values)
    return command


def _create_by_region_by_day_commands():
    obj = {}
    for el in Region:
        doses_command = _create_by_region_by_day_command(el.value)
        obj[el] = [doses_command]

    return obj


def _create_by_region_by_day_requests():
    commands = _create_by_region_by_day_commands()
    key_value = commands.items()
    obj = {}
    for el in key_value:
        key = el[0]
        _commands = el[1]
        group_requests = []
        doses_req = _create_req([_commands[0]])
        obj[key] = [doses_req]

    return obj


# AGE GROUP BY REGION ON DAY
def _get_age_group_by_region_on_day_first_condition_value(group="'90+'"):
    return [{"Literal": {"Value": group}}]


def _get_default_age_group_by_region_on_day_command():
    return {
        "SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [
                    {"Name": "e", "Entity": "eRCO_podatki_ed", "Type": 0},
                    {"Name": "s1", "Entity": "Sifrant_regija", "Type": 0},
                    {"Name": "c", "Entity": "Calendar", "Type": 0},
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "s1"}},
                            "Property": "Regija",
                        },
                        "Name": "Sifrant_regija.Regija",
                    },
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "Odmerek",
                        },
                        "Name": "eRCO_podatki.Odmerek",
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "Delež_regija",
                        },
                        "Name": "eRCO_podatki.Delež_regija",
                    },
                    {
                        "Aggregation": {
                            "Expression": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "e"}},
                                    "Property": "Weight",
                                }
                            },
                            "Function": 0,
                        },
                        "Name": "Sum(eRCO_podatki.Weight)",
                    },
                ],
                "Where": [
                    {
                        "Condition": {
                            "Not": {
                                "Expression": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "e"}
                                                    },
                                                    "Property": "CepivoIme",
                                                }
                                            }
                                        ],
                                        "Values": [[{"Literal": {"Value": "null"}}]],
                                    }
                                }
                            }
                        }
                    },
                    {
                        "Condition": {
                            "Not": {
                                "Expression": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "s1"}
                                                    },
                                                    "Property": "Regija",
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [{"Literal": {"Value": "null"}}],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Celotna Slovenija'"
                                                    }
                                                }
                                            ],
                                            [{"Literal": {"Value": "'TUJINA'"}}],
                                        ],
                                    }
                                }
                            }
                        }
                    },
                    {
                        "Condition": {
                            "Comparison": {
                                "ComparisonKind": 1,
                                "Left": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "c"}},
                                        "Property": "Date",
                                    }
                                },
                                "Right": {
                                    "DateSpan": {
                                        "Expression": {
                                            "Literal": {
                                                "Value": "datetime'2020-12-26T01:00:00'"
                                            }
                                        },
                                        "TimeUnit": 5,
                                    }
                                },
                            }
                        }
                    },
                ],
                "OrderBy": [
                    {
                        "Direction": 2,
                        "Expression": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "Delež_regija",
                            }
                        },
                    }
                ],
            },
            "Binding": {
                "Primary": {"Groupings": [{"Projections": [0, 2, 3]}]},
                "Secondary": {"Groupings": [{"Projections": [1]}]},
                "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {"Window": {"Count": 200}},
                    "Secondary": {"Top": {"Count": 60}},
                },
                "SuppressedJoinPredicates": [3],
                "Version": 1,
                "Highlights": [
                    {
                        "Version": 2,
                        "From": [
                            {"Name": "x", "Entity": "xls_SURS_starost", "Type": 0},
                            {"Name": "e", "Entity": "eRCO_podatki_ed", "Type": 0},
                        ],
                        "Where": [
                            {
                                "Condition": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "x"}
                                                    },
                                                    "Property": "Starostni razred",
                                                }
                                            }
                                        ],
                                        "Values": [],
                                    }
                                }
                            },
                            {
                                "Condition": {
                                    "Not": {
                                        "Expression": {
                                            "In": {
                                                "Expressions": [
                                                    {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "e"
                                                                }
                                                            },
                                                            "Property": "CepivoIme",
                                                        }
                                                    }
                                                ],
                                                "Values": [
                                                    [{"Literal": {"Value": "null"}}]
                                                ],
                                            }
                                        }
                                    }
                                }
                            },
                        ],
                    }
                ],
            },
            "ExecutionMetricsKind": 1,
        }
    }


def _create_age_group_by_region_on_day_command(group="'90+'"):
    values = _get_age_group_by_region_on_day_first_condition_value(group)
    command = _get_default_age_group_by_region_on_day_command()
    command["SemanticQueryDataShapeCommand"]["Binding"]["Highlights"][0]["Where"][0][
        "Condition"
    ]["In"]["Values"].append(values)
    return command


def _create_age_group_by_region_on_day_commands():
    obj = {}
    for el in AgeGroup:
        command = _create_age_group_by_region_on_day_command(el.value)
        obj[el] = [command]

    return obj


def _create_age_group_by_region_on_day_requests():
    commands = _create_age_group_by_region_on_day_commands()
    key_value = commands.items()
    obj = {}
    for el in key_value:
        key = el[0]
        _commands = el[1]
        req = _create_req([_commands[0]])
        obj[key] = [req]

    return obj


# BY MANU USED


def _get_vaccination_by_manufacturer_used_second_condition_value(group):
    return [{"Literal": {"Value": group}}]


def _get_default_vaccination_by_manufacturer_used_command():
    return {
        "SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [
                    {"Name": "c1", "Entity": "Calendar", "Type": 0},
                    {"Name": "c", "Entity": "eRCO_podatki_ed", "Type": 0},
                    {"Name": "x", "Entity": "xls_NIJZ_Odmerki", "Type": 0},
                    {"Name": "s", "Entity": "Sifrant_Cepivo", "Type": 0},
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c1"}},
                            "Property": "Date",
                        },
                        "Name": "Calendar.Date",
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": "Kumulativno skupaj cepljenih",
                        },
                        "Name": "eRCO_podatki.Kumulativno skupaj cepljenih",
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "x"}},
                            "Property": "Tekoča vsota za mero odmerki* v polju Date",
                        },
                        "Name": "xls_NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date",
                    },
                ],
                "Where": [
                    {
                        "Condition": {
                            "Comparison": {
                                "ComparisonKind": 2,
                                "Left": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "c1"}},
                                        "Property": "Date",
                                    }
                                },
                                "Right": {
                                    "DateSpan": {
                                        "Expression": {
                                            "Literal": {
                                                "Value": "datetime'2020-12-26T00:00:00'"
                                            }
                                        },
                                        "TimeUnit": 5,
                                    }
                                },
                            }
                        }
                    },
                    {
                        "Condition": {
                            "In": {
                                "Expressions": [
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "s"}
                                            },
                                            "Property": "Cepivo_Ime",
                                        }
                                    }
                                ],
                                "Values": [],
                            }
                        }
                    },
                ],
            },
            "Binding": {
                "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
                "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
                "Version": 1,
            },
            "ExecutionMetricsKind": 1,
        }
    }


def _create_vaccination_by_manufacturer_used_command(group):
    values = _get_vaccination_by_manufacturer_used_second_condition_value(group)
    command = _get_default_vaccination_by_manufacturer_used_command()
    command["SemanticQueryDataShapeCommand"]["Query"]["Where"][1]["Condition"]["In"][
        "Values"
    ].append(values)
    return command


def _create_vaccination_by_manufacturer_used_commands():
    obj = {}
    for el in Manufacturer:
        command = _create_vaccination_by_manufacturer_used_command(el.value)
        obj[el] = [command]

    return obj


def _create_vaccination_by_manufacturer_used_requests():
    commands = _create_vaccination_by_manufacturer_used_commands()
    key_value = commands.items()
    obj = {}
    for el in key_value:
        key = el[0]
        _commands = el[1]
        req = _create_req([_commands[0]])
        obj[key] = [req]

    return obj


# COMMANDS
_vaccinations_timestamp_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "e", "Entity": "eRCO_podatki_ed", "Type": 0},
                {"Name": "c", "Entity": "Calendar", "Type": 0},
            ],
            "Select": [
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "DatumOsvezevanja",
                            }
                        },
                        "Function": 3,
                    },
                    "Name": "Min(eRCO_podatki.DatumOsvezevanja)",
                }
            ],
            "Where": [
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 1,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T01:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0]}]},
            "DataReduction": {"DataVolume": 3, "Primary": {"Top": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccinations_by_day_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "c1", "Entity": "Calendar", "Type": 0},
                {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c1"}},
                        "Property": "Date",
                    },
                    "Name": "Calendar.Date",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "c"}},
                        "Property": "Weight running total in Date",
                    },
                    "Name": "eRCO_podatki.Weight running total in Date",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "c"}},
                        "Property": "Tekoča vsota za mero Precepljenost v polju Date",
                    },
                    "Name": "eRCO_podatki_ed.Tekoča vsota za mero Precepljenost v polju Date",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 1,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c1"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T01:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
            "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccinations_by_age_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "s", "Entity": "xls_SURS_starost", "Type": 0},
                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                {"Name": "c", "Entity": "Calendar", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Starostni ​razred",
                    },
                    "Name": "SURS_starost.Starostni razred",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Delež_starost_precepljenost",
                    },
                    "Name": "eRCO_podatki_ed.Delež_starost_precepljenost",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Delež_starost_1",
                    },
                    "Name": "eRCO_podatki_ed.Delež_starost",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "Odmerek – kopija",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(eRCO_​​podatki.Odmerek – kopija)",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "Precepljenost",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(eRCO_​​podatki.Precepljenost)",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
                                                "Property": "CepivoIme",
                                            }
                                        }
                                    ],
                                    "Values": [[{"Literal": {"Value": "null"}}]],
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 1,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T01:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                },
            ],
            "OrderBy": [
                {
                    "Direction": 1,
                    "Expression": {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "s"}},
                            "Property": "Starostni ​razred",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2, 3, 4]}]},
            "DataReduction": {"DataVolume": 4, "Primary": {"Window": {"Count": 1000}}},
            "SuppressedJoinPredicates": [3, 4],
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccinations_supplied_and_used_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "c1", "Entity": "Calendar", "Type": 0},
                {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
                {"Name": "n", "Entity": "xls_NIJZ_Odmerki", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c1"}},
                        "Property": "Date",
                    },
                    "Name": "Calendar.Date",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "c"}},
                        "Property": "Kumulativno skupaj cepljenih",
                    },
                    "Name": "eRCO_podatki.Kumulativno skupaj cepljenih",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "n"}},
                        "Property": "Tekoča vsota za mero odmerki*​ v polju Date",
                    },
                    "Name": "NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c1"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T00:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
            "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccination_by_region_command = {
    "SemanticQueryDataShapeCommand": {
        "Binding": {
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Window": {"Count": 200}},
                "Secondary": {"Top": {"Count": 60}},
            },
            "Primary": {"Groupings": [{"Projections": [0, 2, 3]}]},
            "Secondary": {"Groupings": [{"Projections": [1]}]},
            "SuppressedJoinPredicates": [3],
            "Version": 1,
        },
        "Query": {
            "From": [
                {"Entity": "eRCO_podatki_ed", "Name": "e", "Type": 0},
                {
                    "Entity": "Sifrant_regija",
                    "Name": "s1",
                    "Type": 0,
                },
                {"Entity": "Calendar", "Name": "c", "Type": 0},
            ],
            "OrderBy": [
                {
                    "Direction": 2,
                    "Expression": {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "Delež_regija",
                        }
                    },
                }
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s1"}},
                        "Property": "Regija",
                    },
                    "Name": "Sifrant_regija.Regija",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Odmerek",
                    },
                    "Name": "eRCO_podatki.Odmerek",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Delež_regija",
                    },
                    "Name": "eRCO_podatki.Delež_regija",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "Weight",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(eRCO_podatki.Weight)",
                },
            ],
            "Version": 2,
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
                                                "Property": "CepivoIme",
                                            }
                                        }
                                    ],
                                    "Values": [[{"Literal": {"Value": "null"}}]],
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "s1"}
                                                },
                                                "Property": "Regija",
                                            }
                                        }
                                    ],
                                    "Values": [
                                        [{"Literal": {"Value": "null"}}],
                                        [{"Literal": {"Value": "'Celotna Slovenija'"}}],
                                        [{"Literal": {"Value": "'TUJINA'"}}],
                                    ],
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 1,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T01:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                },
            ],
        },
    }
}

_vaccination_supplied_by_manufacturer_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "c", "Entity": "Calendar", "Type": 0},
                {"Name": "n", "Entity": "xls_NIJZ_Odmerki", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c"}},
                        "Property": "Date",
                    },
                    "Name": "Calendar.Date",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "n"}},
                        "Property": "Vrsta cepiva",
                    },
                    "Name": "NIJZ_Odmerki.Vrsta cepiva",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "n"}},
                                "Property": "odmerki*",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(NIJZ_Odmerki.odmerki*)",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "n"}
                                                },
                                                "Property": "Vrsta cepiva",
                                            }
                                        }
                                    ],
                                    "Values": [
                                        [{"Literal": {"Value": "null"}}],
                                        [{"Literal": {"Value": "'Skupaj'"}}],
                                    ],
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "c"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "null"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 1,
                            "Left": {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "n"}
                                            },
                                            "Property": "odmerki*",
                                        }
                                    },
                                    "Function": 0,
                                }
                            },
                            "Right": {"Literal": {"Value": "1L"}},
                        }
                    },
                    "Target": [
                        {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "c"}},
                                "Property": "Date",
                            }
                        },
                        {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "n"}},
                                "Property": "Vrsta cepiva",
                            }
                        },
                    ],
                },
            ],
            "OrderBy": [
                {
                    "Direction": 1,
                    "Expression": {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": "Date",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2], "Subtotal": 1}]},
            "DataReduction": {"DataVolume": 3, "Primary": {"Window": {"Count": 500}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccination_supplied_by_manufacturer_cum_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "c1", "Entity": "Calendar", "Type": 0},
                {"Name": "n", "Entity": "xls_NIJZ_Odmerki", "Type": 0},
                {"Name": "s", "Entity": "Sifrant_Cepivo", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c1"}},
                        "Property": "Date",
                    },
                    "Name": "Calendar.Date",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "n"}},
                        "Property": "Tekoča vsota za mero odmerki* v polju Date",
                    },
                    "Name": "NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Cepivo_Ime",
                    },
                    "Name": "Sifrant_Cepivo.Cepivo_Ime",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c1"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-20T00:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                },
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "n"}
                                                },
                                                "Property": "Vrsta cepiva",
                                            }
                                        }
                                    ],
                                    "Values": [
                                        [{"Literal": {"Value": "'Skupaj'"}}],
                                        [{"Literal": {"Value": "null"}}],
                                    ],
                                }
                            }
                        }
                    }
                },
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1]}]},
            "Secondary": {"Groupings": [{"Projections": [2]}]},
            "DataReduction": {
                "DataVolume": 4,
                "Intersection": {"BinnedLineSample": {}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccinations_by_municipalities_share_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "e", "Entity": "eRCO_podatki_občine", "Type": 0},
                {"Name": "s", "Entity": "xls_SURS_obcine", "Type": 0},
                {"Name": "c", "Entity": "Calendar", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Obcina",
                    },
                    "Name": "SURS_obcine.Obcina",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "s"}},
                                "Property": "PopulacijaObcina",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "CountNonNull(SURS_obcine.PopulacijaObcina)",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Odst_CelotnaSLO_P",
                    },
                    "Name": "eRCO_podatki_obcine_pop.Odst_CelotnaSLO_P",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Odst_CelotnaSLO_C",
                    },
                    "Name": "eRCO_podatki_obcine_pop.Odst_CelotnaSLO_C",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "Cepljeni​",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(eRCO_podatki_občine.Cepljeni​)",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "e"}},
                                "Property": "Polno ﻿Cepljeni",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(eRCO_podatki_občine.PolnöCepljeni)",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "s"}
                                                },
                                                "Property": "Obcina",
                                            }
                                        }
                                    ],
                                    "Values": [[{"Literal": {"Value": "null"}}]],
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 1,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T01:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                },
            ],
            "OrderBy": [
                {
                    "Direction": 2,
                    "Expression": {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "Odst_CelotnaSLO_P",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2, 3, 4, 5]}]},
            "DataReduction": {"DataVolume": 4, "Primary": {"Top": {}}},
            "Aggregates": [{"Select": 2, "Aggregations": [{"Min": {}}, {"Max": {}}]}],
            "SuppressedJoinPredicates": [1, 3, 4, 5],
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

_vaccinations_by_manufacturer_used_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "c1", "Entity": "Calendar", "Type": 0},
                {"Name": "s", "Entity": "Sifrant_Cepivo", "Type": 0},
                {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c1"}},
                        "Property": "Date",
                    },
                    "Name": "Calendar.Date",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Cepivo_Ime",
                    },
                    "Name": "Sifrant_Cepivo.Cepivo_Ime",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "c"}},
                                "Property": "Weight",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(eRCO_podatki_ed.Weight)",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c1"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2020-12-26T00:00:00'"
                                        }
                                    },
                                    "TimeUnit": 5,
                                }
                            },
                        }
                    }
                },
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "In": {
                                    "Expressions": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "s"}
                                                },
                                                "Property": "Cepivo_Ime",
                                            }
                                        }
                                    ],
                                    "Values": [[{"Literal": {"Value": "null"}}]],
                                }
                            }
                        }
                    }
                },
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 2]}]},
            "Secondary": {"Groupings": [{"Projections": [1]}]},
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Sample": {}},
                "Secondary": {"Top": {}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}


# REQ
_vaccinations_timestamp_req = _create_req([_vaccinations_timestamp_command])

_vaccinations_by_day_req = _create_req([_vaccinations_by_day_command])

_vaccinations_by_age_req = _create_req([_vaccinations_by_age_command])

_vaccines_supplied_and_used_req = _create_req([_vaccinations_supplied_and_used_command])

_vaccinations_by_region_req = _create_req([_vaccination_by_region_command], True)

_vaccines_supplied_by_manufacturer_req = _create_req(
    [_vaccination_supplied_by_manufacturer_command]
)

_vaccines_supplied_by_manufacturer_cum_req = _create_req(
    [_vaccination_supplied_by_manufacturer_cum_command]
)

_vaccination_by_age_group_requests = _create_by_age_group_requests()

_vaccinations_by_region_by_day_requests = _create_by_region_by_day_requests()

_vaccinations_municipalities_share_req = _create_req(
    [_vaccinations_by_municipalities_share_command], True
)

_vaccinations_age_group_by_region_on_day_requests = (
    _create_age_group_by_region_on_day_requests()
)

_vaccination_by_manufacturer_supplied_used_requests = (
    _create_vaccination_by_manufacturer_used_requests()
)

_vaccinations_by_manufacturer_used_req = _create_req(
    [_vaccinations_by_manufacturer_used_command]
)
