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

import signal
import sys

from neutron.agent.linux import ip_lib
from neutron.i18n import _LE, _LI

from oslo.config import cfg
from neutron.common import config as common_config
from neutron.common import constants as q_const
from neutron.common import utils as q_utils
from neutron.openstack.common import log as logging

from neutron.plugins.openvswitch.agent.ovs_neutron_agent import \
    create_agent_config_map, OVSNeutronAgent

from networking_bagpipe_l2.agent import bagpipe_bgp_agent

LOG = logging.getLogger(__name__)
cfg.CONF.import_group('AGENT', 'neutron.plugins.openvswitch.common.config')

# TODO: To be replaced by something better
DEFAULT_GATEWAY_MAC = "00:00:de:ad:be:ef"


class OVSBagpipeNeutronAgent(OVSNeutronAgent):

    def __init__(self, *args, **kwargs):
        super(OVSBagpipeNeutronAgent, self).__init__(*args, **kwargs)

        # Creates an HTTP client for BaGPipe BGP component REST service
        self.bgp_agent = (bagpipe_bgp_agent.BaGPipeBGPAgent(
            self.root_helper,
            q_const.AGENT_TYPE_OVS,
            int_br=self.int_br,
            tun_br=self.tun_br,
            patch_int_ofport=self.patch_int_ofport,
            local_vlan_map=self.local_vlan_map,
            setup_entry_for_arp_reply=self.setup_entry_for_arp_reply)
        )

        self.bgp_agent.setup_rpc(self.endpoints, self.connection, self.topic)


def main():
    cfg.CONF.register_opts(ip_lib.OPTS)
    common_config.init(sys.argv[1:])
    common_config.setup_logging()
    q_utils.log_opt_values(LOG)

    try:
        agent_config = create_agent_config_map(cfg.CONF)
    except ValueError as e:
        LOG.error(_LE('%s Agent terminated!'), e)
        sys.exit(1)

    is_xen_compute_host = 'rootwrap-xen-dom0' in agent_config['root_helper']
    if is_xen_compute_host:
        # Force ip_lib to always use the root helper to ensure that ip
        # commands target xen dom0 rather than domU.
        cfg.CONF.set_default('ip_lib_force_root', True)

    agent = OVSBagpipeNeutronAgent(**agent_config)
    signal.signal(signal.SIGTERM, agent._handle_sigterm)

    # Start everything.
    LOG.info(_LI("Agent initialized successfully, now running... "))
    agent.daemon_loop()


if __name__ == "__main__":
    main()
