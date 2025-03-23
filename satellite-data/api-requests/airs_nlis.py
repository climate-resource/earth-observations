import cdsapi

dataset = "satellite-carbon-dioxide"
request = {
    "processing_level": ["level_2"],
    "variable": "co2",
    "sensor_and_algorithm": "airs_nlis",
    "year": [
        "2003", "2004", "2005",
        "2006", "2007"
    ],
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "version": ["3_0"]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
