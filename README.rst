===============================
networking-bgpvpn
===============================

API and Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks

* Free software: Apache license
* Source: http://git.openstack.org/cgit/stackforge/networking-bgpvpn
* Bugs: http://bugs.launchpad.net/bgpvpn

Quick start
-----------

To be able to test this framework, you have to:

* clone this repo and install the python package: ::

	git clone https://git.openstack.org/stackforge/networking-bgpvpn
	
	sudo python setup.py develop

* run the latest devstack (and let it fetch latest openstack code)
  with the following options: ::

	Q_SERVICE_PLUGIN_CLASSES=networking_bgpvpn.neutron.services.bgpvpn.plugin.BGPVPNPlugin
	
	[[post-config|/$NEUTRON_CONF]]
	[service_providers]
	service_provider=BGPVPN:Dummy:networking_bgpvpn.neutron.services.bgpvpn.service_drivers.dummy.dummyBGPVPNDriver:default

* init the db with: ::

	/usr/local/bin/bgpvpn-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head

* bgpvpn-connection-create/update/delete/show/list commands will be available with 
  the neutron client, for example: ::

	source openrc admin admin
	neutron bgpvpn-connection-create --route-targets 64512:1
	neutron bgpvpn-connection-list
	neutron bgpvpn-connection-update <bgpvpn-connection-uuid> --network-id <neutron-net-uuid>

