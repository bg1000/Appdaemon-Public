# goodnight

Goodnight is triggered by scanning an NFC tag.  It runs a series of configurable test to make sure the home is in the desired condition for bed.  Currently goodnight supports checking if the attribute if an entity is either equal to (==) or not equal to (!=) a fixed value. If a particular entity is not in the desired state goodnight can optionally run a service to correct this. For example, goodnight can check to see if the alarm is set and set it if needed.  

The number of rechecks is configurable and messaging is provided for overall success/failure as well as failure messages for individual conditions. Each test with a service call has a retry_seconds parameter which determines the minimum time goodnight will wait before a recheck.  After performing all tests goodnight will not start the next recheck until this criteria has been met for all tests that have failed the check. When a recheck is performed all tests are repeated. 

The service calls are optional since not all things may be completely automated. For example I have not (yet) automated loading a tablet in the diswasher and starting it.  In this case goodnight will simply inform me that the dishwasher is not running.

# Dependencies

This app uses app_messenger (avaialable in this repo) to send phone notifications to android phones.

# App parameters

Sample configuration with comments

```yaml
GoodNight:
  module: goodnight
  class: goodnight
  log_level: INFO # optional, default is INFO, any valid python logging level allowed
  log: tags_log # optional, default is main_log, other logs must be defined in appdaemon.yaml before use
  dependecies: app_messenger # make sure app_messenger is available before this app starts
  max_rechecks: 1 # max # times to recheck before sending overall failure message
  overall_failure_message: "Unable to automatically correct all noted problems."
  overall_success_message: "House is ready for bed. Goodnight."
  notification_list: # list of (android) phones to send notifications to
    - mobile_app_bob_phone
    - mobile_app_pat_phone
  tag_ids: # list of tags that will trigger goodnight
    - !secret bob_nightstand
    - !secret bob_nightstand
  tests: # list of tests - will be performed in order
    - entity_id: cover.garage_door
      attribute: "state"
      test: "=="
      value: "closed"
      failure_service_call: "cover/close_cover"
      service_parameters: { "entity_id": "cover.garage_door" }
      service_message: "Closing Garage Door"
      retry_seconds: 20 # min time before recheck
      failure_message: "Garage Door is open"
      final_failure_message: "Unable to close garage door"
    - entity_id: binary_sensor.dishwasher_on
      test: "=="
      value: "on"
      failure_message: "The dishwasher isn't running"
    - entity_id: alarm_control_panel.6617_truxton_lane_alarm_control_panel
      attribute: "state"
      test: "=="
      value: "armed_home"
      failure_service_call: "input_boolean/toggle"
      service_parameters: { "entity_id": "input_boolean.alarm_home" }
      service_message: "Setting alarm to Home mode."
      retry_seconds: 30
      failure_message: "Alarm not sucessfully set"
      final_failure_message: "Unable to set alarm"
    - entity_id: light.garage_light
      attribute: "state"
      test: "=="
      value: "off"
      failure_service_call: "light/turn_off"
      service_parameters: { "entity_id": "light.garage_light" }
      service_message: "Turning off garage light"
      retry_seconds: 2
      failure_message: "Garage light is on"
      final_failure_message: "Unable to turn off garage light."
    - entity_id: light.garage_entry_light
      attribute: "state"
      test: "=="
      value: "off"
      failure_service_call: "light/turn_off"
      service_parameters: { "entity_id": "light.garage_entry_light" }
      service_message: "Turning off garage entry light"
      retry_seconds: 2
      failure_message: "Garage entry light is on"
      final_failure_message: "Unable to turn off garage entry light."
    - entity_id: light.office_light
      attribute: "state"
      test: "=="
      value: "off"
      failure_service_call: "light/turn_off"
      service_parameters: { "entity_id": "light.office_light" }
      service_message: "Turning off office light"
      retry_seconds: 2
      failure_message: "Office light is on"
      final_failure_message: "Unable to turn off office light."
    - entity_id: light.office_lamp
      attribute: "state"
      test: "=="
      value: "off"
      failure_service_call: "light/turn_off"
      service_parameters: { "entity_id": "light.office_lamp" }
      service_message: "Turning off office lamp"
      retry_seconds: 2
      failure_message: "Office lamp is on"
      final_failure_message: "Unable to turn off office light."
    - entity_id: light.kitchen_lights
      test: "=="
      value: "off"
      failure_message: "The kitchen lights are on"
```




