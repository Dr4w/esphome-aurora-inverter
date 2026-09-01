import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

# Allow multiple hub definitions
MULTI_CONF = True
CONF_AURORA_MONITOR_ID = 'aurora_monitor_id'

cg.add_library("Wire", None)

# C++ namespace and class for the hub
aurora_monitor_ns = cg.esphome_ns.namespace('aurora_monitor')
AuroraMonitor = aurora_monitor_ns.class_('AuroraMonitor', cg.Component)

# Schema for child sensors/text sensors
HUB_CHILD_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_AURORA_MONITOR_ID): cv.use_id(AuroraMonitor),
})

# Schema for the hub itself
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AuroraMonitor),
    cv.Optional('rx_pin'): cv.int_,
    cv.Optional('tx_pin'): cv.int_,
    cv.Optional('tx_control_pin'): cv.int_,
    cv.Optional('address'): cv.int_,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    # Instantiate hub
    var = cg.new_Pvariable(config[CONF_ID])
    # Register as a component
    await cg.register_component(var, config)
    # Apply optional settings
    if 'rx_pin' in config:
        cg.add(var.set_rx_pin(config['rx_pin']))
    if 'tx_pin' in config:
        cg.add(var.set_tx_pin(config['tx_pin']))
    if 'tx_control_pin' in config:
        cg.add(var.set_tx_control_pin(config['tx_control_pin']))
    if 'address' in config:
        cg.add(var.set_address(config['address']))

