# Commands for PS
# $ uv run esgpull convert ground-based-data/cimp6.txt --graph
# $ uv run esgpull convert ground-based-data/cimp6.txt --out ground-based-data/cimp6_converted.yaml
# $ uv run esgpull add --query-file ground-based-data/cimp6_converted.yaml
# $ uv run esgpull show
# $ uv run esgpull update <id>


CMIP6_VERSION_PROJECT = "input4MIPs"
CMIP6_VERSION_MIP_ERA = "CMIP6"
CMIP6_VERSION_SOURCE_ID = "UoM-CMIP-1-2-0"
CMIP6_VERSION_GRID = "gr1-GMNHSH"
CMIP6_VERSION_FREQUENCY = "yr"
SEARCH_TAG = f"cmip6-global-mean-yearly-{CMIP6_VERSION_SOURCE_ID.lower()}"

!uv run esgpull add --tag {SEARCH_TAG} --track project:{CMIP6_VERSION_PROJECT} mip_era:{CMIP6_VERSION_MIP_ERA} source_id:{CMIP6_VERSION_SOURCE_ID} grid_label:{CMIP6_VERSION_GRID} frequency:{CMIP6_VERSION_FREQUENCY}


