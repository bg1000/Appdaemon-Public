# battery_minder

When it comes to battery operated devices I'm not interested in checking battery levels. I would rather have the automation system alert me if battery needs to be replaced.  I also don't want to have to maintain some list of devices that have batteries and add them to some kind of automation.  I want more of a "set it and forget it" approach. Battery-minder searches all entities in home assistant to find batteries and monitors them.  It can search both for battery related entities and attributes of entities.  The search criteria is based on regular expressions.  In the sample configuration shown below battery minder will search for any entity that has an attribute named "battery_level" or any entity that has an entity_id that starts with "sensor" and also contains the text "battery_level".

You may define a warning level and urgent level. Battery minder makes a list of entities/attributes and compares them to these levels. It will send the appropriate alert when battery level drop below the warning or urgent level. Levels can be checked in multiple ways depending on your preferences:
- Instant notification: monitor the entity/attribute for any changes. When it changes compare to defined levels and alert as appropriate.
- Timed notification: you may define one or more times per day you want battery minder to check batteries for you.
- manual scan: you may define an entity that battery_minder will monitor. When the entity state changes batteries will be scanned. This allowd you to trigger the scan from the front end, from an automation, etc.

# Dependencies

This app uses app_messenger (avaialable in this repo) to send phone notifications to android phones.

# App parameters

Sample configuration with comments

```
BatteryCheck:
  module: battery_minder
  class: battery_minder
  log_level: DEBUG # optional, default is INFO, any valid python logging level allowed
  log: main_log # optional, default is main_log, other logs must be defined in appdaemon.yaml before use
  manual_scan: input_boolean.battery_scan # optional - if defined will trigger a scan on state change
  warning_level: 99 # integer
  urgent_level: 85 #
  instant_notification: True # if true will provide notification as soon as state is below defined levels.
  ignore_unknown: False # if False batter_minder will notify you if it gets an invalid reading like 'unknown' for an entity/attribute
  max_notification_frequency: 10 # in minutes - limits the maximum frequency of notifications
  included_entities: # set your search criteria here - these are regex
    - entity_id: ".*" # if entity and attribute are provided both must match
      attribute: "battery_level"
    - entity_id: "^sensor.*battery_level*"
  excluded_entities: # these are specific entities that you don't want to get notifications for
    - vacuum.rosie
    - sensor.sm_g950u_battery_level
    - sensor.vacuum_rosie_battery_level
  non_numeric_checks: # these non-numeric values will trigger a notification
    - low
    - lo
  report_if_charging: False # if the reading is higher than last time battery_minder assumes the battery is charging, optionally ignore
  run_times: # use HH:MM:SS in 24 hour format e.g. "08:00:00"
    - "08:00:00"
    - "12:00:00"
  persistent_notification: true # set to true if you want a persistent notification in the front end
  phones: # list of phones to notify - can be empty
    - mobile_app_bob_phone
  notification_color: red # this is the color of the mobile notification, red is default
```




