# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---


# Commands for PS
# $ uv run esgpull convert ground-based-data/cimp6.txt --graph
# $ uv run esgpull convert ground-based-data/cimp6.txt --out ground-based-data/cimp6_converted.yaml
# $ uv run esgpull add --query-file ground-based-data/cimp6_converted.yaml
# $ uv run esgpull show
# $ uv run esgpull update <id>

# %%
CMIP6_VERSION_PROJECT = "input4MIPs"
CMIP6_VERSION_MIP_ERA = "CMIP6Plus"
CMIP6_VERSION_SOURCE_ID = "UoM-CMIP-1-2-0"
#CMIP6_VERSION_GRID = "gr1-GMNHSH"
CMIP6_VERSION_FREQUENCY = "yr"
CIMP6_VARIABLE_ID = "co2"
SEARCH_TAG = f"cmip6-global-mean-yearly-{CMIP6_VERSION_SOURCE_ID.lower()}"

# %% [markdown]
# add data

# %%
!uv run esgpull add --tag {SEARCH_TAG} --track project:{CMIP6_VERSION_PROJECT} mip_era:{CMIP6_VERSION_MIP_ERA} source_id:{CMIP6_VERSION_SOURCE_ID} frequency:{CMIP6_VERSION_FREQUENCY} variable_id:{CIMP6_VARIABLE_ID}

# %%
!esgpull update -y --tag {SEARCH_TAG} -X utf8