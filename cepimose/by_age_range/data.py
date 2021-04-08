import json

_source = "https://wabi-west-europe-e-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"

_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Accept": "application/json, text/plain, */*",
    "ActivityId": "a73e2035-2f0e-290b-319a-c10ebb699c77",
    "RequestId": "25da6f2b-7604-a99a-beef-8c3de4f59f67",
    "X-PowerBI-ResourceKey": "e868280f-1322-4be2-a19a-e9fc2112609f",
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
        "modelId": 159824,
        "version": "1.0.0",
        "queries": [],
    }


def _get_default_query():
    return {
        "ApplicationContext": {
            "DatasetId": "7b40529e-a50e-4dd3-8fe8-997894b4cdaa",
            "Sources": [{"ReportId": "b201281d-b2e7-4470-9f4e-0b3063794c76"}],
        },
        "CacheKey": "",
        "Query": {"Commands": []},
        "QueryId": "",
    }


def _get_default_command():
    return {
        "SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [
                    {"Name": "c1", "Entity": "Calendar", "Type": 0},
                    {"Name": "c", "Entity": "eRCO_podatki", "Type": 0},
                    {"Name": "s", "Entity": "SURS_starost", "Type": 0},
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


def _get_first_condition_values(range="'90+'", dose="1L"):
    return [
        {"Literal": {"Value": range}},
        {"Literal": {"Value": dose}},
    ]


def _create_command(range="'90+'", dose="1L"):
    values = _get_first_condition_values(range, dose)
    command = _get_default_command()
    command["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["In"][
        "Values"
    ].append(values)
    return command


def _create_req(commands, cache_key=False):
    query = _get_default_query()
    for command in commands:
        query["Query"]["Commands"].append(command)
    if cache_key:
        query["CacheKey"] = json.dumps(query["Query"]["Commands"])
    req = _get_default_req()
    req["queries"].append(query)
    return req


_doses = ["1L", "2L"]

age_ranges = [
    "'0-17'",
    "'18-24'",
    "'25-29'",
    "'30-34'",
    "'35-39'",
    "'40-44'",
    "'45-49'",
    "'50-54'",
    "'55-59'",
    "'60-64'",
    "'65-69'",
    "'70-74'",
    "'75-79'",
    "'80-84'",
    "'85-90'",
    "'90+'",
]


def _create_range_commands():
    obj = {}
    for el in age_ranges:
        dose1_command = _create_command(el, "1L")
        dose2_command = _create_command(el, "2L")
        obj[el] = [dose1_command, dose2_command]

    return obj


def _create_range_requests():
    commands = _create_range_commands()
    key_value = commands.items()
    obj = {}
    for el in key_value:
        key = el[0]
        _commands = el[1]
        range_requests = []
        dose1_req = _create_req([_commands[0]])
        dose2_req = _create_req([_commands[1]])
        obj[key] = [dose1_req, dose2_req]

    return obj


_vaccination_range_requests = _create_range_requests()

_vaccinations_by_age_90_dose1_command = _create_command("'90+'", "1L")
_vaccinations_by_age_90_dose2_command = _create_command("'90+'", "2L")

_vaccinations_by_age_range_90_dose1_req = _create_req(
    [_vaccinations_by_age_90_dose1_command]
)
_vaccinations_by_age_range_90_dose2_req = _create_req(
    [_vaccinations_by_age_90_dose2_command]
)


# not sure what data from this query represents
_vaccinations_by_region_by_age_90_dose1_command = [
    {
        "SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [
                    {"Name": "e", "Entity": "eRCO_podatki", "Type": 0},
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
                            {"Name": "s", "Entity": "SURS_starost", "Type": 0},
                            {"Name": "e", "Entity": "eRCO_podatki", "Type": 0},
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
                                                        "SourceRef": {"Source": "e"}
                                                    },
                                                    "Property": "Odmerek",
                                                }
                                            },
                                        ],
                                        "Values": [
                                            [
                                                {"Literal": {"Value": "'90+'"}},
                                                {"Literal": {"Value": "1L"}},
                                            ]
                                        ],
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
]
