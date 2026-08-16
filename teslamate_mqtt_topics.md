| Topic | Name | Device class | State class | Icon | Unit | Value template | Notes |
|---|---|---|---|---|---|---|---|
| `active_route_destination` |  |  |  |  |  |  | Deprecated by TeslaMate and ignored. The Active Route Destination sensor is derived from the `destination` field in the `active_route` JSON topic instead. |
| `active_route_latitude` |  |  |  |  |  |  | Deprecated by TeslaMate and ignored. The Active Route Location device tracker is derived from the `location.latitude` field in the `active_route` JSON topic instead. |
| `active_route_longitude` |  |  |  |  |  |  | Deprecated by TeslaMate and ignored. The Active Route Location device tracker is derived from the `location.longitude` field in the `active_route` JSON topic instead. |
| `active_route` | `Active Route` |  |  | `mdi:map-marker` |  | Parse the JSON payload into the active-route entities described below. Expose `miles_to_arrival` unchanged with miles as its native unit so Home Assistant can convert it to the user's preferred distance unit. | The derived entities are unavailable until valid JSON without an `error` value is received. |
| `battery_level` | `Battery` | `battery` | `measurement` |  | `%` |  |  |
| `center_display_state` | `Center Display` |  |  | `mdi:television` |  | For a Home Assistant Tesla `center_display_state` sensor, treat `vehicle_state.center_display_state` as an integer enum describing what the vehicle’s center display is currently showing or doing. Known values are: `0` means the center display is off. `2` means the display is on in standby, and may also represent Camp Mode. `3` means the display is on and showing the charging screen. `4` means the display is on in the general/default state. `5` means the display is on and showing the large charging screen. `6` means the display is on and ready to unlock. `7` means Sentry Mode. `8` means Dog Mode. `9` means Media. Value `1` is not documented in the sources I found, so preserve it as unknown rather than guessing. For future safety, any unrecognized integer should map to an unknown/unmapped state while retaining the raw value as an attribute. |  |
| `charge_current_request_max` | `Charge Current Request (Max)` | `current` | `measurement` |  | `A` | Use zero digits of precision |  |
| `charge_current_request` | `Charge Current Request` | `current` | `measurement` |  | `A` | Use zero digits of precision |  |
| `charge_energy_added` | `Energy Added` | `energy` | `total_increasing` |  | `kWh` | Use one digit of precision | |
| `charge_limit_soc` | `Charge Limit` |  | `measurement` | `mdi:battery-charging-90` | `%` | Use zero digits of precision |  |
| `charge_port_door_open` | `Charge Port` | `door` |  | `mdi:ev-plug-tesla` |  |  |  |
| `charger_actual_current` | `Charger Current` | `current` | `measurement` |  | `A` | Use zero digits of precision |  |
| `charger_phases` | `Charger Phases` |  | `measurement` | `mdi:sine-wave` | `phases` | Use zero digits of precision |  |
| `charger_power` | `Charger Power` | `power` | `measurement` |  | `kW` | Use zero digits of precision |  |
| `charger_voltage` | `Charger Voltage` | `voltage` | `measurement` |  | `V` | Use zero digits of precision |  |
| `charging_state` | `Charging State` |  |  | `mdi:ev-station` |  | Preserve the TeslaMate charging state as a human-readable string, but split camel-case words into space-separated words. For example, `NoPower` should display as `No Power`. | |
| `climate_keeper_mode` | `Climate Keeper` |  |  | `mdi:air-conditioner` |  | Preserve the TeslaMate climate keeper mode as a human-readable string, but title case the value. | |
| `display_name` | `Display Name` |  |  | `mdi:form-textbox` |  |  | Used as the Home Assistant config entry title and device name. Also exposed as a diagnostic sensor that is disabled by default. |
| `doors_open` | `Doors` | `door` |  | `mdi:car-door` |  |  |  |
| `download_perc` | `Software Update Download` |  | `measurement` | `mdi:download` | `%` | Use zero digits of precision | Exposed as a diagnostic sensor that is disabled by default. |
| `driver_front_door_open` | `Door (Driver Front)` | `door` |  | `mdi:car-door` |  |  |  |
| `driver_front_window_open` | `Window (Driver Front)` | `window` |  | `mdi:car-door` |  |  |  |
| `driver_rear_door_open` | `Door (Driver Rear)` | `door` |  | `mdi:car-door` |  |  |  |
| `driver_rear_window_open` | `Window (Driver Rear)` | `window` |  | `mdi:car-door` |  |  |  |
| `elevation` | `Elevation` | `distance` | `measurement` | `mdi:image-filter-hdr` | `m` | Use zero digits of precision |  |
| `est_battery_range_km` | `Range (Estimated)` | `distance` | `measurement` | `mdi:map-marker-distance` | `km` | Use zero digits of precision | |
| `exterior_color` | `Exterior Color` |  |  | `mdi:format-color-fill` |  | Preserve the TeslaMate exterior color as a human-readable string, but split camel-case words into space-separated words. For example, `DeepBlue` should display as `Deep Blue`. |  |
| `frunk_open` | `Frunk` | `door` |  | `mdi:car` |  |  |  |
| `geofence` | `Geofence` |  |  | `mdi:earth` |  |  |  |
| `heading` | `Heading` |  | `measurement` | `mdi:compass` | `°` | Use zero digits of precision |  |
| `healthy` | `Health` | `problem` |  | `mdi:heart-pulse` |  | Treat the TeslaMate healthy value as a Home Assistant problem binary sensor. Because TeslaMate publishes `true` when there are no problems and `false` when there are problems, invert the value so `true` reports off/no problem and `false` reports on/problem. |  |
| `ideal_battery_range_km` | `Range (Ideal)` | `distance` | `measurement` | `mdi:map-marker-distance` | `km` | Use zero digits of precision | |
| `inside_temp` | `Temperature (Inside)` | `temperature` | `measurement` |  | `°C` | Use one digit of precision |  |
| `install_perc` | `Software Update Installation` |  | `measurement` | `mdi:update` | `%` | Use zero digits of precision | Exposed as a diagnostic sensor that is disabled by default. |
| `is_climate_on` | `Climate` | `running` |  | `mdi:air-conditioner` |  |  |  |
| `is_preconditioning` | `Preconditioning` | `running` |  | `mdi:air-conditioner` |  |  |  |
| `is_user_present` | `Occupancy` | `occupancy` |  | `mdi:account` |  |  |  |
| `latitude` | `Latitude` |  | `measurement` | `mdi:latitude` | `°` |  | Used by the device tracker. Also exposed as a sensor that is disabled by default. |
| `location` | `Location` |  |  | `mdi:car` |  |  | The device tracker builds its location from latitude and longitude instead of this topic. Also exposed as a sensor that is disabled by default. |
| `locked` | `Lock` | `lock` |  |  |  | Treat the TeslaMate locked value as a Home Assistant lock binary sensor. Because TeslaMate publishes `true` when the car is locked and `false` when the car is unlocked, invert the value so `true` reports off/locked and `false` reports on/unlocked. |  |
| `longitude` | `Longitude` |  | `measurement` | `mdi:longitude` | `°` |  | Used by the device tracker. Also exposed as a sensor that is disabled by default. |
| `model` | `Model` |  |  | `mdi:form-textbox` |  | Prefix the legacy model codes `S`, `X`, `3`, and `Y` with `Model`. Preserve other names, such as `Cybertruck`, without a prefix. | Used as part of the Home Assistant device model. Also exposed as a diagnostic sensor that is disabled by default. |
| `odometer` | `Odometer` | `distance` | `total_increasing` | `mdi:counter` | `km` | Use zero digits of precision |  |
| `outside_temp` | `Temperature (Outside)` | `temperature` | `measurement` |  | `°C` | Use one digit of precision |  |
| `passenger_front_door_open` | `Door (Passenger Front)` | `door` |  | `mdi:car-door` |  |  |  |
| `passenger_front_window_open` | `Window (Passenger Front)` | `window` |  | `mdi:car-door` |  |  |  |
| `passenger_rear_door_open` | `Door (Passenger Rear)` | `door` |  | `mdi:car-door` |  |  |  |
| `passenger_rear_window_open` | `Window (Passenger Rear)` | `window` |  | `mdi:car-door` |  |  |  |
| `plugged_in` | `Plug` | `plug` |  |  |  |  |  |
| `power` | `Power` | `power` | `measurement` |  | `kW` | Use zero digits of precision |  |
| `rated_battery_range_km` | `Range (Rated)` | `distance` | `measurement` | `mdi:map-marker-distance` | `km` | Use zero digits of precision | |
| `scheduled_charging_start_time` | `Charging Start Time` | `timestamp` |  |  |  | Parse the value as a timestamp and use it as-is. |  |
| `sentry_mode` | `Sentry Mode` | `running` |  | `mdi:cctv` |  |  |  |
| `service_mode` | `Service Mode` |  |  | `mdi:wrench` |  |  |  |
| `shift_state` | `Shift State` |  |  | `mdi:car-shift-pattern` |  |  |  |
| `since` | `Last Seen` | `timestamp` |  | `mdi:timer-sand` |  | Parse the value as a timestamp and use it as-is. |  |
| `software_update` | `Update` | `firmware` |  |  |  | Parse the JSON payload and use `installed_version` and `latest_version` as the corresponding properties of the update entity. | Exposed as a diagnostic update entity. |
| `speed` | `Speed` | `speed` | `measurement` | `mdi:speedometer` | `km/h` | Use zero digits of precision |  |
| `spoiler_type` | `Spoiler Type` |  |  | `mdi:weather-windy` |  | Split camel-case words into space-separated words. Append the formatted value to the Home Assistant device model as a parenthetical detail suffixed with `Spoiler`, unless the value is `none`. | Used as part of the Home Assistant device model. Also exposed as a diagnostic sensor that is disabled by default. |
| `state` | `State` |  |  | `mdi:car-connected` |  | Preserve the TeslaMate vehicle state as a human-readable string, but title case the value. |  |
| `sun_roof_installed` | `Sunroof Installed` |  |  | `mdi:car-convertible` |  | When the value is `true`, append `Sunroof` to the Home Assistant device model details. | Also exposed as a diagnostic binary sensor. |
| `sun_roof_percent_open` | `Sunroof Open` |  | `measurement` | `mdi:car-convertible` | `%` | Use zero digits of precision |  |
| `sun_roof_state` | `Sunroof State` |  |  | `mdi:car-convertible` |  | Preserve the TeslaMate sunroof state as a human-readable string by replacing underscores with spaces and title casing the value. |  |
| `time_to_full_charge` | `Charging Time Remaining` | `duration` | `measurement` | `mdi:timer` | `h` |  |  |
| `tpms_pressure_fl` | `Tire Pressure (Front Left)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_pressure_fr` | `Tire Pressure (Front Right)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_pressure_rl` | `Tire Pressure (Rear Left)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_pressure_rr` | `Tire Pressure (Rear Right)` | `pressure` | `measurement` | `mdi:gauge` | `bar` | Use one digit of precision |  |
| `tpms_soft_warning_fl` | `Tire Soft (Front Left)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `tpms_soft_warning_fr` | `Tire Soft (Front Right)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `tpms_soft_warning_rl` | `Tire Soft (Rear Left)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `tpms_soft_warning_rr` | `Tire Soft (Rear Right)` | `problem` |  | `mdi:car-tire-alert` |  |  |  |
| `trim_badging` | `Trim Badging` |  |  | `mdi:form-textbox` |  |  | Used as part of the Home Assistant device model. Also exposed as a diagnostic sensor that is disabled by default. |
| `trunk_open` | `Trunk` | `door` |  | `mdi:car` |  |  |  |
| `update_available` | `Update Available` | `firmware` |  |  |  |  | Exposed as a diagnostic sensor that is disabled by default. |
| `update_version` | `Update Version` | `firmware` |  |  |  |  | Exposed as a diagnostic sensor that is disabled by default. |
| `usable_battery_level` | `Usable Battery` | `battery` | `measurement` |  | `%` |  |  |
| `version` | `Version` |  |  | `mdi:numeric` |  |  | Used as the Home Assistant device software version. Also exposed as a diagnostic sensor that is disabled by default. |
| `wheel_type` | `Wheel Type` |  |  | `mdi:tire` |  | Treat the TeslaMate wheel type as a compact string made from a camel-case wheel name, digits for the wheel size, and an optional alphabetic suffix. Split the camel-case name and suffix into space-separated words, place spaces around the size, and append a double quote to the size. Append the formatted value to the Home Assistant device model as a parenthetical detail suffixed with `Wheels`. For example, `SonicCarbonTwinTurbine19` should contribute `Sonic Carbon Twin Turbine 19" Wheels`, while `Slipstream19Carbon` should contribute `Slipstream 19" Carbon Wheels`. | Used as part of the Home Assistant device model. Also exposed as a diagnostic sensor that is disabled by default. |
| `windows_open` | `Windows` | `window` |  | `mdi:car-door` |  |  |  |

## Active routes

The integration derives six enabled-by-default entities from the single `active_route` JSON topic:

- **Active Route Destination** is a sensor containing `destination`.
- **Active Route Energy At Arrival** is a battery sensor containing `energy_at_arrival` in percent.
- **Active Route Distance To Arrival** is a distance sensor containing `miles_to_arrival` with a native unit of miles. Home Assistant converts it to the user's configured distance unit for display.
- **Active Route Minutes To Arrival** is a duration sensor containing `minutes_to_arrival` in minutes.
- **Active Route Traffic Minutes Delay** is a duration sensor containing `traffic_minutes_delay` in minutes.
- **Active Route Location** is a GPS device tracker using `location.latitude` and `location.longitude`.

A payload such as `{"error": "No active route available"}` makes all six entities unavailable. Missing or malformed JSON also leaves them unavailable. When the route itself is valid but an individual field is absent, the corresponding entity has an unknown state.

The deprecated `active_route_destination`, `active_route_latitude`, and `active_route_longitude` MQTT topics are not read; all active-route state comes from the JSON topic.
