from cepimose.enums import AgeGroup, Region
import datetime

_where_third_common = {
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
                        "Literal": {"Value": "datetime'2020-12-26T01:00:00'"}
                    },
                    "TimeUnit": 5,
                }
            },
        }
    }
}

# region comparison_kind = 2
# age group comparison_kind = 3
def _getWhereRightDateCondition(date: datetime.datetime):
    return {
        "Right": {
            "Comparison": {
                "ComparisonKind": 3,
                "Left": {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c1"}},
                        "Property": "Date",
                    }
                },
                "Right": {"Literal": {"Value": f"datetime'{date.isoformat()}'"}},
            }
        },
    }


def _getWhereLeftDateCondition(date: datetime.datetime):
    return {
        "Left": {
            "Comparison": {
                "ComparisonKind": 2,
                "Left": {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "c1"}},
                        "Property": "Date",
                    }
                },
                "Right": {"Literal": {"Value": f"datetime'{date.isoformat()}'"}},
            }
        }
    }


def _getWhereFirstCondition(left, right):
    obj = {}
    # print(left, right)
    obj["Condition"] = {"And": {**left, **right}}
    return obj


# for AGE GROUP: property="Starostni ​razred", source="x"
def _getWherePropertyCondition(value, property="Regija", source="s"):
    return {
        "Condition": {
            "In": {
                "Expressions": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": source}},
                            "Property": property,
                        }
                    }
                ],
                "Values": [[{"Literal": {"Value": f"'{value}'"}}]],
            }
        }
    }


region_age_group_Version = {"Version": 2}


def _get_default_region_age_group_From():
    return {
        "From": [
            {"Name": "c1", "Entity": "Calendar", "Type": 0},
            {"Name": "c", "Entity": "eRCO_​​podatki", "Type": 0},
        ]
    }


def _get_From(name, entity):
    default = _get_default_region_age_group_From()
    default["From"].append({"Name": name, "Entity": entity, "Type": 0})
    return default


region_From = _get_From("s", "Sifrant_regija")
age_group_From = _get_From("x", "xls_SURS_starost")

region_and_age_group_Select = {
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
    ]
}


def _get_region_Query(
    end_date: datetime.datetime, start_date: datetime.datetime, region
):
    where_left = _getWhereLeftDateCondition(start_date)
    where_right = _getWhereRightDateCondition(end_date)
    where_first = _getWhereFirstCondition(where_left, where_right)
    where_second = _getWherePropertyCondition(region, "Regija", "s")
    where_third = _where_third_common

    where = {"Where": [where_first, where_second, where_third]}

    obj = {}
    obj["Query"] = {
        **region_age_group_Version,
        **region_From,
        **region_and_age_group_Select,
        **where,
    }

    return obj


def _get_age_group_Query(
    end_date: datetime.datetime, start_date: datetime.datetime, group
):
    where_left = _getWhereLeftDateCondition(start_date)
    where_right = _getWhereRightDateCondition(end_date)
    where_first = _getWhereFirstCondition(where_left, where_right)
    where_second = _getWherePropertyCondition(group, "Starostni ​razred", "x")
    where_third = _where_third_common

    where = {"Where": [where_first, where_second, where_third]}

    obj = {
        "Query": {
            **region_age_group_Version,
            **age_group_From,
            **region_and_age_group_Select,
            **where,
        }
    }

    return obj


_region_age_group_Binding = {
    "Binding": {
        "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
        "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
        "Version": 1,
    }
}

_region_age_group_ExecutionMetricsKind = {"ExecutionMetricsKind": 1}


def get_date_range_command(
    end_date: datetime.datetime,
    start_date: datetime.datetime,
    property: Region or AgeGroup,
):
    obj = {}
    obj["SemanticQueryDataShapeCommand"] = {
        **_region_age_group_Binding,
        **_region_age_group_ExecutionMetricsKind,
    }
    if isinstance(property, Region):
        query = _get_region_Query(
            end_date=end_date, start_date=start_date, region=property.value
        )
        obj["SemanticQueryDataShapeCommand"] = {
            **query,
            **obj["SemanticQueryDataShapeCommand"],
        }
        return obj

    if isinstance(property, AgeGroup):
        query = _get_age_group_Query(
            end_date=end_date, start_date=start_date, group=property.value
        )
        obj["SemanticQueryDataShapeCommand"] = {
            **query,
            **obj["SemanticQueryDataShapeCommand"],
        }
        return obj


# COMMAND EXAMPLES
# for Pomurska
_region_date_range_command = {
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
                        "Comparison": {
                            "ComparisonKind": 2,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c1"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "Literal": {"Value": "datetime'2021-02-22T00:00:00'"}
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
                                        "Expression": {"SourceRef": {"Source": "s"}},
                                        "Property": "Regija",
                                    }
                                }
                            ],
                            "Values": [[{"Literal": {"Value": "'Pomurska'"}}]],
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

# for 90+
_age_group_date_range_command = {
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
                        "Comparison": {
                            "ComparisonKind": 3,
                            "Left": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "c1"}},
                                    "Property": "Date",
                                }
                            },
                            "Right": {
                                "Literal": {"Value": "datetime'2021-03-17T00:00:00'"}
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
                                        "Expression": {"SourceRef": {"Source": "x"}},
                                        "Property": "Starostni ​razred",
                                    }
                                }
                            ],
                            "Values": [[{"Literal": {"Value": "'90+'"}}]],
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
            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
            "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}
