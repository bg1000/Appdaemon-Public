import hassapi as hass  # pylint: disable=import-error


class cover_tag_scanned(hass.Hass):
    """ Opens or closes a cover based on an nfc_tag being scanned """

    def initialize(self):
        self.listen_event(
            self.door_tag_scanned,
            "tag_scanned",
            tag_id=self.args["tag_id"],
        )

    def door_tag_scanned(self, event_name, data, kwargs):
        """Open the door if it's closed. Close the door if it's open.
        Ignore the event if the door is opening or closing.
        If a device list is provided, ignore the scan if it
        didn't come from a device in the list.
        'data' looks like this:
        'data': {'tag_id': 'cae3c8c5-faac-4585-be93-a1199fa98fcd',
        'device_id': 'effd5529caba2c3f'}"""

        self.log(
            "tag_id = " + data["tag_id"] + ". device_id = " + data["device_id"],
            level="DEBUG",
        )
        if "devices" in self.args and data["device_id"] not in self.args["devices"]:
            self.log(
                "Ignoring scan from unlisted device " + data["device_id"] + ".",
                level="INFO",
            )
            return
        if self.get_state(self.args["cover_entity"]) == "open":
            self.log(
                "Closing garage door due to NFC tag scan by device "
                + data["device_id"]
                + ".",
                level="INFO",
            )
            self.call_service("cover/close_cover", entity_id=self.args["cover_entity"])
        elif self.get_state(self.args["cover_entity"]) == "closed":
            self.log(
                "Opening garage door due to NFC tag scan by device "
                + data["device_id"]
                + ".",
                level="INFO",
            )
            self.call_service("cover/open_cover", entity_id=self.args["cover_entity"])
