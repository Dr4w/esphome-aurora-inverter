import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor as _sensor
from . import HUB_CHILD_SCHEMA, CONF_AURORA_MONITOR_ID
from .helpers import (
    CONF_DSP_VALUE_TYPE,  DSP_VALUE_TYPE_SCHEMA,
    CONF_ENERGY_TYPE,     ENERGY_TYPE_SCHEMA,
    CONF_INFO_TYPE,       INFO_TYPE_SCHEMA,
)

DEPENDENCIES = ['aurora_monitor']

# Validate against dynamically parsed enums
CONFIG_SCHEMA = (_sensor.sensor_schema()
    .extend({
        cv.Optional(CONF_DSP_VALUE_TYPE): cv.enum(DSP_VALUE_TYPE_SCHEMA),
        cv.Optional(CONF_ENERGY_TYPE): cv.enum(ENERGY_TYPE_SCHEMA),
        cv.Optional(CONF_INFO_TYPE): cv.enum(INFO_TYPE_SCHEMA),
    })
    .extend(HUB_CHILD_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)

async def to_code(config):
    # grab the hub instance
    hub = await cg.get_variable(config[CONF_AURORA_MONITOR_ID])

    # 1) DSP / measurement sensors
    if CONF_DSP_VALUE_TYPE in config:
        sens = await _sensor.new_sensor(config)
        dsp = config[CONF_DSP_VALUE_TYPE]

        # find the original enum name (e.g. "TEMPERATURE_INVERTER")
        dsp_name = next(
            name for name, member in DSP_VALUE_TYPE_SCHEMA.items()
            if member == dsp
        )

        if dsp_name.startswith('TEMPERATURE'):
            # call register_temperature_sensor for any TEMPERATURE_* value
            cg.add(hub.register_temperature_sensor(sens, dsp))
        else:
            # all other DSP values use the normal register_sensor
            cg.add(hub.register_sensor(sens, dsp))

    # 2) Cumulated energy sensors
    elif CONF_ENERGY_TYPE in config:
        sens = await _sensor.new_sensor(config)
        # registers: void register_cumulative_sensor(sensor::Sensor *sensor, CUMULATED_ENERGY_TYPE type);
        cg.add(hub.register_cumulative_sensor(sens, config[CONF_ENERGY_TYPE]))
