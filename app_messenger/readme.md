# app_messenger

App_messenger is an appdaemon app that provides centralized notification for (currently android) phones that are running the home assistant companion app.  The configuration of app_messenger includes default values for the notification.  You can use app_messenger in replace or update node.  In replace mode only what you pass in is used and the defaults are not used in any way. In update mode the values you pass in replace the defaults. If no value is passed in the default is used.  For data the items you pass in replace existing defaults or add to them. You may, for example make ``` ttl:0 and priority:high``` part of the default data.  If you call send_message, in update mode, with only an image as part of the data, the notfication will include the image plus the ``` ttl:0 and the priority: high```.  In replace mode the data would only include the image.

# App parameters

Sample configuration with comments

```yaml
app_messenger:
  module: app_messenger
  class: app_messenger
  log_level: DEBUG # optional, default is INFO, any valid python logging level allowed
  log: main_log # optional, default is main_log, other logs must be defined in appdaemon.yaml before use
  device: mobile_app_bob_phone # default phone to notify, parameter must be present but value can be blank
  title: Appdaemon Alert # default message tital, parameter must be present but value can be blank
  message: "This is an message from Appdaemon" # default message, parameter must be present but value can be blank
  data: # default data to include with notification, must be present but can be blank after data or have blank values as shown
    image:
    clickAction:
    ttl: 0
    priority: "high"
```

# Usage

To send a message with app_messenger you call the send_message method which has the following signature:
```send_message(self, replace, **kwargs)```

If replace is True send_message will operate in replace mode as described above.  If replace is False send_message will operate in update mode. Kwargs may optionally include any or all of the following:

- device
- message
- title
- data

If you want to remove a default value from the notification (e.g. - no title), call send_message in replace mode and pass None as the value 

## Example Usage in another appdaemon app

```python
    def initialize(self):
        self.messenger = self.get_app("app_messenger")
        self.device = mobile_app_jim_phone
        self.data = {
            "image": "https://yourdomanin.duckdns.org/local/snapshots/doorbell.jpg",
            "clickAction": "lovelace/front-porch",
        }
        .
        .
        .
    def some_method():
         self.messenger.send_message(
                False,
                device=self.device,
                message="Person on front porch",
                title="Doorbell Notification",
                data=self.data
            )
```

