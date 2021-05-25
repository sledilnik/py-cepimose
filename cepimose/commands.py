import copy
import datetime
from typing import Union

from cepimose.enums import AgeGroup, Gender, Region, Manufacturer
from cepimose.types import CommandQueryFrom, DateRangeCommands_Requests


_ExecutionMetrics = {"ExecutionMetricsKind": 1}

# DATE RANGE GROUP WHERE
# Region and AgeGroup source = "c1",
def _get_date_range_group_Query_Where_FirstCondition(
    source: str, start_date: datetime.datetime, end_date: datetime.datetime
):
    left = {
        "Left": {
            "Comparison": {
                "ComparisonKind": 2,
                "Left": {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": source}},
                        "Property": "Date",
                    }
                },
                "Right": {"Literal": {"Value": f"datetime'{start_date.isoformat()}'"}},
            }
        }
    }
    right = {
        "Right": {
            "Comparison": {
                "ComparisonKind": 3,
                "Left": {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": source}},
                        "Property": "Date",
                    }
                },
                "Right": {"Literal": {"Value": f"datetime'{end_date.isoformat()}'"}},
            }
        },
    }

    obj = {}
    obj["Condition"] = {"And": {**left, **right}}
    return obj


# for AGE GROUP: property="Starostni ​razred", source="x"
# for REGION: property="Regija", source="s"
def _get_date_range_group_Query_Where_SecondCondition(
    property: str, source: str, value: str
):
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


# Region and AgeGroup source = "c1",
def _get_date_range_group_Query_Where_ThirdCondition(source: str):
    return {
        "Condition": {
            "Comparison": {
                "ComparisonKind": 1,
                "Left": {
                    "Column": {
                        "Expression": {"SourceRef": {"Source": source}},
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


def _get_date_range_group_From(*args: CommandQueryFrom):
    result = []
    for arg in args:
        result.append({"Name": arg.name, "Entity": arg.entity, "Type": arg.type})
    return result


def _get_Binding(projections: list, data_volume: int, primary: dict, version: int):
    return {
        "Primary": {"Groupings": [{"Projections": projections}]},
        "DataReduction": {"DataVolume": data_volume, "Primary": primary},
        "Version": version,
    }


_Date_Range_Group_Query_Options = {
    "common": {
        "Query": {
            "Version": 2,
            "Where": [
                _get_date_range_group_Query_Where_FirstCondition,
                _get_date_range_group_Query_Where_SecondCondition,
                _get_date_range_group_Query_Where_ThirdCondition,
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
        },
        "Binding": _get_Binding([0, 1, 2], 4, {"BinnedLineSample": {}}, 1),
    },
    Region: {
        "Where": [["c1"], ["Regija", "s"], ["c1"]],
        "From": [
            CommandQueryFrom("c", "eRCO_​​podatki", 0),
            CommandQueryFrom("c1", "Calendar", 0),
            CommandQueryFrom("s", "Sifrant_regija", 0),
        ],
    },
    AgeGroup: {
        "Where": [["c1"], ["Starostni ​razred", "x"], ["c1"]],
        "From": [
            CommandQueryFrom("c", "eRCO_​​podatki", 0),
            CommandQueryFrom("c1", "Calendar", 0),
            CommandQueryFrom("x", "xls_SURS_starost", 0),
        ],
    },
}


def _create_date_range_group_Where(
    functions: list,
    arguments: list,
    special_args: list,
):
    result = []
    for index, func in enumerate(functions):
        result.append(func(*arguments[index], *special_args[index]))

    return result


def _get_date_range_group_Query(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    group: Region or AgeGroup,
    common_options: dict,
    group_options: dict,
):
    group_type = type(group)
    if not group_type in [Region, AgeGroup]:
        raise Exception(
            f"Wrong arg [group] type: {group_type}. Possible types: {Region}, {AgeGroup}"
        )

    from_args = group_options["From"]
    where = _create_date_range_group_Where(
        common_options["Query"]["Where"],
        group_options["Where"],
        [[start_date, end_date], [group.value], []],
    )
    command = {}
    command["Query"] = {
        "Version": common_options["Query"]["Version"],
        "From": _get_date_range_group_From(*from_args),
        "Select": common_options["Query"]["Select"],
        "Where": where,
    }
    return command


# GENDER
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


_Date_Range_Group_Gender_Query_Options = {
    "common": {
        "Query": {
            "Version": 2,
            "Where": [
                _get_gender_first_Where_item,
                _get_date_range_group_Query_Where_FirstCondition,
                _get_date_range_group_Query_Where_SecondCondition,
                _get_date_range_group_Query_Where_ThirdCondition,  # arg = "c"
            ],
            "Select": {
                "dose1": [
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "Weight for 1",
                        },
                        "Name": "eRCO_podatki.Weight for 1",
                    }
                ],
                "dose2": [
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
            },
            "OrderBy": {
                "dose1": [
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
                "dose2": [
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
        },
        "Binding": _get_Binding([0], 3, {"Window": {}}, 1),
    },
    Region: {
        "Where": [[], ["c"], ["Regija", "s"], ["c"]],
        "From": [
            CommandQueryFrom("c", "Calendar", 0),
            CommandQueryFrom("e", "eRCO_​​podatki", 0),
            CommandQueryFrom("s", "Sifrant_regija", 0),
        ],
    },
    AgeGroup: {
        "Where": [[], ["c"], ["Starostni ​razred", "x"], ["c"]],
        "From": [
            CommandQueryFrom("c", "Calendar", 0),
            CommandQueryFrom("e", "eRCO_​​podatki", 0),
            CommandQueryFrom("x", "xls_SURS_starost", 0),
        ],
    },
}


def _get_manufacturer_Where_first():
    return {
        "Condition": {
            "Not": {
                "Expression": {
                    "In": {
                        "Expressions": [
                            {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "s"}},
                                    "Property": "Cepivo_Ime",
                                }
                            }
                        ],
                        "Values": [[{"Literal": {"Value": "null"}}]],
                    }
                }
            }
        }
    }


_Date_Range_Group_Manufacturers_Query_Options = {
    "common": {
        "Query": {
            "Version": 2,
            "Where": [
                _get_manufacturer_Where_first,
                _get_date_range_group_Query_Where_FirstCondition,
                _get_date_range_group_Query_Where_SecondCondition,
                _get_date_range_group_Query_Where_ThirdCondition,
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
            "OrderBy": [
                {
                    "Direction": 2,
                    "Expression": {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "e"}},
                            "Property": "Weight for 2",
                        }
                    },
                }
            ],
        },
        "Binding": _get_Binding([0, 1, 2], 3, {"Window": {}}, 1),
    },
    Region: {
        "Where": [[], ["c"], ["Regija", "s1"], ["c"]],
        "From": [
            CommandQueryFrom("e", "eRCO_​​podatki", 0),
            CommandQueryFrom("s", "Sifrant_Cepivo", 0),
            CommandQueryFrom("c", "Calendar", 0),
            CommandQueryFrom("s1", "Sifrant_regija", 0),
        ],
    },
    AgeGroup: {
        "Where": [[], ["c"], ["Starostni ​razred", "x1"], ["c"]],
        "From": [
            CommandQueryFrom("e", "eRCO_​​podatki", 0),
            CommandQueryFrom("s", "Sifrant_Cepivo", 0),
            CommandQueryFrom("c", "Calendar", 0),
            CommandQueryFrom("x1", "xls_SURS_starost", 0),
        ],
    },
}


def _get_gender_commands(
    start_date,
    end_date,
    group: Region or AgeGroup,
):

    group_type = type(group)
    group_options = _Date_Range_Group_Gender_Query_Options[group_type]
    common_options = _Date_Range_Group_Gender_Query_Options["common"]

    queries = {}
    for gender in Gender:
        where = _create_date_range_group_Where(
            common_options["Query"]["Where"],
            group_options["Where"],
            [[gender], [start_date, end_date], [group.value], []],
        )
        _from = _get_date_range_group_From(*group_options["From"])
        common = {
            "Binding": common_options["Binding"],
            **_ExecutionMetrics,
        }
        queries[gender] = {
            "dose1": {
                "Query": {
                    "Version": common_options["Query"]["Version"],
                    "Select": common_options["Query"]["Select"]["dose1"],
                    "Where": where,
                    "OrderBy": common_options["Query"]["OrderBy"]["dose1"],
                    "From": _from,
                },
                **common,
            },
            "dose2": {
                "Query": {
                    "Version": common_options["Query"]["Version"],
                    "Select": common_options["Query"]["Select"]["dose2"],
                    "Where": where,
                    "OrderBy": common_options["Query"]["OrderBy"]["dose2"],
                    "From": _from,
                },
                **common,
            },
        }

    male1 = {"SemanticQueryDataShapeCommand": queries[Gender.MALE]["dose1"]}
    male2 = {"SemanticQueryDataShapeCommand": queries[Gender.MALE]["dose2"]}
    female1 = {"SemanticQueryDataShapeCommand": queries[Gender.FEMALE]["dose1"]}
    female2 = {"SemanticQueryDataShapeCommand": queries[Gender.FEMALE]["dose2"]}

    return [male1, male2, female1, female2]


def _get_manufacturers_command(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    group: Region or AgeGroup,
):
    group_type = type(group)
    group_options = _Date_Range_Group_Manufacturers_Query_Options[group_type]
    common_options = _Date_Range_Group_Manufacturers_Query_Options["common"]

    command = {}
    command["SemanticQueryDataShapeCommand"] = {
        "Binding": common_options["Binding"],
        **_ExecutionMetrics,
    }

    where = _create_date_range_group_Where(
        common_options["Query"]["Where"],
        group_options["Where"],
        [[], [start_date, end_date], [group.value], []],
    )
    _from = _get_date_range_group_From(*group_options["From"])

    query = {
        "Query": {
            "Version": common_options["Query"]["Version"],
            "From": _from,
            "Where": where,
            "Select": common_options["Query"]["Select"],
            "OrderBy": common_options["Query"]["OrderBy"],
        }
    }

    command["SemanticQueryDataShapeCommand"] = {
        **query,
        **command["SemanticQueryDataShapeCommand"],
    }

    return command


def _get_date_range_command(
    end_date: datetime.datetime,
    start_date: datetime.datetime,
    property: Region or AgeGroup,
) -> DateRangeCommands_Requests:
    common_options = _Date_Range_Group_Query_Options["common"]

    command = {}
    command["SemanticQueryDataShapeCommand"] = {
        "Binding": common_options["Binding"],
        **_ExecutionMetrics,
    }

    group_type = type(property)
    group_options = _Date_Range_Group_Query_Options[group_type]

    query = _get_date_range_group_Query(
        start_date, end_date, property, common_options, group_options
    )

    command["SemanticQueryDataShapeCommand"] = {
        **query,
        **command["SemanticQueryDataShapeCommand"],
    }

    [male1, male2, female1, female2] = _get_gender_commands(
        start_date, end_date, property
    )

    manufacturers = _get_manufacturers_command(start_date, end_date, property)

    commands = DateRangeCommands_Requests(
        command, male1, male2, female1, female2, manufacturers
    )

    return commands


def _get_default_manufacturer_used_command(manu: Manufacturer):
    return {
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
                                "Values": [[{"Literal": {"Value": f"'{manu.value}'"}}]],
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


def _create_manufacturers_used_commands():
    obj = {}
    for manu in Manufacturer:
        obj[manu] = _get_default_manufacturer_used_command(manu)

    return obj