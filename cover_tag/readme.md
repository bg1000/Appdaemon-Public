# cover_tag

Cover_tag listens for an NFC tag to be scanned.  If the defined cover is open when the tag is scanned it will close the cover. If the defined cover is closed it will open it. If the cover is neither open nor closed the scan is ignored.  Cover_tag also accepts an optional list of device id's. If this list is present, the scan must come from a device on the list or it will be ignored. My personal use case for this is opening and closing the garage door base on scanning a tag located on the outside of the garage.

# App parameters

Sample configuration with comments

```
CoverEntityScanned:
  module: cover_tag
  class: cover_tag_scanned
  log_level: INFO # optional, default is INFO, any valid python logging level allowed
  log: tags_log # optional, default is main_log, other logs must be defined in appdaemon.yaml before use
  tag_id: !secret tag1 # this is the tag you and/or home assistant assigned when you set up the tag
  cover_entity: cover.garage_door name of the cover you want to control
  devices: # this section is option
    - !secret bob_phone # each phone reports a unique id when you scan a tag
    - !secret pat_phone
```
_Note: If you don't know the tag or device id you can set the log_level to DEBUG, scan a tag and retrieve the values from the log._



