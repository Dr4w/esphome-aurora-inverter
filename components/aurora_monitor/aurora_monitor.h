// aurora_monitor.h
#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "ABBAurora.h"

namespace esphome {
namespace aurora_monitor {

enum INFO_TYPE {
  CONNECTION_STATUS,
  SYSTEM_PN,
  SYSTEM_SERIAL_NUMBER,
  FIRMWARE_RELEASE
};

struct sensor_dsp {
  sensor::Sensor *sensor;
  DSP_VALUE_TYPE type;
};

struct sensor_text {
  text_sensor::TextSensor *sensor;
  enum INFO_TYPE type;
};

struct sensor_cumulative {
  sensor::Sensor *sensor;
  CUMULATED_ENERGY_TYPE type;
};

class AuroraMonitor : public PollingComponent {
 public:
  AuroraMonitor() : PollingComponent(5000) {}

  static AuroraMonitor *get_instance() {
    static AuroraMonitor instance;
    return &instance;
  }

  void setup() override;
  void update() override;
  void dump_config() override;

  // Configuration setters
  void set_rx_pin(uint8_t rx) { rx_pin_ = rx; }
  void set_tx_pin(uint8_t tx) { tx_pin_ = tx; }
  void set_tx_control_pin(uint8_t ctrl) { tx_control_pin_ = ctrl; }
  void set_address(uint8_t addr) { address_ = addr; }

  // Registration methods
  void register_sensor(sensor::Sensor *sensor, DSP_VALUE_TYPE type);
  void register_temperature_sensor(sensor::Sensor *sensor, DSP_VALUE_TYPE type);
  void register_cumulative_sensor(sensor::Sensor *sensor, CUMULATED_ENERGY_TYPE type);
  void register_text_sensor(text_sensor::TextSensor *sensor, INFO_TYPE type);

protected:
  uint8_t rx_pin_{22};
  uint8_t tx_pin_{21};
  uint8_t tx_control_pin_{26};
  uint8_t address_{2};

  ABBAurora *inverter_{nullptr};
  bool connected_{false};

// Registered sensor entries
  std::vector<sensor_dsp *> sensors_;
  std::vector<sensor_dsp *> temperature_sensors_;
  std::vector<sensor_cumulative *> cumulative_sensors_;
  std::vector<sensor_text *> text_sensors_;
};

}  // namespace aurora_monitor
}  // namespace esphome

