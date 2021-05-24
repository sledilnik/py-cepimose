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
        "From": _get_date_range_group_From(
            CommandQueryFrom("c", "eRCO_​​podatki", 0),
            CommandQueryFrom("c1", "Calendar", 0),
            CommandQueryFrom("s", "Sifrant_regija", 0),
        ),
    },
    AgeGroup: {
        "Where": [["c1"], ["Starostni ​razred", "x"], ["c1"]],
        "From": _get_date_range_group_From(
            CommandQueryFrom("c", "eRCO_​​podatki", 0),
            CommandQueryFrom("c1", "Calendar", 0),
            CommandQueryFrom("x", "xls_SURS_starost", 0),
        ),
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

    group_options = _Date_Range_Group_Query_Options[group_type]

    group_from = group_options["From"]
    where = _create_date_range_group_Where(
        common_options["Query"]["Where"],
        group_options["Where"],
        [[start_date, end_date], [group.value], []],
    )
    command = {}
    command["Query"] = {
        "Version": common_options["Query"]["Version"],
        "From": group_from,
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
        "From": _get_date_range_group_From(
            CommandQueryFrom("c", "Calendar", 0),
            CommandQueryFrom("e", "eRCO_​​podatki", 0),
            CommandQueryFrom("s", "Sifrant_regija", 0),
        ),
    },
    AgeGroup: {
        "Where": [[], ["c"], ["Starostni ​razred", "x"], ["c"]],
        "From": _get_date_range_group_From(
            CommandQueryFrom("c", "Calendar", 0),
            CommandQueryFrom("e", "eRCO_​​podatki", 0),
            CommandQueryFrom("x", "xls_SURS_starost", 0),
        ),
    },
}


def _get_default_manufacturers_From():
    return {
        "From": [
            {"Name": "e", "Entity": "eRCO_​​podatki", "Type": 0},
            {"Name": "s", "Entity": "Sifrant_Cepivo", "Type": 0},
            {"Name": "c", "Entity": "Calendar", "Type": 0},
        ]
    }


def _get_manufacturer_From(name, entity):
    default = _get_default_manufacturers_From()
    default["From"].append({"Name": name, "Entity": entity, "Type": 0})
    return default


_manufacturer_region_From = _get_manufacturer_From("s1", "Sifrant_regija")
_manufacturer_age_group_From = _get_manufacturer_From("x1", "xls_SURS_starost")

_manufacturer_Select = [
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
]

_manufacturer_Where_first = {
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

_manufacturer_OrderBy = [
    {
        "Direction": 2,
        "Expression": {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "e"}},
                "Property": "Weight for 2",
            }
        },
    }
]

_manufacturer_Binding = {
    "Primary": {"Groupings": [{"Projections": [0, 1, 2]}]},
    "DataReduction": {"DataVolume": 3, "Primary": {"Window": {}}},
    "Version": 1,
}


def _replace_manufacturer_Query_From(obj: dict, property):
    obj["SemanticQueryDataShapeCommand"]["Query"]["From"] = property["From"]


def _replace_Query_Select(obj: dict, replace_with: list):
    obj["SemanticQueryDataShapeCommand"]["Query"]["Select"] = replace_with
    return obj


def _replace_gender_Query_Where(obj: dict):
    obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["And"][
        "Left"
    ]["Comparison"]["Left"]["Column"]["Expression"]["SourceRef"]["Source"] = "c"
    obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][0]["Condition"]["And"][
        "Right"
    ]["Comparison"]["Left"]["Column"]["Expression"]["SourceRef"]["Source"] = "c"

    obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][2]["Condition"][
        "Comparison"
    ]["Left"]["Column"]["Expression"]["SourceRef"]["Source"] = "c"

    return obj


# region Source = "s1", age_group Source = "x1"
def _replace_manufacturer_Query_Where(obj: dict, Source: str = "s1"):
    obj["SemanticQueryDataShapeCommand"]["Query"]["Where"][1]["Condition"]["In"][
        "Expressions"
    ][0]["Column"]["Expression"]["SourceRef"]["Source"] = Source


def _insert_gender_to_Query_Where(obj: dict, insert: dict, position=0):
    obj["SemanticQueryDataShapeCommand"]["Query"]["Where"].insert(position, insert)
    return obj


def _add_gender_OrderBy_to_Query(obj: dict, order_by: dict):
    obj["SemanticQueryDataShapeCommand"]["Query"] = {
        **obj["SemanticQueryDataShapeCommand"]["Query"],
        "OrderBy": order_by,
    }
    return obj


def _replace_Binding(obj: dict, property: dict):
    obj["SemanticQueryDataShapeCommand"]["Binding"] = property
    return obj


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
                    "From": group_options["From"],
                },
                **common,
            },
            "dose2": {
                "Query": {
                    "Version": common_options["Query"]["Version"],
                    "Select": common_options["Query"]["Select"]["dose2"],
                    "Where": where,
                    "OrderBy": common_options["Query"]["OrderBy"]["dose2"],
                    "From": group_options["From"],
                },
                **common,
            },
        }

    male1 = {"SemanticQueryDataShapeCommand": queries[Gender.MALE]["dose1"]}
    male2 = {"SemanticQueryDataShapeCommand": queries[Gender.MALE]["dose2"]}
    female1 = {"SemanticQueryDataShapeCommand": queries[Gender.FEMALE]["dose1"]}
    female2 = {"SemanticQueryDataShapeCommand": queries[Gender.FEMALE]["dose2"]}

    return [male1, male2, female1, female2]


def _get_manufacturers_command(obj: dict, group: Region or AgeGroup):
    if isinstance(group, Region):
        _replace_manufacturer_Query_From(obj, _manufacturer_region_From)
        _replace_Query_Select(obj, _manufacturer_Select)
        _replace_gender_Query_Where(obj)
        _replace_manufacturer_Query_Where(obj, "s1")
    elif isinstance(group, AgeGroup):
        _replace_manufacturer_Query_From(obj, _manufacturer_age_group_From)
        _replace_Query_Select(obj, _manufacturer_Select)
        _replace_gender_Query_Where(obj)
        _replace_manufacturer_Query_Where(obj, "x1")
    else:
        raise Exception("Argument [group] is not valid!")

    _insert_gender_to_Query_Where(obj, _manufacturer_Where_first)
    _add_gender_OrderBy_to_Query(obj, _manufacturer_OrderBy)
    _replace_Binding(obj, _manufacturer_Binding)
    return obj


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

    command_clone = copy.deepcopy(command)
    manufacturers = _get_manufacturers_command(command_clone, property)

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