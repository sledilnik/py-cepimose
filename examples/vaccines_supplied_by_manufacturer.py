supplied_by_name_res = {
    "jobIds": ["973bf604-1b94-40aa-8a42-d8db674573c9"],
    "results": [
        {
            "jobId": "973bf604-1b94-40aa-8a42-d8db674573c9",
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
                                            "Property": "Date",
                                        },
                                        "Calc": "G0",
                                        "IsSameAsSelect": true,
                                    }
                                ],
                                "Name": "Calendar.Date",
                            },
                            {
                                "Kind": 1,
                                "Depth": 0,
                                "Value": "G1",
                                "GroupKeys": [
                                    {
                                        "Source": {
                                            "Entity": "NIJZ_Odmerki",
                                            "Property": "Vrsta cepiva",
                                        },
                                        "Calc": "G1",
                                        "IsSameAsSelect": true,
                                    }
                                ],
                                "Name": "NIJZ_Odmerki.Vrsta cepiva",
                            },
                            {
                                "Kind": 2,
                                "Value": "M0",
                                "Format": "#,0",
                                "Subtotal": ["A0"],
                                "Name": "Sum(NIJZ_Odmerki.odmerki*)",
                            },
                        ],
                        "Expressions": {
                            "Primary": {
                                "Groupings": [
                                    {
                                        "Keys": [
                                            {
                                                "Source": {
                                                    "Entity": "Calendar",
                                                    "Property": "Date",
                                                },
                                                "Select": 0,
                                            },
                                            {
                                                "Source": {
                                                    "Entity": "NIJZ_Odmerki",
                                                    "Property": "Vrsta cepiva",
                                                },
                                                "Select": 1,
                                            },
                                        ],
                                        "Member": "DM1",
                                        "SubtotalMember": "DM0",
                                    }
                                ]
                            }
                        },
                        "Version": 2,
                    },
                    "dsr": {
                        "Version": 2,
                        "MinorVersion": 1,
                        "DS": [
                            {
                                "N": "DS0",
                                "PH": [
                                    {
                                        "DM0": [
                                            {"S": [{"N": "A0", "T": 3}], "A0": 476280}
                                        ]
                                    },
                                    {
                                        "DM1": [
                                            {
                                                "S": [
                                                    {"N": "G0", "T": 7},
                                                    {"N": "G1", "T": 1, "DN": "D0"},
                                                    {"N": "M0", "T": 3},
                                                ],
                                                "C": [1608940800000, 0, 11700],
                                            },
                                            {"C": [1609286400000, 8190], "R": 2},
                                            {"C": [1609718400000, 19890], "R": 2},
                                            {"C": [1610323200000], "R": 6},
                                            {"C": [1610409600000, 1, 1200]},
                                            {"C": [1610928000000, 0, 9360]},
                                            {"C": [1611532800000, 19890], "R": 2},
                                            {"C": [1612051200000, 1, 2400]},
                                            {"C": [1612137600000, 0, 17550]},
                                            {"C": [1612483200000, 1, 4800]},
                                            {"C": [1612569600000, 2, 9600]},
                                            {"C": [1612828800000, 0, 17550]},
                                            {"C": [1613001600000, 2, 9600]},
                                            {"C": [1613347200000, 0, 21060]},
                                            {"C": [1613606400000, 2, 16800]},
                                            {"C": [1613952000000, 0, 22230]},
                                            {"C": [1614211200000, 2, 16800]},
                                            {"C": [1, 8400], "R": 1},
                                            {"C": [1614556800000, 0, 19890]},
                                            {"C": [1614816000000, 2, 21600]},
                                            {"C": [1615161600000, 0, 19890]},
                                            {"C": [1615420800000, 2, 14400]},
                                            {"C": [1615507200000, 1, 12000]},
                                            {"C": [1615766400000, 0, 19890]},
                                            {"C": [1616112000000, 2, 4800]},
                                            {"C": [1616371200000, 0, 29250]},
                                            {"C": [1616630400000, 1, 18000]},
                                            {"C": [1616716800000, 2, 4800]},
                                            {"C": [1616976000000, 0, 29250]},
                                            {"C": [1617235200000, 2, 45600]},
                                        ]
                                    },
                                ],
                                "IC": true,
                                "HAD": true,
                                "ValueDicts": {
                                    "D0": ["Pfizer-BioNTech", "Moderna", "Astra Zeneca"]
                                },
                            }
                        ],
                    },
                }
            },
        }
    ],
}
