#!/usr/bin/python
#
#   tapinfo.py : List TAP device info for running VMs
#
#   2010/01/20 ver1.0
#   2010/01/21 ver1.1
#

import libvirt
import os
import re
from xml.dom import minidom

Conn = libvirt.open( "qemu:///system" )

def showTaps():
    vnetRe = re.compile( "vnet\d+" )
    fmt = "%-16s %-12s %-18s %-12s %-12s"
    print fmt % ( "Domain", "Tap", "MAC Address", "Network", "Bridge" )
    for id in Conn.listDomainsID():
        print "-" * 78
        vm = Conn.lookupByID( id )
        vmXMLDesc = minidom.parseString( vm.XMLDesc( 0 ) )
        for iface in vmXMLDesc.getElementsByTagName( "interface" ):
            ifaceType = iface.getAttribute( "type" )
            if ifaceType == "network":
                network = iface.getElementsByTagName( "source" )[0].getAttribute( "network" )
                netXMLDesc = minidom.parseString( Conn.networkLookupByName( network ).XMLDesc( 0 ) )
                bridge = netXMLDesc.getElementsByTagName( "bridge" )[ 0 ].getAttribute( "name" )
            elif ifaceType == "bridge":
                network = ""
                bridge = iface.getElementsByTagName( "source" )[0].getAttribute( "bridge" )
            mac = iface.getElementsByTagName( "mac" )[0].getAttribute( "address" )
            device = iface.getElementsByTagName( "target" )[0].getAttribute( "dev" )
            print fmt % ( vm.name(), device, mac, network, bridge )

if __name__ == "__main__":
    showTaps()
    print

