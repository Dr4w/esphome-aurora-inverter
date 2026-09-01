import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor as _text_sensor
from . import HUB_CHILD_SCHEMA, CONF_AURORA_MONITOR_ID
from .helpers import (
    CONF_INFO_TYPE,       INFO_TYPE_SCHEMA,
)

DEPENDENCIES = ['aurora_monitor']

# Validate against dynamically parsed enums
CONFIG_SCHEMA = (_text_sensor.text_sensor_schema()
    .extend({
        cv.Optional(CONF_INFO_TYPE): cv.enum(INFO_TYPE_SCHEMA),
    })
    .extend(HUB_CHILD_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)

async def to_code(config):
    # grab the hub instance
    hub = await cg.get_variable(config[CONF_AURORA_MONITOR_ID])

    # 3) Text‐sensor info items
    if CONF_INFO_TYPE in config:
        text = await _text_sensor.new_text_sensor(config)
        # registers: void register_text_sensor(text_sensor::TextSensor *sensor, INFO_TYPE type);
        cg.add(hub.register_text_sensor(text, config[CONF_INFO_TYPE]))
