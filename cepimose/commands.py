import copy
import datetime

from cepimose.enums import AgeGroup, Gender, Region
from cepimose.types import DateRangeCommands_Requests

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


_gender_From_firest_and_second = [
    {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
    {"Name": "c", "Entity": "Calendar", "Type": 0},
]

_gender_dose_1_Select = [
    {
        "Measure": {
            "Expression": {"SourceRef": {"Source": "e"}},
            "Property": "Weight for 1",
        },
        "Name": "eRCO_podatki.Weight for 1",
    }
]

_gender_dose_2_Select = [
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
        "Name": "Sum(eRCO_podatki_ed.Precepljenost)",
    }
]


def _get_gender_first_Where_item(gender):
    return {
        "Condition": {
            "In": {
                "Expressions": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "OsebaSpol",
                        }
                    }
                ],
                "Values": [[{"Literal": {"Value": f"'{gender.value}'"}}]],
            }
        }
    }


_gender_dose_1_OrderBy = [
    {
        "Direction": 2,
        "Expression": {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "e"}},
                "Property": "Weight for 1",
            }
        },
    }
]

_gender_dose_2_OrderBy = [
    {
        "Direction": 2,
        "Expression": {
            "Aggregation": {
                "Expression": {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "e"}},
                        "Property": "Precepljenost",
                    }
                },
                "Function": 0,
            }
        },
    }
]

_gender_Binding = {
    "Primary": {"Groupings": [{"Projections": [0]}]},
    "DataReduction": {"DataVolume": 3, "Primary": {"Window": {}}},
    "Version": 1,
}


def _replace_Query_From(obj: dict):
    obj["SemanticQueryDataShapeCommand"]["Query"]["From"][
        0
    ] = _gender_From_firest_and_second[0]
    obj["SemanticQueryDataShapeCommand"]["Query"]["From"][
        1
    ] = _gender_From_firest_and_second[1]
    return obj


def _replace_Query_Select(obj: dict, replace_with: list):
    clone_obj = {**obj}
    clone_obj["SemanticQueryDataShapeCommand"]["Query"]["Select"] = replace_with
    return {**clone_obj}


def _replace_Query_Where(obj: dict):
    clone_obj = {**obj}
    clone_obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["And"][
        "Left"
    ]["Comparison"]["Left"]["Column"]["Expression"]["SourceRef"]["Source"] = "c"
    clone_obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["And"][
        "Right"
    ]["Comparison"]["Left"]["Column"]["Expression"]["SourceRef"]["Source"] = "c"

    clone_obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][2]["Condition"][
        "Comparison"
    ]["Left"]["Column"]["Expression"]["SourceRef"]["Source"] = "c"

    return clone_obj


def _insert_to_Query_Where(obj: dict, insert: dict, position=0):
    clone_obj = {**obj}
    clone_obj["SemanticQueryDataShapeCommand"]["Query"]["Where"].insert(
        position, insert
    )
    return {**clone_obj}


def _add_OrderBy_to_Query(obj: dict, order_by: dict):
    clone_obj = {**obj}
    clone_obj["SemanticQueryDataShapeCommand"]["Query"] = {
        **clone_obj["SemanticQueryDataShapeCommand"]["Query"],
        "OrderBy": order_by,
    }
    return {**clone_obj}


def _replace_Binding(obj: dict):
    clone_obj = {**obj}
    clone_obj["SemanticQueryDataShapeCommand"]["Binding"] = _gender_Binding
    return clone_obj


def _create_gender_command(obj: dict, options: dict = {}):
    clone_obj = {**obj}
    select_options = options["Select"]
    where_options = options["Where"]
    order_by_options = options["OrderBy"]

    new_obj = _replace_Query_Select({**clone_obj}, select_options)
    new_obj = _replace_Query_Where({**new_obj})
    new_obj = _insert_to_Query_Where({**new_obj}, where_options)
    new_obj = _add_OrderBy_to_Query({**new_obj}, order_by_options)
    new_obj = _replace_Binding({**new_obj})

    return {**new_obj}


def _get_gender_commands(obj: dict):

    male_dose_1_options = {
        "Select": _gender_dose_1_Select,
        "Where": _get_gender_first_Where_item(Gender.MALE),
        "OrderBy": _gender_dose_1_OrderBy,
    }

    male_dose_2_options = {
        "Select": _gender_dose_2_Select,
        "Where": _get_gender_first_Where_item(Gender.MALE),
        "OrderBy": _gender_dose_2_OrderBy,
    }

    female_dose_1_options = {
        "Select": _gender_dose_1_Select,
        "Where": _get_gender_first_Where_item(Gender.FEMALE),
        "OrderBy": _gender_dose_1_OrderBy,
    }

    female_dose_2_options = {
        "Select": _gender_dose_2_Select,
        "Where": _get_gender_first_Where_item(Gender.FEMALE),
        "OrderBy": _gender_dose_2_OrderBy,
    }

    deepcopay_obj = copy.deepcopy(obj)
    _replace_Query_From(deepcopay_obj)

    male1 = copy.deepcopy(deepcopay_obj)
    male2 = copy.deepcopy(deepcopay_obj)
    female1 = copy.deepcopy(deepcopay_obj)
    female2 = copy.deepcopy(deepcopay_obj)

    male_dose_1 = _create_gender_command(male1, male_dose_1_options)
    male_dose_2 = _create_gender_command(male2, male_dose_2_options)
    female_dose_1 = _create_gender_command(female1, female_dose_1_options)
    female_dose_2 = _create_gender_command(female2, female_dose_2_options)
    return [male_dose_1, male_dose_2, female_dose_1, female_dose_2]


def get_date_range_command(
    end_date: datetime.datetime,
    start_date: datetime.datetime,
    property: Region or AgeGroup,
) -> DateRangeCommands_Requests:
    obj = {}
    obj["SemanticQueryDataShapeCommand"] = {
        **_region_age_group_Binding,
        **_region_age_group_ExecutionMetricsKind,
    }
    if isinstance(property, Region):
        query = _get_region_Query(
            end_date=end_date, start_date=start_date, region=property.value
        )
        # used
        obj["SemanticQueryDataShapeCommand"] = {
            **query,
            **obj["SemanticQueryDataShapeCommand"],
        }

        clone_obj = copy.deepcopy(obj)
        [male1, male2, female1, female2] = _get_gender_commands(clone_obj)
        commands = DateRangeCommands_Requests(obj, male1, male2, female1, female2)

        return commands

    if isinstance(property, AgeGroup):
        query = _get_age_group_Query(
            end_date=end_date, start_date=start_date, group=property.value
        )
        obj["SemanticQueryDataShapeCommand"] = {
            **query,
            **obj["SemanticQueryDataShapeCommand"],
        }

        clone_obj = copy.deepcopy(obj)
        [male1, male2, female1, female2] = _get_gender_commands(clone_obj)
        commands = DateRangeCommands_Requests(obj, male1, male2, female1, female2)

        return commands


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
                        "And": {
                            "Left": {
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
                                        "Literal": {
                                            "Value": "datetime'2021-02-05T00:00:00'"
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
                                                "SourceRef": {"Source": "c1"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-04-03T00:00:00'"
                                        }
                                    },
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

# for Pomurska - Male - First
"""
diff from _region_date_range_command:
Query:
    Version: OK!
    From: first and second item
    Select: completely different, just one item
    Where: add one item on first position
    OrderBy: new property 
Binding:different
ExecutionMetricsKind: OK!

"""

_region_date_range_by_gender_by_dose_1_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                {"Name": "c", "Entity": "Calendar", "Type": 0},
                {"Name": "s", "Entity": "Sifrant_regija", "Type": 0},
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
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "OsebaSpol",
                                    }
                                }
                            ],
                            "Values": [[{"Literal": {"Value": "'Moški'"}}]],
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
                                                "SourceRef": {"Source": "c"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-01-30T00:00:00'"
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
                                                "SourceRef": {"Source": "c"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-03-26T00:00:00'"
                                        }
                                    },
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
                            "Property": "Weight for 1",
                        }
                    },
                }
            ],
        },
        "Binding": {
            "Primary": {"Groupings": [{"Projections": [0]}]},
            "DataReduction": {"DataVolume": 3, "Primary": {"Window": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}


_region_date_range_by_gender_by_dose_2_command = {
    "Commands": [
        {
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [
                        {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
                        {"Name": "c", "Entity": "Calendar", "Type": 0},
                        {"Name": "s", "Entity": "Sifrant_regija", "Type": 0},
                    ],
                    "Select": [
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
                                    "Values": [[{"Literal": {"Value": "'Moški'"}}]],
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
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "Date",
                                                }
                                            },
                                            "Right": {
                                                "Literal": {
                                                    "Value": "datetime'2021-01-30T00:00:00'"
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
                                                        "SourceRef": {"Source": "c"}
                                                    },
                                                    "Property": "Date",
                                                }
                                            },
                                            "Right": {
                                                "Literal": {
                                                    "Value": "datetime'2021-03-26T00:00:00'"
                                                }
                                            },
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
                    "DataReduction": {"DataVolume": 3, "Primary": {"Window": {}}},
                    "Version": 1,
                },
                "ExecutionMetricsKind": 1,
            }
        }
    ]
}


my_gender_by_dose_1_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "e", "Entity": "eRCO_\u200b\u200bpodatki", "Type": 0},
                {"Name": "c", "Entity": "Calendar", "Type": 0},
                {"Name": "s", "Entity": "Sifrant_regija", "Type": 0},
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
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "OsebaSpol",
                                    }
                                }
                            ],
                            "Values": [[{"Literal": {"Value": "'Moški'"}}]],
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
                                                "SourceRef": {"Source": "c"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-01-30T00:00:00'"
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
                                                "SourceRef": {"Source": "c"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-03-26T00:00:00'"
                                        }
                                    },
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
                            "Property": "Weight for 1",
                        }
                    },
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

my_gender_by_dose_2_command = {
    "SemanticQueryDataShapeCommand": {
        "Query": {
            "Version": 2,
            "From": [
                {"Name": "e", "Entity": "eRCO_\u200b\u200bpodatki", "Type": 0},
                {"Name": "c", "Entity": "Calendar", "Type": 0},
                {"Name": "s", "Entity": "Sifrant_regija", "Type": 0},
            ],
            "Select": [
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
                                        "Expression": {"SourceRef": {"Source": "e"}},
                                        "Property": "OsebaSpol",
                                    }
                                }
                            ],
                            "Values": [[{"Literal": {"Value": "'Moški'"}}]],
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
                                                "SourceRef": {"Source": "c1"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-01-30T00:00:00'"
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
                                                "SourceRef": {"Source": "c1"}
                                            },
                                            "Property": "Date",
                                        }
                                    },
                                    "Right": {
                                        "Literal": {
                                            "Value": "datetime'2021-03-26T00:00:00'"
                                        }
                                    },
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
            "OrderBy": [
                {
                    "Direction": 2,
                    "Expression": {
                        "Aggregation": {
                            "Expression": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "e"}},
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
            "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
            "DataReduction": {"DataVolume": 4, "Primary": {"BinnedLineSample": {}}},
            "Version": 1,
        },
        "ExecutionMetricsKind": 1,
    }
}
