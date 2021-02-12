import hassapi as hass  # pylint: disable=import-error
import datetime as datetime


class goodnight(hass.Hass):
    def initialize(self):
        self.recheck_handle = None
        self.messenger = self.get_app("app_messenger")
        for id in self.args["tag_ids"]:
            self.listen_event(self.goodnight_tag_scanned, "tag_scanned", tag_id=id)

    def goodnight_tag_scanned(self, event_name, data, kwargs):
        self.log("Goodnight tag scanned", level="INFO")
        self.log(
            "tag_id = " + data["tag_id"] + ". device_id = " + data["device_id"],
            level="INFO",
        )
        self.check_count = 0
        self.run_tests()

    def run_tests(self, kwargs=None):
        self.check_count += 1
        args = self.app_config[self.name]
        self.log("Check count = " + str(self.check_count), level="DEBUG")
        if (self.check_count) > self.args["max_rechecks"]:
            if "overall_failure_message" in args:
                self.send_notifications(
                    self.args["notification_list"], args["overall_failure_message"]
                )
            self.cancel_timer(self.recheck_handle)
            self.recheck_handle = None
            self.check_count = 0
            return
        self.failed = False
        for test in args["tests"]:
            attribute = test["attribute"] if "attribute" in test else "state"
            if not self.passed_test(
                test["entity_id"], attribute, test["test"], test["value"]
            ):
                self.log("Test failed for " + test["entity_id"], level="DEBUG")
                self.failed = True
                if "failure_service_call" in test:
                    self.make_service_call(test)
                else:
                    self.send_notifications(
                        self.args["notification_list"], test["failure_message"]
                    )
                if (
                    "final_failure_message" in test
                    and self.check_count == self.args["max_rechecks"]
                ):
                    self.send_notifications(
                        self.args["notification_list"], test["final_failure_message"]
                    )
            else:
                self.log("Test passed for " + test["entity_id"], level="DEBUG")
        if not self.failed:
            self.check_count = 0
            self.send_notifications(
                self.args["notification_list"], self.args["overall_success_message"]
            )

    def passed_test(self, entity, attribute, test, value):
        self.log("entity = " + entity, level="DEBUG")
        self.log("attribute = " + attribute, level="DEBUG")
        self.log("test = " + test, level="DEBUG")
        self.log("test value = " + value, level="DEBUG")
        self.log(
            "attribute value = "
            + str(self.get_state(entity_id=entity, attribute=attribute)),
            level="DEBUG",
        )
        if test == "==":
            return self.get_state(entity_id=entity, attribute=attribute) == value
        elif test == "!=":
            return self.get_state(entity_id=entity, attribute=attribute) != value
        else:
            raise ValueError("Test must be one of: ==, !=")

    def make_service_call(self, test):
        msg = (
            test["failure_service_call"]
            + ". Will be rechecked in "
            + str(test["retry_seconds"])
            + " seconds."
        )
        self.log(msg, level="DEBUG")
        self.call_service(test["failure_service_call"], **test["service_parameters"])
        if self.recheck_handle is not None:
            time, interval, kwargs = self.info_timer(self.recheck_handle)
            self.log("Recheck currently scheduled for " + str(time), level="DEBUG")
            duration = time - datetime.datetime.now()
            if duration.total_seconds() < test["retry_seconds"]:
                self.cancel_timer(self.recheck_handle)
                self.log(
                    "Restting recheck timer for "
                    + str(test["retry_seconds"])
                    + " seconds.",
                    level="DEBUG",
                )
                self.recheck_handle = self.run_in(self.run_tests, test["retry_seconds"])
            else:
                self.log(
                    "Starting recheck timer for "
                    + str(test["retry_seconds"])
                    + " seconds.",
                    level="DEBUG",
                )
                self.recheck_handle = self.run_in(self.run_tests, test["retry_seconds"])
            if "service_message" in test:
                self.send_notifications(
                    self.args["notification_list"],
                    test["service_message"]
                    + ". Will be rechecked in "
                    + str(test["retry_seconds"])
                    + " seconds.",
                )

    def send_notifications(self, notify_list, msg, **kwargs):
        data = kwargs["data"] if "data" in kwargs else None

        for list_item in notify_list:
            self.log("Sending notification to " + list_item, level="DEBUG")
            self.messenger.send_message(
                False,
                device=list_item,
                message=msg,
                title="Goodnight Notification",
                data=data,
            )
