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

_vaccinations_by_day_req = {
	"cancelQueries": [],
	"modelId": 159824,
	"queries": [
		{
			"ApplicationContext": {
				"DatasetId": "7b40529e-a50e-4dd3-8fe8-997894b4cdaa",
				"Sources": [
					{
						"ReportId": "b201281d-b2e7-4470-9f4e-0b3063794c76"
					}
				]
			},
			"CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"Calendar\",\"Type\":0},{\"Name\":\"c\",\"Entity\":\"eRCO_podatki\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Date\"},\"Name\":\"Calendar.Date\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Weight running total in Date\"},\"Name\":\"eRCO_podatki.Weight running total in Date\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Odmerek\"},\"Name\":\"eRCO_podatki.Odmerek\"}],\"Where\":[{\"Condition\":{\"Comparison\":{\"ComparisonKind\":1,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Date\"}},\"Right\":{\"DateSpan\":{\"Expression\":{\"Literal\":{\"Value\":\"datetime'2020-12-26T01:00:00'\"}},\"TimeUnit\":5}}}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Intersection\":{\"BinnedLineSample\":{}}},\"Version\":1}}}]}",
			"Query": {
				"Commands": [
					{
						"SemanticQueryDataShapeCommand": {
							"Binding": {
								"DataReduction": {
									"DataVolume": 4,
									"Intersection": {
										"BinnedLineSample": {}
									}
								},
								"Primary": {
									"Groupings": [
										{
											"Projections": [
												0,
												1
											]
										}
									]
								},
								"Secondary": {
									"Groupings": [
										{
											"Projections": [
												2
											]
										}
									]
								},
								"Version": 1
							},
							"Query": {
								"From": [
									{
										"Entity": "Calendar",
										"Name": "c1",
										"Type": 0
									},
									{
										"Entity": "eRCO_podatki",
										"Name": "c",
										"Type": 0
									}
								],
								"Select": [
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "c1"
												}
											},
											"Property": "Date"
										},
										"Name": "Calendar.Date"
									},
									{
										"Measure": {
											"Expression": {
												"SourceRef": {
													"Source": "c"
												}
											},
											"Property": "Weight running total in Date"
										},
										"Name": "eRCO_podatki.Weight running total in Date"
									},
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "c"
												}
											},
											"Property": "Odmerek"
										},
										"Name": "eRCO_podatki.Odmerek"
									}
								],
								"Version": 2,
								"Where": [
									{
										"Condition": {
											"Comparison": {
												"ComparisonKind": 1,
												"Left": {
													"Column": {
														"Expression": {
															"SourceRef": {
																"Source": "c1"
															}
														},
														"Property": "Date"
													}
												},
												"Right": {
													"DateSpan": {
														"Expression": {
															"Literal": {
																"Value": "datetime'2020-12-26T01:00:00'"
															}
														},
														"TimeUnit": 5
													}
												}
											}
										}
									}
								]
							}
						}
					}
				]
			},
			"QueryId": ""
		}
	],
	"version": "1.0.0"
}

_vaccinations_by_age_req = {
	"cancelQueries": [],
	"modelId": 159824,
	"queries": [
		{
			"ApplicationContext": {
				"DatasetId": "7b40529e-a50e-4dd3-8fe8-997894b4cdaa",
				"Sources": [
					{
						"ReportId": "b201281d-b2e7-4470-9f4e-0b3063794c76"
					}
				]
			},
			"CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"e\",\"Entity\":\"eRCO_podatki\",\"Type\":0},{\"Name\":\"s\",\"Entity\":\"SURS_starost\",\"Type\":0},{\"Name\":\"c\",\"Entity\":\"Calendar\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Starostni razred\"},\"Name\":\"SURS_starost.Starostni razred\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Delež_starost\"},\"Name\":\"eRCO_podatki.Delež_starost\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Odmerek\"},\"Name\":\"eRCO_podatki.Odmerek\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Weight\"}},\"Function\":0},\"Name\":\"Sum(eRCO_podatki.Weight)\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"CepivoIme\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"null\"}}]]}}}}},{\"Condition\":{\"Comparison\":{\"ComparisonKind\":1,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Date\"}},\"Right\":{\"DateSpan\":{\"Expression\":{\"Literal\":{\"Value\":\"datetime'2020-12-26T01:00:00'\"}},\"TimeUnit\":5}}}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Starostni razred\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,3]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"SuppressedJoinPredicates\":[3],\"Version\":1}}}]}",
			"Query": {
				"Commands": [
					{
						"SemanticQueryDataShapeCommand": {
							"Binding": {
								"DataReduction": {
									"DataVolume": 4,
									"Primary": {
										"Window": {
											"Count": 200
										}
									},
									"Secondary": {
										"Top": {
											"Count": 60
										}
									}
								},
								"Primary": {
									"Groupings": [
										{
											"Projections": [
												0,
												1,
												3
											]
										}
									]
								},
								"Secondary": {
									"Groupings": [
										{
											"Projections": [
												2
											]
										}
									]
								},
								"SuppressedJoinPredicates": [
									3
								],
								"Version": 1
							},
							"Query": {
								"From": [
									{
										"Entity": "eRCO_podatki",
										"Name": "e",
										"Type": 0
									},
									{
										"Entity": "SURS_starost",
										"Name": "s",
										"Type": 0
									},
									{
										"Entity": "Calendar",
										"Name": "c",
										"Type": 0
									}
								],
								"OrderBy": [
									{
										"Direction": 1,
										"Expression": {
											"Column": {
												"Expression": {
													"SourceRef": {
														"Source": "s"
													}
												},
												"Property": "Starostni razred"
											}
										}
									}
								],
								"Select": [
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "s"
												}
											},
											"Property": "Starostni razred"
										},
										"Name": "SURS_starost.Starostni razred"
									},
									{
										"Measure": {
											"Expression": {
												"SourceRef": {
													"Source": "e"
												}
											},
											"Property": "Delež_starost"
										},
										"Name": "eRCO_podatki.Delež_starost"
									},
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "e"
												}
											},
											"Property": "Odmerek"
										},
										"Name": "eRCO_podatki.Odmerek"
									},
									{
										"Aggregation": {
											"Expression": {
												"Column": {
													"Expression": {
														"SourceRef": {
															"Source": "e"
														}
													},
													"Property": "Weight"
												}
											},
											"Function": 0
										},
										"Name": "Sum(eRCO_podatki.Weight)"
									}
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
																		"SourceRef": {
																			"Source": "e"
																		}
																	},
																	"Property": "CepivoIme"
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
														]
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
															"SourceRef": {
																"Source": "c"
															}
														},
														"Property": "Date"
													}
												},
												"Right": {
													"DateSpan": {
														"Expression": {
															"Literal": {
																"Value": "datetime'2020-12-26T01:00:00'"
															}
														},
														"TimeUnit": 5
													}
												}
											}
										}
									}
								]
							}
						}
					}
				]
			},
			"QueryId": ""
		}
	],
	"version": "1.0.0"
}

_vaccines_supplied_and_used_req = {
	"cancelQueries": [],
	"modelId": 159824,
	"queries": [
		{
			"ApplicationContext": {
				"DatasetId": "7b40529e-a50e-4dd3-8fe8-997894b4cdaa",
				"Sources": [
					{
						"ReportId": "b201281d-b2e7-4470-9f4e-0b3063794c76"
					}
				]
			},
			"CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"Calendar\",\"Type\":0},{\"Name\":\"c\",\"Entity\":\"eRCO_podatki\",\"Type\":0},{\"Name\":\"n\",\"Entity\":\"NIJZ_Odmerki\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Date\"},\"Name\":\"Calendar.Date\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Kumulativno skupaj cepljenih\"},\"Name\":\"eRCO_podatki.Kumulativno skupaj cepljenih\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"n\"}},\"Property\":\"Tekoča vsota za mero odmerki* v polju Date\"},\"Name\":\"NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date\"}],\"Where\":[{\"Condition\":{\"Comparison\":{\"ComparisonKind\":2,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Date\"}},\"Right\":{\"DateSpan\":{\"Expression\":{\"Literal\":{\"Value\":\"datetime'2020-12-26T00:00:00'\"}},\"TimeUnit\":5}}}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"BinnedLineSample\":{}}},\"Version\":1}}}]}",
			"Query": {
				"Commands": [
					{
						"SemanticQueryDataShapeCommand": {
							"Binding": {
								"DataReduction": {
									"DataVolume": 4,
									"Primary": {
										"BinnedLineSample": {}
									}
								},
								"Primary": {
									"Groupings": [
										{
											"Projections": [
												0,
												1,
												2
											]
										}
									]
								},
								"Version": 1
							},
							"Query": {
								"From": [
									{
										"Entity": "Calendar",
										"Name": "c1",
										"Type": 0
									},
									{
										"Entity": "eRCO_podatki",
										"Name": "c",
										"Type": 0
									},
									{
										"Entity": "NIJZ_Odmerki",
										"Name": "n",
										"Type": 0
									}
								],
								"Select": [
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "c1"
												}
											},
											"Property": "Date"
										},
										"Name": "Calendar.Date"
									},
									{
										"Measure": {
											"Expression": {
												"SourceRef": {
													"Source": "c"
												}
											},
											"Property": "Kumulativno skupaj cepljenih"
										},
										"Name": "eRCO_podatki.Kumulativno skupaj cepljenih"
									},
									{
										"Measure": {
											"Expression": {
												"SourceRef": {
													"Source": "n"
												}
											},
											"Property": "Tekoča vsota za mero odmerki* v polju Date"
										},
										"Name": "NIJZ_Odmerki.Tekoča vsota za mero odmerki* v polju Date"
									}
								],
								"Version": 2,
								"Where": [
									{
										"Condition": {
											"Comparison": {
												"ComparisonKind": 2,
												"Left": {
													"Column": {
														"Expression": {
															"SourceRef": {
																"Source": "c1"
															}
														},
														"Property": "Date"
													}
												},
												"Right": {
													"DateSpan": {
														"Expression": {
															"Literal": {
																"Value": "datetime'2020-12-26T00:00:00'"
															}
														},
														"TimeUnit": 5
													}
												}
											}
										}
									}
								]
							}
						}
					}
				]
			},
			"QueryId": ""
		}
	],
	"version": "1.0.0"
}

_vaccinations_by_region_req = {
	"cancelQueries": [],
	"modelId": 159824,
	"queries": [
		{
			"ApplicationContext": {
				"DatasetId": "7b40529e-a50e-4dd3-8fe8-997894b4cdaa",
				"Sources": [
					{
						"ReportId": "b201281d-b2e7-4470-9f4e-0b3063794c76"
					}
				]
			},
			"CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"e\",\"Entity\":\"eRCO_podatki\",\"Type\":0},{\"Name\":\"s1\",\"Entity\":\"Sifrant_regija\",\"Type\":0},{\"Name\":\"c\",\"Entity\":\"Calendar\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s1\"}},\"Property\":\"Regija\"},\"Name\":\"Sifrant_regija.Regija\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Odmerek\"},\"Name\":\"eRCO_podatki.Odmerek\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Delež_regija\"},\"Name\":\"eRCO_podatki.Delež_regija\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Weight\"}},\"Function\":0},\"Name\":\"Sum(eRCO_podatki.Weight)\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"CepivoIme\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"null\"}}]]}}}}},{\"Condition\":{\"Not\":{\"Expression\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s1\"}},\"Property\":\"Regija\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"null\"}}],[{\"Literal\":{\"Value\":\"'Celotna Slovenija'\"}}],[{\"Literal\":{\"Value\":\"'TUJINA'\"}}]]}}}}},{\"Condition\":{\"Comparison\":{\"ComparisonKind\":1,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Date\"}},\"Right\":{\"DateSpan\":{\"Expression\":{\"Literal\":{\"Value\":\"datetime'2020-12-26T01:00:00'\"}},\"TimeUnit\":5}}}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"e\"}},\"Property\":\"Delež_regija\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,2,3]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"SuppressedJoinPredicates\":[3],\"Version\":1}}}]}",
			"Query": {
				"Commands": [
					{
						"SemanticQueryDataShapeCommand": {
							"Binding": {
								"DataReduction": {
									"DataVolume": 4,
									"Primary": {
										"Window": {
											"Count": 200
										}
									},
									"Secondary": {
										"Top": {
											"Count": 60
										}
									}
								},
								"Primary": {
									"Groupings": [
										{
											"Projections": [
												0,
												2,
												3
											]
										}
									]
								},
								"Secondary": {
									"Groupings": [
										{
											"Projections": [
												1
											]
										}
									]
								},
								"SuppressedJoinPredicates": [
									3
								],
								"Version": 1
							},
							"Query": {
								"From": [
									{
										"Entity": "eRCO_podatki",
										"Name": "e",
										"Type": 0
									},
									{
										"Entity": "Sifrant_regija",
										"Name": "s1",
										"Type": 0
									},
									{
										"Entity": "Calendar",
										"Name": "c",
										"Type": 0
									}
								],
								"OrderBy": [
									{
										"Direction": 2,
										"Expression": {
											"Measure": {
												"Expression": {
													"SourceRef": {
														"Source": "e"
													}
												},
												"Property": "Delež_regija"
											}
										}
									}
								],
								"Select": [
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "s1"
												}
											},
											"Property": "Regija"
										},
										"Name": "Sifrant_regija.Regija"
									},
									{
										"Column": {
											"Expression": {
												"SourceRef": {
													"Source": "e"
												}
											},
											"Property": "Odmerek"
										},
										"Name": "eRCO_podatki.Odmerek"
									},
									{
										"Measure": {
											"Expression": {
												"SourceRef": {
													"Source": "e"
												}
											},
											"Property": "Delež_regija"
										},
										"Name": "eRCO_podatki.Delež_regija"
									},
									{
										"Aggregation": {
											"Expression": {
												"Column": {
													"Expression": {
														"SourceRef": {
															"Source": "e"
														}
													},
													"Property": "Weight"
												}
											},
											"Function": 0
										},
										"Name": "Sum(eRCO_podatki.Weight)"
									}
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
																		"SourceRef": {
																			"Source": "e"
																		}
																	},
																	"Property": "CepivoIme"
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
														]
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
																	"Property": "Regija"
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
															]
														]
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
															"SourceRef": {
																"Source": "c"
															}
														},
														"Property": "Date"
													}
												},
												"Right": {
													"DateSpan": {
														"Expression": {
															"Literal": {
																"Value": "datetime'2020-12-26T01:00:00'"
															}
														},
														"TimeUnit": 5
													}
												}
											}
										}
									}
								]
							}
						}
					}
				]
			},
			"QueryId": ""
		}
	],
	"version": "1.0.0"
}