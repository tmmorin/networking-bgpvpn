# Copyright (c) 2015 Orange.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log

from neutron.plugins.ml2 import driver_api as api

LOG = log.getLogger(__name__)


class ML2BGPVPNMechanismDriver(api.MechanismDriver):
    """This driver notifies the BGPVPNPlugin driver of port events.

    It allows to notify BGP VPN plugin service drivers that need to be aware
    of ports coming and going.
    """

    def initialize(self):
        LOG.warning("The bgpvpn_notify mechanism is now unneeded and "
                    "can be safely removed from your config")
