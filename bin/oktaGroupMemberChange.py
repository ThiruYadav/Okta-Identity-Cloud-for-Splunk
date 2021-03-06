
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_okta_identity_cloud_for_splunk_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_oktaGroupMemberChange_helper

class AlertActionWorkeroktaGroupMemberChange(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkeroktaGroupMemberChange, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_global_setting("max_log_batch"):
            self.log_error('max_log_batch is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_param("okta_org"):
            self.log_error('okta_org is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("user_id"):
            self.log_error('user_id is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("group_id"):
            self.log_error('group_id is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("action"):
            self.log_error('action is a mandatory parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_oktaGroupMemberChange_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e.message:
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkeroktaGroupMemberChange("TA-Okta_Identity_Cloud_for_Splunk", "oktaGroupMemberChange").run(sys.argv)
    sys.exit(exitcode)
