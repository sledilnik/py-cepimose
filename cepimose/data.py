import json

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


_model_ver = _get_model_version("ver2")

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


def _get_default_by_age_range_command():
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


def _get_by_age_range_first_condition_values(range="'90+'", dose="1L"):
    return [
        {"Literal": {"Value": range}},
        {"Literal": {"Value": dose}},
    ]


def _create_by_age_range_command(range="'90+'", dose="1L"):
    values = _get_by_age_range_first_condition_values(range, dose)
    command = _get_default_by_age_range_command()
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


def _create_by_age_range_commands():
    obj = {}
    for el in age_ranges:
        dose1_command = _create_by_age_range_command(el, "1L")
        dose2_command = _create_by_age_range_command(el, "2L")
        key = el.replace("'", "")
        obj[key] = [dose1_command, dose2_command]

    return obj


def _create_by_age_range_requests():
    commands = _create_by_age_range_commands()
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


# COMMANDS
_vaccinations_by_day_command = {
    "SemanticQueryDataShapeCommand": {
        "Binding": {
            "DataReduction": {
                "DataVolume": 4,
                "Intersection": {"BinnedLineSample": {}},
            },
            "Primary": {"Groupings": [{"Projections": [0, 1]}]},
            "Secondary": {"Groupings": [{"Projections": [2]}]},
            "Version": 1,
        },
        "Query": {
            "From": [
                {"Entity": "Calendar", "Name": "c1", "Type": 0},
                {"Entity": "eRCO_podatki", "Name": "c", "Type": 0},
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
            "Version": 2,
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
    }
}

_vaccinations_by_age_command = {
    "SemanticQueryDataShapeCommand": {
        "Binding": {
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Window": {"Count": 200}},
                "Secondary": {"Top": {"Count": 60}},
            },
            "Primary": {"Groupings": [{"Projections": [0, 1, 3]}]},
            "Secondary": {"Groupings": [{"Projections": [2]}]},
            "SuppressedJoinPredicates": [3],
            "Version": 1,
        },
        "Query": {
            "From": [
                {"Entity": "eRCO_podatki", "Name": "e", "Type": 0},
                {"Entity": "SURS_starost", "Name": "s", "Type": 0},
                {"Entity": "Calendar", "Name": "c", "Type": 0},
            ],
            "OrderBy": [
                {
                    "Direction": 1,
                    "Expression": {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "s"}},
                            "Property": "Starostni razred",
                        }
                    },
                }
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Starostni razred",
                    },
                    "Name": "SURS_starost.Starostni razred",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Delež_starost",
                    },
                    "Name": "eRCO_podatki.Delež_starost",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Odmerek",
                    },
                    "Name": "eRCO_podatki.Odmerek",
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

_vaccinations_supplied_and_used_command = {
    "SemanticQueryDataShapeCommand": {
        "Binding": {
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"BinnedLineSample": {}},
            },
            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
            "Version": 1,
        },
        "Query": {
            "From": [
                {"Entity": "Calendar", "Name": "c1", "Type": 0},
                {"Entity": "eRCO_podatki", "Name": "c", "Type": 0},
                {"Entity": "NIJZ_Odmerki", "Name": "n", "Type": 0},
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
                        "Property": "Tekoča vsota za mero odmerki* v polju Date",
                    },
                    "Name": "NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date",
                },
            ],
            "Version": 2,
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
                {"Entity": "eRCO_podatki", "Name": "e", "Type": 0},
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
        "Binding": {
            "DataReduction": {
                "DataVolume": 3,
                "Primary": {"Window": {"Count": 500}},
            },
            "Primary": {"Groupings": [{"Projections": [0, 1, 2], "Subtotal": 1}]},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
        "Query": {
            "From": [
                {"Entity": "Calendar", "Name": "c", "Type": 0},
                {"Entity": "NIJZ_Odmerki", "Name": "n", "Type": 0},
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
        },
    }
}

_vaccination_supplied_by_manufacturer_cum_command = {
    "SemanticQueryDataShapeCommand": {
        "Binding": {
            "DataReduction": {
                "DataVolume": 4,
                "Intersection": {"BinnedLineSample": {}},
            },
            "Primary": {"Groupings": [{"Projections": [0, 2]}]},
            "Secondary": {"Groupings": [{"Projections": [1]}]},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
        "Query": {
            "From": [
                {"Entity": "Calendar", "Name": "c1", "Type": 0},
                {
                    "Entity": "Vezno_Vrsta_cepiva",
                    "Name": "v",
                    "Type": 0,
                },
                {"Entity": "NIJZ_Odmerki", "Name": "n", "Type": 0},
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
                        "Expression": {"SourceRef": {"Source": "v"}},
                        "Property": "Vrsta_cepiva",
                    },
                    "Name": "Vezno_Vrsta_cepiva.Vrsta_cepiva",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "n"}},
                        "Property": "Tekoča vsota za mero odmerki* v polju Date",
                    },
                    "Name": "NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date",
                },
            ],
            "Version": 2,
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
    }
}

_vaccinations_by_age_90_dose1_command = _create_by_age_range_command("'90+'", "1L")
_vaccinations_by_age_90_dose2_command = _create_by_age_range_command("'90+'", "2L")

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

# REQ
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

_vaccinations_by_age_range_90_dose1_req = _create_req(
    [_vaccinations_by_age_90_dose1_command]
)
_vaccinations_by_age_range_90_dose2_req = _create_req(
    [_vaccinations_by_age_90_dose2_command]
)

_vaccination_by_age_range_requests = _create_by_age_range_requests()
