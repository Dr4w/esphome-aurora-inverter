# helpers.py
# Shared utility code for aurora_monitor component

import os
import re
import esphome.codegen as cg

# Paths to C++ headers for dynamic enum parsing
BASE = os.path.abspath(os.path.dirname(__file__))
ENUM_FILE = os.path.join(BASE, 'ABBAuroraEnums.h')
HUB_HEADER = os.path.join(BASE, 'aurora_monitor.h')

# Utility to parse any C++ enum by name
def parse_enum(enum_name, file_path):
    text = open(file_path, 'r').read()
    pattern = rf'enum\s+{enum_name}\s*\{{([^}}]+)\}}'
    m = re.search(pattern, text)
    if not m:
        return []
    values = []
    for line in m.group(1).splitlines():
        line = line.strip().rstrip(',')
        if '=' in line:
            values.append(line.split('=')[0].strip())
    return values

# Dynamic lists for schemas
DSP_VALUES = parse_enum('DSP_VALUE_TYPE', ENUM_FILE)
ENERGY_TYPES = parse_enum('CUMULATED_ENERGY_TYPE', ENUM_FILE)

INFO_TYPES = [
    'CONNECTION_STATUS',
    'SYSTEM_PN',
    'SYSTEM_SERIAL_NUMBER',
    'FIRMWARE_RELEASE',
]

global_ns = cg.global_ns
aurora_monitor_ns = cg.esphome_ns.namespace('aurora_monitor')

# 1) Create the CodegenEnum objects
DSP_VALUE_TYPE        = global_ns.enum('DSP_VALUE_TYPE', DSP_VALUES)
CUMULATED_ENERGY_TYPE = global_ns.enum('CUMULATED_ENERGY_TYPE', ENERGY_TYPES)
INFO_TYPE             = aurora_monitor_ns.enum('INFO_TYPE', INFO_TYPES)

# 2) Build Python dicts for cv.enum
DSP_VALUE_TYPE_SCHEMA = {name: getattr(DSP_VALUE_TYPE, name) for name in DSP_VALUES}
ENERGY_TYPE_SCHEMA    = {name: getattr(CUMULATED_ENERGY_TYPE, name) for name in ENERGY_TYPES}
INFO_TYPE_SCHEMA      = {name: getattr(INFO_TYPE, name) for name in INFO_TYPES}

# 3) Config keys
CONF_DSP_VALUE_TYPE  = 'dsp_value_type'
CONF_ENERGY_TYPE     = 'energy_type'
CONF_INFO_TYPE       = 'info_type'
