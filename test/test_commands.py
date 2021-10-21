import datetime
from enum import unique
import unittest
from unittest.case import skip
import cepimose
from cepimose.enums import AgeGroup, Gender, Manufacturer, Region

_timestamp_queries = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
                                                "Property": "DatumOsveževanja",
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
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
            ]
        },
        "CacheKey": '{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"e","Entity":"eRCO_​​podatki","Type":0},{"Name":"c","Entity":"Calendar","Type":0}],"Select":[{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"e"}},"Property":"DatumOsveževanja"}},"Function":3},"Name":"Min(eRCO_podatki.DatumOsvezevanja)"}],"Where":[{"Condition":{"Comparison":{"ComparisonKind":1,"Left":{"Column":{"Expression":{"SourceRef":{"Source":"c"}},"Property":"Date"}},"Right":{"DateSpan":{"Expression":{"Literal":{"Value":"datetime\'2020-12-26T01:00:00\'"}},"TimeUnit":5}}}}}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0]}]},"DataReduction":{"DataVolume":3,"Primary":{"Top":{}}},"Version":1},"ExecutionMetricsKind":1}}]}',
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "da086fda6709e1327c0d",
                }
            ],
        },
    }
]

_by_age_group_queries = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "c1", "Entity": "Calendar", "Type": 0},
                                {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "x", "Entity": "xls_SURS_starost", "Type": 0},
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
                                                            "SourceRef": {"Source": "x"}
                                                        },
                                                        "Property": "Starostni ​razred",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'90+'"}}]
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
                                                                        "Source": "c"
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
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c1"}
                                                    },
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
                            "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {"BinnedLineSample": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "37907fcc1d650bd01406",
                }
            ],
        },
    }
]

_by_region_by_day_queries = [
    {
        "Query": {
            "Commands": [
                {
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
                                            "Values": [
                                                [{"Literal": {"Value": "'Pomurska'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c1"}
                                                    },
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
                            "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {"BinnedLineSample": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "37907fcc1d650bd01406",
                }
            ],
        },
    }
]

_age_group_by_region_queries = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
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
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Delež_regija_1",
                                    },
                                    "Name": "eRCO_podatki.Delež_regija",
                                },
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Delež_regija_precepljenost",
                                    },
                                    "Name": "eRCO_podatki_ed.Delež_regija_precepljenost",
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
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
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
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
                                                                        "Source": "s1"
                                                                    }
                                                                },
                                                                "Property": "Regija",
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "null"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Celotna Slovenija'"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'TUJINA'"
                                                                }
                                                            }
                                                        ],
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
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
                                            "Expression": {
                                                "SourceRef": {"Source": "e"}
                                            },
                                            "Property": "Delež_regija_1",
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {
                                "Groupings": [{"Projections": [0, 1, 2, 3, 4]}]
                            },
                            "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {"Window": {"Count": 1000}},
                            },
                            "SuppressedJoinPredicates": [3, 4],
                            "Version": 1,
                            "Highlights": [
                                {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "x",
                                            "Entity": "xls_SURS_starost",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "e",
                                            "Entity": "eRCO_​​podatki",
                                            "Type": 0,
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
                                                                    "SourceRef": {
                                                                        "Source": "x"
                                                                    }
                                                                },
                                                                "Property": "Starostni ​razred",
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'90+'"
                                                                }
                                                            }
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
                                                                [
                                                                    {
                                                                        "Literal": {
                                                                            "Value": "null"
                                                                        }
                                                                    }
                                                                ]
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
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "73a64094acbd371ddd40",
                }
            ],
        },
    }
]

_manufacturer_supplied_used_queries = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "c1", "Entity": "Calendar", "Type": 0},
                                {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
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
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c1"}
                                                    },
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
                                            "Values": [
                                                [
                                                    {
                                                        "Literal": {
                                                            "Value": "'Pfizer-BioNTech'"
                                                        }
                                                    }
                                                ]
                                            ],
                                        }
                                    }
                                },
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
                            "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {"BinnedLineSample": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "8233796ced1be0a31515",
                }
            ],
        },
    }
]

male_dose_1_queries_2021_05_01_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {
                                    "Name": "e",
                                    "Entity": "eRCO_\u200b\u200bpodatki",
                                    "Type": 0,
                                },
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Weight for 1",
                                    },
                                    "Name": "eRCO_podatki.Weight for 1",
                                }
                            ],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [
                                                {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "e"}
                                                        },
                                                        "Property": "OsebaSpol",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'Moški'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 3,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "Date",
                                                }
                                            },
                                            "Right": {
                                                "Literal": {
                                                    "Value": "datetime'2021-05-03T00:00:00'"
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "Date",
                                                }
                                            },
                                            "Right": {
                                                "DateSpan": {
                                                    "Expression": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
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
                                            "Expression": {
                                                "SourceRef": {"Source": "e"}
                                            },
                                            "Property": "Weight for 1",
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "8233796ced1be0a31515",
                }
            ],
        },
    }
]

male_dose_2_queries_2021_05_01_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {
                                    "Name": "e",
                                    "Entity": "eRCO_\u200b\u200bpodatki",
                                    "Type": 0,
                                },
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
                                                "Property": "Precepljenost",
                                            }
                                        },
                                        "Function": 0,
                                    },
                                    "Name": "Sum(eRCO_podatki_ed.Precepljenost)",
                                }
                            ],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [
                                                {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "e"}
                                                        },
                                                        "Property": "OsebaSpol",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'Moški'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 3,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "Date",
                                                }
                                            },
                                            "Right": {
                                                "Literal": {
                                                    "Value": "datetime'2021-05-03T00:00:00'"
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "Date",
                                                }
                                            },
                                            "Right": {
                                                "DateSpan": {
                                                    "Expression": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
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
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "e"}
                                                    },
                                                    "Property": "Precepljenost",
                                                }
                                            },
                                            "Function": 0,
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "8233796ced1be0a31515",
                }
            ],
        },
    }
]

group_date_range_queries = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "c1", "Entity": "Calendar", "Type": 0},
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
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c1"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c1"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c1"}
                                                    },
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
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
                            "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {"BinnedLineSample": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "37907fcc1d650bd01406",
                }
            ],
        },
    }
]

male1_date_range_queries_2021_05_01_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Weight for 1",
                                    },
                                    "Name": "eRCO_podatki.Weight for 1",
                                }
                            ],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [
                                                {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "e"}
                                                        },
                                                        "Property": "OsebaSpol",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'Moški'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
                            ],
                            "OrderBy": [
                                {
                                    "Direction": 2,
                                    "Expression": {
                                        "Measure": {
                                            "Expression": {
                                                "SourceRef": {"Source": "e"}
                                            },
                                            "Property": "Weight for 1",
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "37907fcc1d650bd01406",
                }
            ],
        },
    }
]

male2_date_range_queries_2021_05_01_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
                                                "Property": "Precepljenost",
                                            }
                                        },
                                        "Function": 0,
                                    },
                                    "Name": "Sum(eRCO_podatki_ed.Precepljenost)",
                                }
                            ],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [
                                                {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "e"}
                                                        },
                                                        "Property": "OsebaSpol",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'Moški'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
                            ],
                            "OrderBy": [
                                {
                                    "Direction": 2,
                                    "Expression": {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "e"}
                                                    },
                                                    "Property": "Precepljenost",
                                                }
                                            },
                                            "Function": 0,
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "58905942ae8d24176dbd",
                }
            ],
        },
    }
]

female1_date_range_queries_2021_05_01_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Weight for 1",
                                    },
                                    "Name": "eRCO_podatki.Weight for 1",
                                }
                            ],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [
                                                {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "e"}
                                                        },
                                                        "Property": "OsebaSpol",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'Ženske'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
                            ],
                            "OrderBy": [
                                {
                                    "Direction": 2,
                                    "Expression": {
                                        "Measure": {
                                            "Expression": {
                                                "SourceRef": {"Source": "e"}
                                            },
                                            "Property": "Weight for 1",
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "df157d8c2c7b603db9b4",
                }
            ],
        },
    }
]

female2_date_range_queries_2021_05_01_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e"}
                                                },
                                                "Property": "Precepljenost",
                                            }
                                        },
                                        "Function": 0,
                                    },
                                    "Name": "Sum(eRCO_podatki_ed.Precepljenost)",
                                }
                            ],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [
                                                {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "e"}
                                                        },
                                                        "Property": "OsebaSpol",
                                                    }
                                                }
                                            ],
                                            "Values": [
                                                [{"Literal": {"Value": "'Ženske'"}}]
                                            ],
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
                            ],
                            "OrderBy": [
                                {
                                    "Direction": 2,
                                    "Expression": {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "e"}
                                                    },
                                                    "Property": "Precepljenost",
                                                }
                                            },
                                            "Function": 0,
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "00a1a6bd176268d0daab",
                }
            ],
        },
    }
]

manufacturers_date_range_queries_2021_05_21_2021_05_03 = [
    {
        "Query": {
            "Commands": [
                {
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                                {"Name": "s", "Entity": "Sifrant_Cepivo", "Type": 0},
                                {"Name": "c", "Entity": "Calendar", "Type": 0},
                            ],
                            "Select": [
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Weight for 1",
                                    },
                                    "Name": "eRCO_podatki.Weight for 1",
                                },
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "Weight for 2",
                                    },
                                    "Name": "eRCO_podatki.Weight for 2",
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
                                        "Not": {
                                            "Expression": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "s"
                                                                    }
                                                                },
                                                                "Property": "Cepivo_Ime",
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
                                {
                                    "Condition": {
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-01T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "c"
                                                                }
                                                            },
                                                            "Property": "Date",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2021-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            },
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 1,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {"Source": "c"}
                                                    },
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
                            ],
                            "OrderBy": [
                                {
                                    "Direction": 2,
                                    "Expression": {
                                        "Measure": {
                                            "Expression": {
                                                "SourceRef": {"Source": "e"}
                                            },
                                            "Property": "Weight for 2",
                                        }
                                    },
                                }
                            ],
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {}},
                            },
                            "Version": 1,
                        },
                        "ExecutionMetricsKind": 1,
                    }
                }
            ]
        },
        "QueryId": "",
        "ApplicationContext": {
            "DatasetId": "51c64860-e9ec-49d8-8a36-743bced78e1a",
            "Sources": [
                {
                    "ReportId": "dddc4907-41d2-4b6c-b34b-3aac90b7fdee",
                    "VisualId": "61ce741d0886b757de37",
                }
            ],
        },
    }
]


@skip
class CepimoseTestCommands(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def tearDown(self):
        super().tearDown()

    def get_command(self, obj: "list[dict]"):
        print(obj)
        return obj[0]["Query"]["Commands"][0]

    def get_SemanticQueryDataShapeCommand_field(
        self, obj: "list[dict]", field: str = "Query"
    ):
        command = self.get_command(obj)
        return command["SemanticQueryDataShapeCommand"].get(field, None)

    def compare(self, real: dict, our: dict):
        for key, value in real.items():
            print(key, value)
            print(key, our[key])
            print()
            if isinstance(value, dict):
                self.assertDictEqual(
                    value,
                    our[key],
                )
            else:
                self.assertEqual(
                    value,
                    our[key],
                )

    # @unittest.skip("TODO")
    def test_timestamp_command(self):
        ts_command = self.get_command(_timestamp_queries)
        self.assertDictEqual(
            ts_command,
            cepimose.data._vaccinations_timestamp_command,
        )

    # @unittest.skip("TODO")
    def test_by_age_group_command(self):
        age_group_commands = cepimose.data._create_by_age_group_commands()
        group_90_command = age_group_commands[AgeGroup.GROUP_90][0]
        self.assertDictEqual(self.get_command(_by_age_group_queries), group_90_command)

    # @unittest.skip("TODO")
    def test_by_region_by_day_command(self):
        region_commands = cepimose.data._create_by_region_by_day_commands()
        region_pomurska_command = region_commands[Region.POMURSKA][0]
        self.assertDictEqual(
            self.get_command(_by_region_by_day_queries), region_pomurska_command
        )

    # @unittest.skip("TODO")
    def test_age_group_by_region_command(self):
        age_group_commands = cepimose.data._create_age_group_by_region_on_day_commands()
        group_90_command = age_group_commands[AgeGroup.GROUP_90][0]
        self.assertDictEqual(
            self.get_command(_age_group_by_region_queries), group_90_command
        )

    # @unittest.skip("TODO")
    def test_age_group_by_region_command(self):
        manufacturer_commands = (
            cepimose.data._create_vaccination_by_manufacturer_supplied_used_commands()
        )
        pfizer_command = manufacturer_commands[Manufacturer.PFIZER][0]
        self.assertDictEqual(
            self.get_command(_manufacturer_supplied_used_queries), pfizer_command
        )

    # @unittest.skip("TODO")
    def test_gender_commands(self):
        gender_commands = cepimose.data._create_vaccinations_gender_commands(
            start_date=datetime.datetime(2021, 5, 1),
            end_date=datetime.datetime(2021, 5, 3),
        )
        male_commands = gender_commands[Gender.MALE]
        male_dose_1_command, male_dose_2_command = male_commands
        self.assertDictEqual(
            self.get_command(male_dose_1_queries_2021_05_01_2021_05_03),
            male_dose_1_command,
        )
        self.assertDictEqual(
            self.get_command(male_dose_2_queries_2021_05_01_2021_05_03),
            male_dose_2_command,
        )

    # @unittest.skip("TODO")
    def test_date_range_commands(self):
        date_range_commands = cepimose.commands._get_date_range_group_commands(
            start_date=datetime.datetime(2021, 5, 1),
            end_date=datetime.datetime(2021, 5, 3),
            group=None,
        )

        self.assertDictEqual(
            self.get_command(group_date_range_queries), date_range_commands.group
        )

        real_male_1_Query = self.get_command(
            male1_date_range_queries_2021_05_01_2021_05_03
        )
        real_male_2_Query = self.get_command(
            male2_date_range_queries_2021_05_01_2021_05_03
        )
        real_female_1_Query = self.get_command(
            female1_date_range_queries_2021_05_01_2021_05_03
        )
        real_female_2_Query = self.get_command(
            female2_date_range_queries_2021_05_01_2021_05_03
        )
        real_manufacturers_Query = self.get_command(
            manufacturers_date_range_queries_2021_05_21_2021_05_03
        )

        self.assertDictEqual(real_male_1_Query, date_range_commands.male1)
        self.assertDictEqual(real_male_2_Query, date_range_commands.male2)
        self.assertDictEqual(real_female_1_Query, date_range_commands.female1)
        self.assertDictEqual(real_female_2_Query, date_range_commands.female2)
        self.assertDictEqual(
            real_manufacturers_Query, date_range_commands.manufacturers
        )
