import hassapi as hass  # pylint: disable=import-error
import re
import datetime


class battery_minder(hass.Hass):
    def initialize(self):
        self.messenger = self.get_app("app_messenger")
        if "manual_scan" in self.args:
            self.listen_state(self.scan_for_batteries, self.args["manual_scan"])
        self.notification_color = (
            self.args["notification_color"]
            if "notification_color" in self.args
            else "red"
        )
        self.scan_items = []
        if "run_times" in self.args and len(self.args["run_times"]) > 0:
            for run_time in self.args["run_times"]:
                self.run_daily(self.scheduled_scan, self.parse_time(run_time))

        self.scan_for_batteries(None, None, 0, 0, None)

    def scheduled_scan(self, kwargs):
        """ Needed because of difference between schedule and listen_state callback signatures. """

        self.scan_for_batteries(None, None, None, None, None)

    def scan_for_batteries(self, entity, attribute, old, new, kwargs):
        """ Scans home assistant for any battery level entities/attributes. """

        for item in self.scan_items:
            if item["handle"] is not None:
                self.cancel_listen_state(item["handle"])
        del self.scan_items[:]
        for ent in self.args["included_entities"]:
            attr_regex = ent["attribute"] if "attribute" in ent else None
            self.scan_items.extend(
                self.get_states_re(ent["entity_id"], attr_regex=attr_regex)
            )

        for item in self.scan_items:
            if item["attribute"] is not None:
                self.log(
                    "Battery scan discovered "
                    + item["entity_id"]
                    + "("
                    + item["friendly_name"]
                    + ")"
                    + "."
                    + item["attribute"]
                )

            else:
                self.log("Battery scan discovered " + item["entity_id"])
            #
            # Check battery levels on any discovered batteries.
            #
            new = self.get_state(item["entity_id"], item["attribute"])
            kwargs = {}
            kwargs["friendly_name"] = item["friendly_name"]
            self.check_battery_level(
                item["entity_id"], item["attribute"], new, new, kwargs
            )
            #
            # If instant_notification is True then listen for state
            # changes for any discovered batteries.
            #

            if self.args["instant_notification"]:
                item["handle"] = self.listen_state(
                    self.check_battery_level,
                    item["entity_id"],
                    attribute=item["attribute"],
                    friendly_name=item["friendly_name"],
                )

    def check_battery_level(self, entity, attribute, old, new, kwargs):
        """ Checks battery levels with values that are numeric or strings."""

        matches = [item for item in self.scan_items if item["entity_id"] == entity]
        for item in matches:
            # First check since discovered
            if item["last_checked"] is None:
                item["last_checked"] = datetime.datetime.now()
            # Enough time has passed to check again
            elif (
                int((datetime.datetime.now() - item["last_checked"]).seconds) * 60
                >= self.args["max_notification_frequency"]
                ):
                item["last_checked"] = datetime.datetime.now()
            # It's too soon to check again
            else:
                self.log(
                    "Aborting check of "
                    + entity
                    + " because it was last checked at "
                    + str(item["last_checked"])
                    + ".",
                    level="DEBUG"
                )
                return

        friendly_name = kwargs["friendly_name"]
        try:
            if not self.args["report_if_charging"] and int(new) > int(old):
                self.log(
                    "Aborting check of " + entity + " because it's charging.",
                    level="DEBUG",
                )
                return
            self.check_as_numeric(entity, attribute, friendly_name, int(new))
        except TypeError:
            if new is None:
                if not self.args["ignore_unknown"]:
                    self.send_notification(
                        "The new value of "
                        + entity
                        + " ("
                        + friendly_name
                        + ") was 'None' during a battery check. "
                    )
            if old is None:
                if not self.args["ignore_unknown"]:
                    self.send_notification(
                        "The old value of "
                        + entity
                        + " ("
                        + friendly_name
                        + ") was 'None' during a battery check. "
                    )
        except ValueError:
            if new == "unknown":
                if not self.args["ignore_unknown"]:
                    self.send_notification(
                        "The value of "
                        + entity
                        + " ("
                        + friendly_name
                        + ") was unknown during a battery check. "
                    )
            elif self.isfloat(new):
                if not self.args["report_if_charging"] and float(new) > float(old):
                    return
                self.check_as_numeric(entity, attribute, friendly_name, float(new))
            else:
                for item in self.args["non_numeric_checks"]:
                    if item.lower() == new.lower():
                        self.send_notification(
                            entity + " (" + friendly_name + ") is " + new + "."
                        )

    def check_as_numeric(self, entity, attribute, friendly_name, level):
        """ Checks numeric battery levels. """
        _entity = entity if entity is not None else ""
        _attribute = attribute if attribute is not None else ""
        _friendly_name = friendly_name if friendly_name is not None else ""
        _level = level if level is not None else 0

        try:
            if _level < self.args["urgent_level"]:
                self.send_notification(
                    "Urgent! - The battery of "
                    + _entity
                    + " ("
                    + _friendly_name
                    + ")."
                    + _attribute
                    + " has reached "
                    + str(_level)
                    + "%"
                )
            elif _level < self.args["warning_level"]:
                self.send_notification(
                    "Warning - The battery of "
                    + _entity
                    + " ("
                    + _friendly_name
                    + ")."
                    + _attribute
                    + " has reached "
                    + str(_level)
                    + "%"
                )
        except ValueError:
            self.log(str(level) + " is not numberic", level="ERROR")

    def send_notification(self, msg):
        """ Sends notification to all configured locations. """

        if self.args["persistent_notification"]:
            self.call_service(
                "persistent_notification/create", title="Battery Low", message=msg
            )
        data = {"color": self.notification_color}
        for phone in self.args["phones"]:
            self.messenger.send_message(
                False,
                device=phone,
                message=msg,
                title="Battery Notification",
                data=data,
            )

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def get_states_re(self, entity_regex, **kwargs):
        """Searches for entities and optionally attributes that match a given regex pattern.

        entity_regex -- required - regex pattern for entity id
        attr_regex optional (if in kwargs) -- regex pattern for attributes

        If attr_regex is provided both the entity and the attribute must match

        A list of matches is returned in the format:
        entity_id.state (for entity_id only matches)
        entity_id.attribute (for entity_id and attribute matches)"""

        matches = []
        states = self.get_state()
        #
        # states contains a dictionary with the entity_ids as the keys
        # The values are sub-directionaries containing the information about the entity
        # The attributes are in a sub-dictionary of the values dictionary
        #
        for entity_id, entity_info in states.items():
            match = {}
            match["handle"] = None
            match["attribute"] = None
            match["entity_id"] = None
            match["friendly_name"] = None
            match["current_value"] = "0"
            match["last_checked"] = None
            match_found = False
            if re.search(entity_regex, entity_id):
                match["entity_id"] = entity_id
                if "friendly_name" in entity_info["attributes"]:
                    match["friendly_name"] = entity_info["attributes"]["friendly_name"]
                else:
                    match["friendly_name"] = ""

                if "attr_regex" in kwargs and kwargs["attr_regex"] is not None:
                    for attr in entity_info["attributes"].keys():
                        if re.search(kwargs["attr_regex"], attr):
                            match["attribute"] = attr
                            match_found = True
                            match["current_value"] = self.get_state(entity_id, attr)
                    # As written this will always use the last match so ?
                else:
                    match_found = True
                    match["current_value"] = self.get_state(entity_id)
            if match_found and match["entity_id"] not in self.args["excluded_entities"]:
                match["handle"] = None
                matches.append(match)

        return matches
