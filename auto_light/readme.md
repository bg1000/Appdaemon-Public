# auto_light

As the name implies auto_light is for automatic lighting control.  It can perform basic motion controlled light with some extra features. You may specifiy an arbitrary number of entities and states that will turn on the light.  This might, for example, be three motion detectors, or a motion detector and a door switch.  You may also specify an arbitrary number of entoties and states that must be true for the light to turn off. You may also optionally specify an entity and state which enables/disbles automatically turning off the light. This allows you to enable and disable auto shut off from the front end or through another automation.

## Example use case

My garage light turns on if motion is detected or if either the interior or exterior garage door opens. If the alloted time passes the light will turn off if no motion is detected. If I am seated at my workbench in the garage I will not trigger the motion detector so I disable the auto turn off feature via the home assistant front end.

# Dependencies

This app uses app_messenger (avaialable in this repo) to send phone notifications to android phones.

# App parameters

Sample configuration with comments

```
GarageMotion:
  module: auto_light
  class: auto_light
  log_level: DEBUG # optional, default is INFO, any valid python logging level allowed
  log: main_log # optional, default is main_log, other logs must be defined in appdaemon.yaml before use
  OnEntities: # list of entities and states that will turn on the light - This is a boolean OR
    - entity_id: binary_sensor.garage_motion_1
      state: "on" # quoted so it doesn't parse as boolean
    - entity_id: binary_sensor.wyzesense_779c130a
      state: "on"
    - entity_id: cover.garage_cover
      state: "opening"
  OffEntities: # list of entities and states that must be met for the light to auto turn off - This is a boolean AND
    - entity_id: binary_sensor.garage_motion_1
      state: "off"
  EnableOffEntity: input_boolean.enable_garage_light # entity to determine if auto turn off is enabled
  EnableOffEnableState: "on"
  EnableOffDisableState: "off"
  LightEntity: light.garage_light # light entity
  OnTimeMin: 4 # length of timer, in minutes
```




