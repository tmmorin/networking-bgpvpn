from neutron import manager
from neutron import context as n_context

from neutron.openstack.common import log
from neutron.plugins.common import constants

from neutron.plugins.ml2 import driver_api as api


LOG = log.getLogger(__name__)


class ML2BGPVPNMechanismDriver(api.MechanismDriver):
    """
    This ML2 mechanism driver simply notifies the BGPVPNPlugin of update/delete
    port events.

    It allows to notify BGP VPN plugin service drivers that need to be aware
    of ports coming and going.
    """

    def initialize(self):
        self.db_context = n_context.get_admin_context()

    def delete_network_precommit(self, context):
        network = context.current

        bgpvpnplugin = manager.NeutronManager.get_service_plugins().get(
            constants.BGPVPN)

        if bgpvpnplugin:
            bgpvpnplugin.prevent_bgpvpn_network_deletion(self.db_context,
                                                         network['id'])

    def update_port_postcommit(self, context):
        port = context.current

        bgpvpnplugin = manager.NeutronManager.get_service_plugins().get(
            constants.BGPVPN)

        if bgpvpnplugin:
            bgpvpnplugin.notify_port_updated(self.db_context, port)

    def delete_port_postcommit(self, context):
        port = context.current

        bgpvpnplugin = manager.NeutronManager.get_service_plugins().get(
            constants.BGPVPN)

        if bgpvpnplugin:
            bgpvpnplugin.remove_port_from_bgpvpn_agent(self.db_context, port)
