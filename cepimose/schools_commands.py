# https://app.powerbi.com/view?r=eyJrIjoiNjdmMTYxOGUtNGY4ZC00YjMxLTgzMWEtZWExNTJmYmIxMGRiIiwidCI6ImFkMjQ1ZGFlLTQ0YTAtNGQ5NC04OTY3LTVjNjk5MGFmYTQ2MyIsImMiOjl9

# Število in odstotek potrjenih in število aktivnih primerov
_schools_confirmed_and_active_cases_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
            ],
            "Select": [
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Zadnji_teden_sum",
                    },
                    "Name": "Query1.Zadnji_teden_sum",
                },
                {
                    "Arithmetic": {
                        "Left": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Source": "q"}},
                                "Property": "Zadnji_teden_sum",
                            }
                        },
                        "Right": {
                            "ScopedEval": {
                                "Expression": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "q"}},
                                        "Property": "Zadnji_teden_sum",
                                    }
                                },
                                "Scope": [],
                            }
                        },
                        "Operator": 3,
                    },
                    "Name": "Divide(Query1.Zadnji_teden_sum, ScopedEval(Query1.Zadnji_teden_sum, []))",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Aktivni_primeri",
                    },
                    "Name": "Query1.Aktivni_primeri",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Starostni_razred1",
                    },
                    "Name": "Query1.Starostni_razred1",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Primer",
                    },
                    "Name": "Query1.Primer",
                },
                {
                    "Arithmetic": {
                        "Left": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Source": "q"}},
                                "Property": "Primer",
                            }
                        },
                        "Right": {
                            "ScopedEval": {
                                "Expression": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "q"}},
                                        "Property": "Primer",
                                    }
                                },
                                "Scope": [],
                            }
                        },
                        "Operator": 3,
                    },
                    "Name": "Divide(Query1.Primer, ScopedEval(Query1.Primer, []))",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                            "Expression": {"SourceRef": {"Source": "q"}},
                            "Property": "Starostni_razred1",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {
                "Groupings": [{"Projections": [0, 1, 2, 3, 4, 5], "Subtotal": 1}]
            },
            "DataReduction": {
                "DataVolume": 3,
                "Primary": {"Window": {"Count": 500}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

# Odstotek potrjenih primerov otrok in mladostnikov po starostnih skupinah med prebivalci
_schools_age_group_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "s1", "Entity": "SURS_data_MO", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
            ],
            "Select": [
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "s1"}},
                                "Property": "Število",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "Sum(SURS_data_MO.Število)",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Delez_starostMO_tabela",
                    },
                    "Name": "Query1.Delez_starostMO_tabela",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Primer",
                    },
                    "Name": "Query1.Primer",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s1"}},
                        "Property": "Razred_MO",
                    },
                    "Name": "SURS_data_MO.Razred_MO",
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
                                                    "SourceRef": {"Source": "s1"}
                                                },
                                                "Property": "Razred_MO",
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
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                            "Expression": {"SourceRef": {"Source": "s1"}},
                            "Property": "Razred_MO",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2, 3], "Subtotal": 1}]},
            "DataReduction": {
                "DataVolume": 3,
                "Primary": {"Window": {"Count": 500}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

#  Odstotek potrjenih primerov otrok in mladostnikov po starostnih skupinah (triade) med prebivalci
_schools_age_groups_triada_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "s", "Entity": "SURS_data_Triada", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
            ],
            "Select": [
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "s"}},
                                "Property": "Število",
                            }
                        },
                        "Function": 0,
                    },
                    "Name": "SURS_data_Triada.Število",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Triada_razred",
                    },
                    "Name": "SURS_data_Triada.Triada_razred",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "DeležTriadaTabela",
                    },
                    "Name": "Query1.DeležTriadaTabela",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Primer",
                    },
                    "Name": "Query1.Primer",
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
                                                "Property": "Triada_razred",
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
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                            "Property": "Triada_razred",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1, 2, 3], "Subtotal": 1}]},
            "DataReduction": {"DataVolume": 3, "Primary": {"Window": {"Count": 500}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

# Podatki veljajo za obdobje
_schools_date_range_timestamps_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {
                    "Name": "q",
                    "Expression": {
                        "Subquery": {
                            "Query": {
                                "Version": 2,
                                "From": [
                                    {"Name": "t", "Entity": "Teden", "Type": 0},
                                    {
                                        "Name": "subquery1",
                                        "Expression": {
                                            "Subquery": {
                                                "Query": {
                                                    "Version": 2,
                                                    "From": [
                                                        {
                                                            "Name": "st",
                                                            "Entity": "Teden",
                                                            "Type": 0,
                                                        }
                                                    ],
                                                    "Select": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "st"
                                                                    }
                                                                },
                                                                "Property": "ISO_Leto_teden",
                                                            },
                                                            "Name": "Teden.ISO_Leto_teden",
                                                        }
                                                    ],
                                                    "Where": [
                                                        {
                                                            "Condition": {
                                                                "Not": {
                                                                    "Expression": {
                                                                        "Comparison": {
                                                                            "ComparisonKind": 0,
                                                                            "Left": {
                                                                                "Column": {
                                                                                    "Expression": {
                                                                                        "SourceRef": {
                                                                                            "Source": "st"
                                                                                        }
                                                                                    },
                                                                                    "Property": "Razlika_tedenISO",
                                                                                }
                                                                            },
                                                                            "Right": {
                                                                                "Literal": {
                                                                                    "Value": "0L"
                                                                                }
                                                                            },
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "Condition": {
                                                                "Comparison": {
                                                                    "ComparisonKind": 2,
                                                                    "Left": {
                                                                        "Column": {
                                                                            "Expression": {
                                                                                "SourceRef": {
                                                                                    "Source": "st"
                                                                                }
                                                                            },
                                                                            "Property": "Ponedeljek",
                                                                        }
                                                                    },
                                                                    "Right": {
                                                                        "DateSpan": {
                                                                            "Expression": {
                                                                                "Literal": {
                                                                                    "Value": "datetime'2021-08-30T00:00:00'"
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
                                                                    "Expression": {
                                                                        "SourceRef": {
                                                                            "Source": "st"
                                                                        }
                                                                    },
                                                                    "Property": "Ponedeljek",
                                                                }
                                                            },
                                                        }
                                                    ],
                                                    "Top": 1,
                                                }
                                            }
                                        },
                                        "Type": 2,
                                    },
                                ],
                                "Select": [
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Ponedeljek",
                                        },
                                        "Name": "Teden.Ponedeljek",
                                    }
                                ],
                                "Where": [
                                    {
                                        "Condition": {
                                            "Not": {
                                                "Expression": {
                                                    "Comparison": {
                                                        "ComparisonKind": 0,
                                                        "Left": {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "t"
                                                                    }
                                                                },
                                                                "Property": "Razlika_tedenISO",
                                                            }
                                                        },
                                                        "Right": {
                                                            "Literal": {"Value": "0L"}
                                                        },
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "Condition": {
                                            "Comparison": {
                                                "ComparisonKind": 2,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {"Source": "t"}
                                                        },
                                                        "Property": "Ponedeljek",
                                                    }
                                                },
                                                "Right": {
                                                    "DateSpan": {
                                                        "Expression": {
                                                            "Literal": {
                                                                "Value": "datetime'2021-08-30T00:00:00'"
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
                                                                "SourceRef": {
                                                                    "Source": "t"
                                                                }
                                                            },
                                                            "Property": "ISO_Leto_teden",
                                                        }
                                                    }
                                                ],
                                                "Table": {
                                                    "SourceRef": {"Source": "subquery1"}
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
                                                "Expression": {
                                                    "SourceRef": {"Source": "t"}
                                                },
                                                "Property": "Ponedeljek",
                                            }
                                        },
                                    }
                                ],
                            }
                        }
                    },
                    "Type": 2,
                },
                {
                    "Name": "q1",
                    "Expression": {
                        "Subquery": {
                            "Query": {
                                "Version": 2,
                                "From": [
                                    {"Name": "t1", "Entity": "Teden", "Type": 0},
                                    {
                                        "Name": "subquery11",
                                        "Expression": {
                                            "Subquery": {
                                                "Query": {
                                                    "Version": 2,
                                                    "From": [
                                                        {
                                                            "Name": "st1",
                                                            "Entity": "Teden",
                                                            "Type": 0,
                                                        }
                                                    ],
                                                    "Select": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "st1"
                                                                    }
                                                                },
                                                                "Property": "ISO_Leto_teden",
                                                            },
                                                            "Name": "Teden.ISO_Leto_teden",
                                                        }
                                                    ],
                                                    "Where": [
                                                        {
                                                            "Condition": {
                                                                "Not": {
                                                                    "Expression": {
                                                                        "Comparison": {
                                                                            "ComparisonKind": 0,
                                                                            "Left": {
                                                                                "Column": {
                                                                                    "Expression": {
                                                                                        "SourceRef": {
                                                                                            "Source": "st1"
                                                                                        }
                                                                                    },
                                                                                    "Property": "Razlika_tedenISO",
                                                                                }
                                                                            },
                                                                            "Right": {
                                                                                "Literal": {
                                                                                    "Value": "0L"
                                                                                }
                                                                            },
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "Condition": {
                                                                "Comparison": {
                                                                    "ComparisonKind": 2,
                                                                    "Left": {
                                                                        "Column": {
                                                                            "Expression": {
                                                                                "SourceRef": {
                                                                                    "Source": "st1"
                                                                                }
                                                                            },
                                                                            "Property": "Ponedeljek",
                                                                        }
                                                                    },
                                                                    "Right": {
                                                                        "DateSpan": {
                                                                            "Expression": {
                                                                                "Literal": {
                                                                                    "Value": "datetime'2021-08-30T00:00:00'"
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
                                                                "Column": {
                                                                    "Expression": {
                                                                        "SourceRef": {
                                                                            "Source": "st1"
                                                                        }
                                                                    },
                                                                    "Property": "Nedelja",
                                                                }
                                                            },
                                                        }
                                                    ],
                                                    "Top": 1,
                                                }
                                            }
                                        },
                                        "Type": 2,
                                    },
                                ],
                                "Select": [
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t1"}
                                            },
                                            "Property": "Nedelja",
                                        },
                                        "Name": "Teden.Nedelja",
                                    }
                                ],
                                "Where": [
                                    {
                                        "Condition": {
                                            "Not": {
                                                "Expression": {
                                                    "Comparison": {
                                                        "ComparisonKind": 0,
                                                        "Left": {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "t1"
                                                                    }
                                                                },
                                                                "Property": "Razlika_tedenISO",
                                                            }
                                                        },
                                                        "Right": {
                                                            "Literal": {"Value": "0L"}
                                                        },
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "Condition": {
                                            "Comparison": {
                                                "ComparisonKind": 2,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "t1"
                                                            }
                                                        },
                                                        "Property": "Ponedeljek",
                                                    }
                                                },
                                                "Right": {
                                                    "DateSpan": {
                                                        "Expression": {
                                                            "Literal": {
                                                                "Value": "datetime'2021-08-30T00:00:00'"
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
                                                                "SourceRef": {
                                                                    "Source": "t1"
                                                                }
                                                            },
                                                            "Property": "ISO_Leto_teden",
                                                        }
                                                    }
                                                ],
                                                "Table": {
                                                    "SourceRef": {
                                                        "Source": "subquery11"
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
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "t1"}
                                                },
                                                "Property": "Nedelja",
                                            }
                                        },
                                    }
                                ],
                            }
                        }
                    },
                    "Type": 2,
                },
            ],
            "Select": [
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "q"}},
                                "Property": "Teden.Ponedeljek",
                            }
                        },
                        "Function": 3,
                    },
                    "Name": "Min(expr.Teden.Ponedeljek)",
                },
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "q1"}},
                                "Property": "Teden.Nedelja",
                            }
                        },
                        "Function": 3,
                    },
                    "Name": "Min(expr.Teden.Nedelja)",
                },
            ],
        },
        "Binding": {"Primary": {"Groupings": [{"Projections": [0, 1]}]}, "Version": 1},
        "ExecutionMetricsKind": 1,
    }
}

# Število potrjenih primerov otrok in mladostnikov po starostnih skupinah (zadnji in prejšnji teden)
_schools_age_group_confirmed_weekly_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Starostni_razred1",
                    },
                    "Name": "Query1.Starostni_razred1",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "t"}},
                        "Property": "ISO_Leto_teden",
                    },
                    "Name": "Teden.ISO_Leto_teden",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Primer",
                    },
                    "Name": "Query1.Primer",
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
                                                    "SourceRef": {"Source": "q"}
                                                },
                                                "Property": "Starostni_razred1",
                                            }
                                        }
                                    ],
                                    "Values": [
                                        [{"Literal": {"Value": "'e: 19 let in več'"}}]
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
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                            "Expression": {"SourceRef": {"Source": "t"}},
                            "Property": "ISO_Leto_teden",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [1, 2]}]},
            "Secondary": {"Groupings": [{"Projections": [0]}]},
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Window": {"Count": 200}},
                "Secondary": {"Top": {"Count": 60}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

#  Odstotek potrjenih primerov otrok in mladostnikov po starostnih skupinah med prebivalci (zadnji in prejšnji teden)
_schools_age_group_percent_per_capita_weekly_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "t", "Entity": "Teden", "Type": 0},
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "s", "Entity": "SURS_data_MO", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "t"}},
                        "Property": "ISO_Leto_teden",
                    },
                    "Name": "Teden.ISO_Leto_teden",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Delez_starostMO_tabela",
                    },
                    "Name": "Query1.Delez_starostMO_tabela",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Razred_MO",
                    },
                    "Name": "SURS_data_MO.Razred_MO",
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
                                                "Property": "Razred_MO",
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
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                            "Expression": {"SourceRef": {"Source": "t"}},
                            "Property": "ISO_Leto_teden",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1]}]},
            "Secondary": {"Groupings": [{"Projections": [2]}]},
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Window": {"Count": 200}},
                "Secondary": {"Top": {"Count": 60}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

# Odstotek potrjenih primerov otrok in mladostnikov po starostnih skupinah (triade) med prebivalci -> weekly
_schools_age_groups_percent_triada_weekly_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
                {"Name": "s", "Entity": "SURS_data_Triada", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "t"}},
                        "Property": "ISO_Leto_teden",
                    },
                    "Name": "Teden.ISO_Leto_teden",
                },
                {
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "DeležTriada",
                    },
                    "Name": "Query1.DeležTriada",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "s"}},
                        "Property": "Triada_razred",
                    },
                    "Name": "SURS_data_Triada.Triada_razred",
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
                                                "Property": "Triada_razred",
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
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "q"}},
                            "Property": "DeležTriada",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0, 1]}]},
            "Secondary": {"Groupings": [{"Projections": [2]}]},
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Window": {"Count": 200}},
                "Secondary": {"Top": {"Count": 60}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

# Odstotek potrjenih primerov po starostnih skupinah
_schools_age_group_percent_weekly_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "q", "Entity": "Query1", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
            ],
            "Select": [
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "q"}},
                        "Property": "Starostni_razred1",
                    },
                    "Name": "Query1.Starostni_razred1",
                },
                {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "t"}},
                        "Property": "ISO_Leto_teden",
                    },
                    "Name": "Teden.ISO_Leto_teden",
                },
                {
                    "Arithmetic": {
                        "Left": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Source": "q"}},
                                "Property": "Primer",
                            }
                        },
                        "Right": {
                            "ScopedEval": {
                                "Expression": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "q"}},
                                        "Property": "Primer",
                                    }
                                },
                                "Scope": [],
                            }
                        },
                        "Operator": 3,
                    },
                    "Name": "Query1.Primer",
                },
            ],
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
                            "Expression": {"SourceRef": {"Source": "t"}},
                            "Property": "ISO_Leto_teden",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [1, 2]}]},
            "Secondary": {"Groupings": [{"Projections": [0]}]},
            "DataReduction": {
                "DataVolume": 4,
                "Primary": {"Window": {"Count": 200}},
                "Secondary": {"Top": {"Count": 60}},
            },
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}

# Datum osvežitve podatkov
_schools_timestamp_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "c", "Entity": "Calendar", "Type": 0},
                {"Name": "t", "Entity": "Teden", "Type": 0},
            ],
            "Select": [
                {
                    "Aggregation": {
                        "Expression": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "c"}},
                                "Property": "Danes",
                            }
                        },
                        "Function": 3,
                    },
                    "Name": "Min(Calendar.Danes)",
                }
            ],
            "Where": [
                {
                    "Condition": {
                        "Not": {
                            "Expression": {
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {"Source": "t"}
                                            },
                                            "Property": "Razlika_tedenISO",
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "0L"}},
                                }
                            }
                        }
                    }
                },
                {
                    "Condition": {
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "t"}},
                                    "Property": "Ponedeljek",
                                }
                            },
                            "Right": {
                                "DateSpan": {
                                    "Expression": {
                                        "Literal": {
                                            "Value": "datetime'2021-08-30T00:00:00'"
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
            "Primary": {"Groupings": [{"Projections": [0]}]},
            "DataReduction": {"DataVolume": 3, "Primary": {"Top": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}