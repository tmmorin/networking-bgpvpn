How to use bagpipe driver jointly as the openvswitch ML2 mech driver ?
----------------------------------------------------------------------

* add bgpvpn_notify to Q_ML2_PLUGIN_MECHANISM_DRIVERS

* add ::

	[[post-config|/$NEUTRON_CONF]]
	[service_providers]
	service_provider=BGPVPN:BaGPipe:networking_bgpvpn.neutron.services.bgpvpn.service_drivers.bagpipe.bagpipe.BaGPipeBGPVPNDriver:default

* configure the openvswitch mech_driver to enable the agent ARP responder

* agent:

  * install networking-bagpipe-l2_

  * run neutron-bagpipe-openvswitch-agent instead of neutron-bagpipe-openvswitch-agent in for q-agt 

