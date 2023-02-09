def sample_simulation_response():
    return {
        "groupData": [{
            "model": {
                "id": "16cb1109-d036-4999-b668-0b3faf8728a4",
                "tags": ["test1", "test2"],
                "title": "REGALBELOITCORP-11-21-2022",
                "templateId": "d87b8446-38a1-4fd4-ad71-a40c3ef77b0f",
                "ticker": "RBC",
                "companyName": "REGAL BELOIT CORP",
                "currency": "USD",
                "industry": "MOTORS & GENERATORS",
                "geography": "United States",
                "createdAt": "2022-11-22 14:35:19",
                "lastUpdate": "0001-01-01T00:00:00Z",
                "dataSources": "default",
                "startPeriod": 2019,
                "forecastPeriod": 5,
                "historicalPeriod": 5,
                "iterations": 100,
                "precision": 0.001,
                "periodType": "ANNUAL",
                "edges": {}
            },
            "fields": {
                "Change in IRR": {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "format":
                    "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                    "value": "0",
                    "edges": {}
                },
                "Current share price (DCF)": {
                    "id": "868cf808-32fb-4deb-b987-5c2647d00677",
                    "identifier": "[DCF[Current share price[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"decimalPlaces\":\"2\",\"valFormat\":\"Currency\"}",
                    "formula": "PRICE(RBC, 11/21/2022)",
                    "internalFormula": "PRICE(RBC, 11/21/2022)",
                    "error": "Invalid syntax",
                    "edges": {}
                },
                "Implied premium (DCF)": {
                    "id": "fb96ca77-7295-4abb-8821-49ca494cd5ba",
                    "identifier": "[DCF[Implied premium[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontWeight\":\"bold\",\"fontStyle\":\"italic\",\"decimalPlaces\":\"2\",\"valFormat\":\"Percentage\"}",
                    "formula":
                    "[DCF[Implied share price[2019]]] / [DCF[Current share price[2019]]] - 1",
                    "internalFormula":
                    "[DCF[Implied share price[2019]]] / [DCF[Current share price[2019]]] - 1",
                    "error": "Invalid syntax",
                    "edges": {}
                },
                "Implied share price (DCF)": {
                    "id": "96b503c9-0069-409a-aff7-238a678c17b4",
                    "identifier": "[DCF[Implied share price[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontWeight\":\"bold\",\"valFormat\":\"Currency\"}",
                    "value": "64.65889880620502",
                    "formula":
                    "[DCF[Equity value[2019]]] / [DCF[Diluted[2019]]]",
                    "internalFormula":
                    "[DCF[Equity value[2019]]] / [DCF[Diluted[2019]]]",
                    "edges": {}
                },
                "Perpetual growth rate (DCF)": {
                    "id": "0abbeb31-5c8c-486a-9e1f-39099a28b70d",
                    "identifier": "[DCF[Perpetual growth rate[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                    "value": "0.0089",
                    "formula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "internalFormula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "edges": {}
                },
                "Perpetual growth rate (DCF) (Simulated)": {
                    "id": "0abbeb31-5c8c-486a-9e1f-39099a28b70d",
                    "identifier": "[DCF[Perpetual growth rate[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                    "value": "0.0089",
                    "formula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "internalFormula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "edges": {
                        "dependantCells": [{
                            "id": "e6b095de-7535-416b-9f14-0a51596133b8",
                            "identifier": "[DCF[Terminal value[2019]]]",
                            "edges": {}
                        }],
                        "precedentCells": [{
                            "id": "d04463e0-6b5c-48e3-a7d4-0753aa4fcce7",
                            "identifier":
                            "[DCF Drivers[Risk-free rate[2019]]]",
                            "edges": {}
                        }]
                    }
                },
                "Ticker": {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "period": 2019,
                    "format": "{\\\"valFormat\\\":\\\"Plain text\\\"}\"",
                    "value": "RBC",
                    "dataValue": "RBC",
                    "formula": "RBC",
                    "internalFormula": "RBC",
                    "edges": {}
                }
            }
        }, {
            "model": {
                "id": "a7aae9eb-861b-420c-89d7-829b47bce230",
                "title": "MCDONALDSCORP-11-22-2022",
                "templateId": "d87b8446-38a1-4fd4-ad71-a40c3ef77b0f",
                "ticker": "MCD",
                "companyName": "MCDONALDS CORP",
                "currency": "USD",
                "industry": "RETAIL-EATING PLACES",
                "geography": "United States",
                "createdAt": "2022-11-23 11:35:24",
                "lastUpdate": "0001-01-01T00:00:00Z",
                "dataSources": "default",
                "startPeriod": 2019,
                "forecastPeriod": 5,
                "historicalPeriod": 5,
                "iterations": 100,
                "precision": 0.001,
                "periodType": "ANNUAL",
                "rollForward": True,
                "updates": True,
                "edges": {}
            },
            "fields": {
                "Change in IRR": {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "format":
                    "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                    "value": "0",
                    "edges": {}
                },
                "Current share price (DCF)": {
                    "id": "b570faa3-01f0-418f-ae06-f8348b331613",
                    "identifier": "[DCF[Current share price[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"decimalPlaces\":\"2\",\"valFormat\":\"Currency\"}",
                    "formula": "PRICE(MCD, 11/22/2022)",
                    "internalFormula": "PRICE(MCD, 11/22/2022)",
                    "error": "Invalid syntax",
                    "edges": {}
                },
                "Implied premium (DCF)": {
                    "id": "65f5b521-f3d2-49bb-b2fa-4c2eb213f0bb",
                    "identifier": "[DCF[Implied premium[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontWeight\":\"bold\",\"fontStyle\":\"italic\",\"decimalPlaces\":\"2\",\"valFormat\":\"Percentage\"}",
                    "formula":
                    "[DCF[Implied share price[2019]]] / [DCF[Current share price[2019]]] - 1",
                    "internalFormula":
                    "[DCF[Implied share price[2019]]] / [DCF[Current share price[2019]]] - 1",
                    "error": "Invalid syntax",
                    "edges": {}
                },
                "Implied share price (DCF)": {
                    "id": "609fc527-2c0b-487b-b763-70482032a38f",
                    "identifier": "[DCF[Implied share price[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontWeight\":\"bold\",\"valFormat\":\"Currency\"}",
                    "value": "-0.776625753327982",
                    "formula":
                    "[DCF[Equity value[2019]]] / [DCF[Diluted[2019]]]",
                    "internalFormula":
                    "[DCF[Equity value[2019]]] / [DCF[Diluted[2019]]]",
                    "edges": {}
                },
                "Perpetual growth rate (DCF)": {
                    "id": "9a56d6c7-8d00-449c-a9f6-5ef2ca663f3e",
                    "identifier": "[DCF[Perpetual growth rate[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                    "value": "0.0089",
                    "formula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "internalFormula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "edges": {}
                },
                "Perpetual growth rate (DCF) (Simulated)": {
                    "id": "9a56d6c7-8d00-449c-a9f6-5ef2ca663f3e",
                    "identifier": "[DCF[Perpetual growth rate[2019]]]",
                    "period": 2019,
                    "format":
                    "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                    "value": "0.0089",
                    "formula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "internalFormula": "[DCF Drivers[Risk-free rate[2019]]]",
                    "edges": {
                        "dependantCells": [{
                            "id": "3a6505c6-94be-409b-b4a3-0d9828288cc6",
                            "identifier": "[DCF[Terminal value[2019]]]",
                            "edges": {}
                        }],
                        "precedentCells": [{
                            "id": "feef8220-74b2-41b8-bc44-90be942168bc",
                            "identifier":
                            "[DCF Drivers[Risk-free rate[2019]]]",
                            "edges": {}
                        }]
                    }
                },
                "Ticker": {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "period": 2019,
                    "format": "{\\\"valFormat\\\":\\\"Plain text\\\"}\"",
                    "value": "MCD",
                    "dataValue": "MCD",
                    "formula": "MCD",
                    "internalFormula": "MCD",
                    "edges": {}
                }
            }
        }],
        "simulation": [{
            "id":
            "a7aae9eb-861b-420c-89d7-829b47bce230",
            "ticker":
            "MCD",
            "startPeriod":
            2019,
            "forecastEndPeriod":
            2024,
            "historicalStartPeriod":
            2015,
            "lineItems": [{
                "id": "0615a14a-b695-4188-a2f0-7850a0e50e32",
                "name": "Perpetual growth rate",
                "order": 20,
                "tags": ["DCF", "Perpetual growth rate (DCF)"],
                "format":
                "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                "edges": {
                    "facts": [{
                        "id": "0388afc1-b71e-4441-bc61-376c3e9126e4",
                        "identifier": "[DCF[Perpetual growth rate[2015]]]",
                        "period": 2015,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "11d0c409-1bac-4750-b008-1a2c7602bae8",
                        "identifier": "[DCF[Perpetual growth rate[2023]]]",
                        "period": 2023,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "2deb14d5-54b4-4be6-a321-6560469db558",
                        "identifier": "[DCF[Perpetual growth rate[2020]]]",
                        "period": 2020,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "4c254840-34d1-4ab8-a7f8-a341c20d01bb",
                        "identifier": "[DCF[Perpetual growth rate[2016]]]",
                        "period": 2016,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "57c02b53-12d5-4a1f-974b-80ae57a15f65",
                        "identifier": "[DCF[Perpetual growth rate[2021]]]",
                        "period": 2021,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "916034b5-45b1-432c-b679-fad210c7cf6e",
                        "identifier": "[DCF[Perpetual growth rate[2024]]]",
                        "period": 2024,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "9a56d6c7-8d00-449c-a9f6-5ef2ca663f3e",
                        "identifier": "[DCF[Perpetual growth rate[2019]]]",
                        "period": 2019,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                        "value": "0.0089",
                        "formula": "[DCF Drivers[Risk-free rate[2019]]]",
                        "internalFormula":
                        "[DCF Drivers[Risk-free rate[2019]]]",
                        "edges": {
                            "dependantCells": [{
                                "id": "3a6505c6-94be-409b-b4a3-0d9828288cc6",
                                "identifier": "[DCF[Terminal value[2019]]]",
                                "edges": {}
                            }],
                            "precedentCells": [{
                                "id": "feef8220-74b2-41b8-bc44-90be942168bc",
                                "identifier":
                                "[DCF Drivers[Risk-free rate[2019]]]",
                                "edges": {}
                            }]
                        }
                    }, {
                        "id": "bbaf89de-ec33-420b-8875-97463596a5a1",
                        "identifier": "[DCF[Perpetual growth rate[2017]]]",
                        "period": 2017,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "c877948c-49ca-4522-a9e3-f0ef2c43b735",
                        "identifier": "[DCF[Perpetual growth rate[2018]]]",
                        "period": 2018,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "d9ffe308-894e-4bd6-afb0-565e786b709e",
                        "identifier": "[DCF[Perpetual growth rate[2022]]]",
                        "period": 2022,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }]
                }
            }]
        }, {
            "id":
            "16cb1109-d036-4999-b668-0b3faf8728a4",
            "ticker":
            "RBC",
            "startPeriod":
            2019,
            "forecastEndPeriod":
            2024,
            "historicalStartPeriod":
            2015,
            "lineItems": [{
                "id": "b5056240-785f-49e3-a8b0-d1c2ac3b7f75",
                "name": "Perpetual growth rate",
                "order": 20,
                "tags": ["DCF", "Perpetual growth rate (DCF)"],
                "format":
                "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                "edges": {
                    "facts": [{
                        "id": "0abbeb31-5c8c-486a-9e1f-39099a28b70d",
                        "identifier": "[DCF[Perpetual growth rate[2019]]]",
                        "period": 2019,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Percentage\"}",
                        "value": "0.0089",
                        "formula": "[DCF Drivers[Risk-free rate[2019]]]",
                        "internalFormula":
                        "[DCF Drivers[Risk-free rate[2019]]]",
                        "edges": {
                            "dependantCells": [{
                                "id": "e6b095de-7535-416b-9f14-0a51596133b8",
                                "identifier": "[DCF[Terminal value[2019]]]",
                                "edges": {}
                            }],
                            "precedentCells": [{
                                "id": "d04463e0-6b5c-48e3-a7d4-0753aa4fcce7",
                                "identifier":
                                "[DCF Drivers[Risk-free rate[2019]]]",
                                "edges": {}
                            }]
                        }
                    }, {
                        "id": "1ca45251-36db-4337-b4d2-6195438dd69e",
                        "identifier": "[DCF[Perpetual growth rate[2022]]]",
                        "period": 2022,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "2f487957-1c1a-4688-b705-81f5397451c6",
                        "identifier": "[DCF[Perpetual growth rate[2016]]]",
                        "period": 2016,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "3f8e5a7e-42bd-4a52-8bbb-0a28b18d16ce",
                        "identifier": "[DCF[Perpetual growth rate[2021]]]",
                        "period": 2021,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "4f33efca-3f3c-4f4e-9ade-68b00cc3d0be",
                        "identifier": "[DCF[Perpetual growth rate[2018]]]",
                        "period": 2018,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "6152d5fa-06df-44bc-a4b6-d287ec54c2fe",
                        "identifier": "[DCF[Perpetual growth rate[2017]]]",
                        "period": 2017,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "61ef37ec-295b-4c59-8cfb-e3c198c832ed",
                        "identifier": "[DCF[Perpetual growth rate[2015]]]",
                        "period": 2015,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "formula": " ",
                        "edges": {}
                    }, {
                        "id": "96003e6d-838c-46dc-9def-a780284b44fb",
                        "identifier": "[DCF[Perpetual growth rate[2024]]]",
                        "period": 2024,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "f13c816f-57c1-4e79-91e6-4b4d4574d5b9",
                        "identifier": "[DCF[Perpetual growth rate[2020]]]",
                        "period": 2020,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }, {
                        "id": "f8c29b8c-1efa-471c-8b8f-34087e8080e4",
                        "identifier": "[DCF[Perpetual growth rate[2023]]]",
                        "period": 2023,
                        "format":
                        "{\"fontStyle\":\"italic\",\"valFormat\":\"Plain text\"}",
                        "value": "0",
                        "formula": " ",
                        "internalFormula": "0 * 1.1",
                        "edges": {}
                    }]
                }
            }]
        }]
    }
