import cdsapi

dataset = "satellite-carbon-dioxide"
request = {
    "processing_level": ["level_3"],
    "variable": "xco2",
    "sensor_and_algorithm": "merged_obs4mips",
    "version": ["4_5"]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
