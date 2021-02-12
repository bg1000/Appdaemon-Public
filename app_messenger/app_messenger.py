import hassapi as hass  # pylint: disable=import-error
import adbase as ad  # pylint: disable=import-error
import copy


class app_messenger(hass.Hass):
    def initialize(self):
        self._data = {}
        self._device = self.args["device"]
        for key, value in self.args["data"].items():
            self._data[key] = value
            if value is None:
                value = ""
            else:
                value = str(value)
            self.log("default data." + key + " is: " + value, level="DEBUG")
        self._data = self.args["data"]
        self._message = self.args["message"]
        self._title = self.args["title"]
        self.log("default device is: " + self._device, level="DEBUG")
        self.log("default message is: " + self._message, level="DEBUG")
        self.log("default title is: " + self._title, level="DEBUG")

    @ad.app_lock
    def send_message(self, replace, **kwargs):
        """Sends phone notification

        If replace is true use only what is passed in kwargs.
        if replace is false update defaults with what is passed in kwargs.


        The desired functionality is for users to be able to omit optional
        parameters by deleting them or setting them to 'None'. However, the service
        call fails when these 'None' values are passed.
        We will instead pass a nested dictionary with all the none values stripped out."""

        if replace:
            device = kwargs["device"] if "device" in kwargs else None
            message = kwargs["message"] if "message" in kwargs else None
            title = kwargs["title"] if "title" in kwargs else None
            data = kwargs["data"] if "data" in kwargs else None
            self.log("Sending message in replace mode.", level="DEBUG")
        else:
            self.log("Sending message in update mode.", level="DEBUG")
            device = kwargs["device"] if "device" in kwargs else self._device
            message = kwargs["message"] if "message" in kwargs else self._message
            title = kwargs["title"] if "title" in kwargs else self._title
            if "data" in kwargs:
                self.log("Data was in kwargs", level="DEBUG")
                self.log("kwargs[data] is: %s", kwargs["data"], level="DEBUG")
                data = copy.deepcopy(self._data)
                if kwargs["data"] is not None:
                    data.update(kwargs["data"])
                self.log("data is: %s", data, level="DEBUG")
            else:
                self.log("Data was not in kwargs", level="DEBUG")
                data = self._data
        if data is not None:
            data = self.RemoveNoneArgs(**data)
        else:
            self.log("Message data is None.", level="DEBUG")
        kwargs = self.RemoveNoneArgs(title=title, message=message, data=data)

        self.log("Sending message " + message + " to " + device + ".", level="INFO")
        self.call_service("notify/" + device, **kwargs)

    def RemoveNoneArgs(self, **kwargs):
        """Accepts key word arguments and returns a dictionary with
        any items that were None stripped out of the original dictionary
        The idea for this comes from the link below (response #9).

        https://stackoverflow.com/questions/52494128/call-function-without-optional-arguments-if-they-are-none"""

        return {k: v for k, v in kwargs.items() if v is not None}
