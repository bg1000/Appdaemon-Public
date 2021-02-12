import hassapi as hass  # pylint: disable=import-error


class auto_light(hass.Hass):
    def initialize(self):
        self.handle = None
        for entity in self.args["OnEntities"]:
            self.listen_state(self.light_on, entity["entity_id"], new=entity["state"])
            self.log(
                "Listening for " + entity["entity_id"] + ".state = " + entity["state"],
                level="DEBUG",
            )
        self.listen_state(
            self.enable_auto,
            self.args["EnableOffEntity"],
            old=self.args["EnableOffEnableState"],
            new=self.args["EnableOffDisableState"],
        )
        self.listen_state(
            self.disable_auto,
            self.args["EnableOffEntity"],
            old=self.args["EnableOffDisableState"],
            new=self.args["EnableOffEnableState"],
        )

    def light_on(self, entity, attribute, old, new, kwargs):
        self.log(
            "Turning on "
            + str(self.args["LightEntity"])
            + " due to motion or door opening.",
            level="INFO",
        )
        if self.handle is not None:
            self.cancel_timer(self.handle)
            self.handle = None
        self.call_service("light/turn_on", entity_id=self.args["LightEntity"])
        if (
            self.get_state(self.args["EnableOffEntity"])
            == self.args["EnableOffEnableState"]
        ):
            self.handle = self.run_in(
                self.light_off, self.args["OnTimeMin"] * 60, **kwargs
            )

    def light_off(self, kwargs):
        if (
            self.get_state(self.args["EnableOffEntity"])
            == self.args["EnableOffEnableState"]
        ):
            for entity in self.args["OffEntities"]:
                if self.get_state(entity["entity_id"]) != entity["state"]:
                    return
            self.log("Turning off " + str(self.args["LightEntity"]) + ".", level="INFO")
            self.call_service("light/turn_off", entity_id=self.args["LightEntity"])

    def enable_auto(self, entity, attribute, old, new, kwargs):
        if self.handle is not None:
            self.cancel_timer(self.handle)
        self.handle = self.run_in(self.light_off, self.args["OnTimeMin"] * 60, **kwargs)

    def disable_auto(self, entity, attribute, old, new, kwargs):
        if self.handle is not None:
            self.cancel_timer(self.handle)
            self.handle = None
