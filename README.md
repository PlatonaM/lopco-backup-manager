#### /backups

**GET**

_List all backups._

    # Example
    
    curl http://<host>/backups
    [
        {
            "name": "export-2020-11-10T07:52:20.712702Z",
            "time": "2020-11-10T07:52:20.712702Z",
            "size": 8127
        },
        {
            "name": "export-2020-11-09T11:06:45.307337Z",
            "time": "2020-11-09T11:06:45.307337Z",
            "size": 8523
        },
        {
            "name": "import-2020-11-09T11:00:50.780737Z",
            "time": "2020-11-09T11:00:50.780737Z",
            "size": 8523
        },
        {
            "name": "export-2020-11-06T12:36:40.620706Z",
            "time": "2020-11-06T12:36:40.620706Z",
            "size": 8509
        }
    ]

**PATCH**

_Create a backup._

    # Example
    
    curl -X PATCH http://<host>/backups

**POST**

_Import a backup._
    
    # Example
    
    cat backup.json
    {
        "http://pipeline-registry/pipelines": {
            "677f99d4-2ec7-450c-add2-8b7c5f7f171c": {
                "name": "No upload test",
                "stages": {
                    "0": {
                        "worker": {
                            "name": "XLSX to CSV",
                            "image": "platonam/lopco-xlsx-to-csv-worker:dev",
                            "data_cache_path": "/data_cache",
                            "description": "Convert a Microsoft Excel Open XML Spreadsheet file to Comma-Separated Values.",
                            "configs": {
                                "delimiter": ";"
                            },
                            "input": {
                                "type": "single",
                                "fields": [
                                    {
                                        "name": "xlsx_file",
                                        "media_type": "application/vnd.ms-excel",
                                        "is_file": true
                                    }
                                ]
                            },
                            "output": {
                                "type": "single",
                                "fields": [
                                    {
                                        "name": "csv_file",
                                        "media_type": "text/csv",
                                        "is_file": true
                                    },
                                    {
                                        "name": "line_count",
                                        "media_type": "text/plain",
                                        "is_file": false
                                    }
                                ]
                            },
                            "id": "1567e155-51c6-4f0b-a898-842c737f1b34"
                        },
                        "description": "convert xlsx to csv",
                        "input_map": {
                            "xlsx_file": "init_source"
                        }
                    },
                    "1": {
                        "worker": {
                            "name": "Trim CSV",
                            "image": "platonam/lopco-trim-csv-worker:dev",
                            "data_cache_path": "/data_cache",
                            "description": "Trim a column from a Comma-Separated Values file.",
                            "configs": {
                                "delimiter": ";",
                                "column_num": "2"
                            },
                            "input": {
                                "type": "single",
                                "fields": [
                                    {
                                        "name": "input_csv",
                                        "media_type": "text/csv",
                                        "is_file": true
                                    }
                                ]
                            },
                            "output": {
                                "type": "single",
                                "fields": [
                                    {
                                        "name": "output_csv",
                                        "media_type": "text/csv",
                                        "is_file": true
                                    },
                                    {
                                        "name": "line_count",
                                        "media_type": "text/plain",
                                        "is_file": false
                                    }
                                ]
                            },
                            "id": "04e6b617-fff1-41bb-a50c-8c2a2c0413e5"
                        },
                        "description": "remove index",
                        "input_map": {
                            "input_csv": "csv_file"
                        }
                    },
                    "2": {
                        "worker": {
                            "name": "Split CSV",
                            "image": "platonam/lopco-split-csv-worker:dev",
                            "data_cache_path": "/data_cache",
                            "description": "Split a Comma-Separated Values file into multiple unique files.",
                            "configs": {
                                "column": "sensor",
                                "delimiter": ";"
                            },
                            "input": {
                                "type": "single",
                                "fields": [
                                    {
                                        "name": "source_table",
                                        "media_type": "text/csv",
                                        "is_file": true
                                    }
                                ]
                            },
                            "output": {
                                "type": "multiple",
                                "fields": [
                                    {
                                        "name": "unique_id",
                                        "media_type": "text/plain",
                                        "is_file": false
                                    },
                                    {
                                        "name": "result_table",
                                        "media_type": "text/csv",
                                        "is_file": true
                                    },
                                    {
                                        "name": "line_count",
                                        "media_type": "text/plain",
                                        "is_file": false
                                    }
                                ]
                            },
                            "id": "004894dc-bb03-4649-92c4-6b184c30c594"
                        },
                        "description": "split into modules",
                        "input_map": {
                            "source_table": "output_csv"
                        }
                    }
                }
            }
        },
        "http://machine-registry/machines": {},
        "http://worker-registry/workers": {
            "004894dc-bb03-4649-92c4-6b184c30c594": {
                "name": "Split CSV",
                "image": "platonam/lopco-split-csv-worker:latest",
                "data_cache_path": "/data_cache",
                "description": "Split a Comma-Separated Values file into multiple unique files.",
                "configs": {
                    "column": null,
                    "delimiter": null
                },
                "input": {
                    "type": "single",
                    "fields": [
                        {
                            "name": "source_table",
                            "media_type": "text/csv",
                            "is_file": true
                        }
                    ]
                },
                "output": {
                    "type": "multiple",
                    "fields": [
                        {
                            "name": "unique_id",
                            "media_type": "text/plain",
                            "is_file": false
                        },
                        {
                            "name": "result_table",
                            "media_type": "text/csv",
                            "is_file": true
                        },
                        {
                            "name": "line_count",
                            "media_type": "text/plain",
                            "is_file": false
                        }
                    ]
                }
            },
            "1567e155-51c6-4f0b-a898-842c737f1b34": {
                "name": "XLSX to CSV",
                "image": "platonam/lopco-xlsx-to-csv-worker:latest",
                "data_cache_path": "/data_cache",
                "description": "Convert a Microsoft Excel Open XML Spreadsheet file to Comma-Separated Values.",
                "configs": {
                    "delimiter": null
                },
                "input": {
                    "type": "single",
                    "fields": [
                        {
                            "name": "xlsx_file",
                            "media_type": "application/vnd.ms-excel",
                            "is_file": true
                        }
                    ]
                },
                "output": {
                    "type": "single",
                    "fields": [
                        {
                            "name": "csv_file",
                            "media_type": "text/csv",
                            "is_file": true
                        },
                        {
                            "name": "line_count",
                            "media_type": "text/plain",
                            "is_file": false
                        }
                    ]
                }
            },
            "04e6b617-fff1-41bb-a50c-8c2a2c0413e5": {
                "name": "Trim CSV",
                "image": "platonam/lopco-trim-csv-worker:latest",
                "data_cache_path": "/data_cache",
                "description": "Trim a column from a Comma-Separated Values file.",
                "configs": {
                    "delimiter": null,
                    "column_num": null
                },
                "input": {
                    "type": "single",
                    "fields": [
                        {
                            "name": "input_csv",
                            "media_type": "text/csv",
                            "is_file": true
                        }
                    ]
                },
                "output": {
                    "type": "single",
                    "fields": [
                        {
                            "name": "output_csv",
                            "media_type": "text/csv",
                            "is_file": true
                        },
                        {
                            "name": "line_count",
                            "media_type": "text/plain",
                            "is_file": false
                        }
                    ]
                }
            }
        },
        "http://protocol-adapter-registry/protocol-adapters": {
            "5e674298-49d5-4723-926c-cf062dd9c141": {
                "name": "HTTP Protocol Adapter",
                "image": "platonam/lopco-http-protocol-adapter:latest",
                "data_cache_path": "/data_cache",
                "description": "Upload files via HTTP.",
                "configs": {
                    "CONF_LOGGER_LEVEL": "info"
                },
                "ports": [
                    {
                        "port": 80,
                        "protocol": "tcp"
                    }
                ]
            }
        }
    }
    
    curl \
    -d @backup.json \
    -X POST http://<host>/backups

#### /backups/{backup}

**GET**

_Download a backup._

    # Example

    curl -O -J http://<host>/backups/export-2020-11-10T07:52:20.712702Z
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  8127  100  8127    0     0   721k      0 --:--:-- --:--:-- --:--:--  721k
    curl: Saved to filename 'export-2020-11-10T07-52-20.712702Z.json'
