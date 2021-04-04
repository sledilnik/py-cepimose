supplied_sum_by_name_res = {
    "jobIds": [
        "f16eb5a7-17a8-44d4-8d5e-5a2326a6b062"
    ],
    "results": [
        {
            "jobId": "f16eb5a7-17a8-44d4-8d5e-5a2326a6b062",
            "result": {
                "data": {
                    "descriptor": {
                        "Select": [
                            {
                                "Kind": 1,
                                "Depth": 0,
                                "Value": "G0",
                                "GroupKeys": [
                                    {
                                        "Source": {
                                            "Entity": "Calendar",
                                            "Property": "Date"
                                        },
                                        "Calc": "G0",
                                        "IsSameAsSelect": true
                                    }
                                ],
                                "Name": "Calendar.Date"
                            },
                            {
                                "Kind": 1,
                                "SecondaryDepth": 0,
                                "Value": "G1",
                                "GroupKeys": [
                                    {
                                        "Source": {
                                            "Entity": "Vezno_Vrsta_cepiva",
                                            "Property": "Vrsta_cepiva"
                                        },
                                        "Calc": "G1",
                                        "IsSameAsSelect": true
                                    }
                                ],
                                "Name": "Vezno_Vrsta_cepiva.Vrsta_cepiva"
                            },
                            {
                                "Kind": 2,
                                "Value": "M0",
                                "Format": "#,0",
                                "Name": "NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date"
                            }
                        ],
                        "Expressions": {
                            "Primary": {
                                "Groupings": [
                                    {
                                        "Keys": [
                                            {
                                                "Source": {
                                                    "Entity": "Calendar",
                                                    "Property": "Date"
                                                },
                                                "Select": 0
                                            }
                                        ],
                                        "Member": "DM0"
                                    }
                                ]
                            },
                            "Secondary": {
                                "Groupings": [
                                    {
                                        "Keys": [
                                            {
                                                "Source": {
                                                    "Entity": "Vezno_Vrsta_cepiva",
                                                    "Property": "Vrsta_cepiva"
                                                },
                                                "Select": 1
                                            }
                                        ],
                                        "Member": "DM1"
                                    }
                                ]
                            }
                        },
                        "Limits": {
                            "Intersection": {
                                "Id": "L0",
                                "BinnedLineSample": {
                                    "MaxTargetPointCount": 3500,
                                    "MinPointsPerSeriesCount": 350,
                                    "IntersectionDbCountCalc": "A0",
                                    "PrimaryDbCountCalc": "A1",
                                    "SecondaryDbCountCalc": "A2"
                                }
                            }
                        },
                        "Version": 2
                    },
                    "dsr": {
                        "Version": 2,
                        "MinorVersion": 1,
                        "DS": [
                            {
                                "N": "DS0",
                                "S": [
                                    {
                                        "N": "A0",
                                        "T": 4
                                    },
                                    {
                                        "N": "A1",
                                        "T": 4
                                    },
                                    {
                                        "N": "A2",
                                        "T": 4
                                    }
                                ],
                                "C": [
                                    33,
                                    30,
                                    3
                                ],
                                "SH": [
                                    {
                                        "DM1": [
                                            {
                                                "S": [
                                                    {
                                                        "N": "G1",
                                                        "T": 1
                                                    }
                                                ],
                                                "G1": "Astra Zeneca"
                                            },
                                            {
                                                "G1": "Moderna"
                                            },
                                            {
                                                "G1": "Pfizer-BioNTech"
                                            }
                                        ]
                                    }
                                ],
                                "PH": [
                                    {
                                        "DM0": [
                                            {
                                                "S": [
                                                    {
                                                        "N": "G0",
                                                        "T": 7
                                                    }
                                                ],
                                                "G0": 1608940800000,
                                                "X": [
                                                    {
                                                        "S": [
                                                            {
                                                                "N": "M0",
                                                                "T": 3
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "I": 2,
                                                        "M0": 11700
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1609286400000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 19890
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1609718400000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 39780
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1610323200000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 59670
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1610409600000,
                                                "X": [
                                                    {
                                                        "I": 1,
                                                        "M0": 1200
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1610928000000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 69030
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1611532800000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 88920
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1612051200000,
                                                "X": [
                                                    {
                                                        "I": 1,
                                                        "M0": 3600
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1612137600000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 106470
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1612483200000,
                                                "X": [
                                                    {
                                                        "I": 1,
                                                        "M0": 8400
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1612569600000,
                                                "X": [
                                                    {
                                                        "M0": 9600
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1612828800000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 124020
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1613001600000,
                                                "X": [
                                                    {
                                                        "M0": 19200
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1613347200000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 145080
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1613606400000,
                                                "X": [
                                                    {
                                                        "M0": 36000
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1613952000000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 167310
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1614211200000,
                                                "X": [
                                                    {
                                                        "M0": 52800
                                                    },
                                                    {
                                                        "M0": 16800
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1614556800000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 187200
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1614816000000,
                                                "X": [
                                                    {
                                                        "M0": 74400
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1615161600000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 207090
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1615420800000,
                                                "X": [
                                                    {
                                                        "M0": 88800
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1615507200000,
                                                "X": [
                                                    {
                                                        "I": 1,
                                                        "M0": 28800
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1615766400000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 226980
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1616112000000,
                                                "X": [
                                                    {
                                                        "M0": 93600
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1616371200000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 256230
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1616630400000,
                                                "X": [
                                                    {
                                                        "I": 1,
                                                        "M0": 46800
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1616716800000,
                                                "X": [
                                                    {
                                                        "M0": 98400
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1616976000000,
                                                "X": [
                                                    {
                                                        "I": 2,
                                                        "M0": 285480
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1617235200000,
                                                "X": [
                                                    {
                                                        "M0": 144000
                                                    }
                                                ]
                                            },
                                            {
                                                "G0": 1617321600000,
                                                "X": [
                                                    {
                                                        "M0": 144000.0001
                                                    },
                                                    {
                                                        "M0": 46800.0001
                                                    },
                                                    {
                                                        "M0": 285480.0001
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ],
                                "IC": true,
                                "HAD": true
                            }
                        ]
                    }
                }
            }
        }
    ]
}
