
#!/usr/bin/python

 

"""

Script created by VND - Visual Network Description (SDN version)

"""

from mininet.net import Mininet

from mininet.node import Controller, RemoteController, OVSKernelSwitch, OVSLegacyKernelSwitch, UserSwitch

from mininet.cli import CLI

from mininet.log import setLogLevel

from mininet.link import Link, TCLink
import os

 

def topology():

    "Create a network."

    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

 

    print ("*** Creating nodes")

    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24' )

    h2 = net.addHost( 'h2', mac='00:00:00:00:00:02', ip='10.0.10.2/24' )

    h3 = net.addHost( 'h3', mac='00:00:00:00:00:03', ip='10.0.0.2/24' )

    s4 = net.addSwitch( 's4', listenPort=6673, mac='00:00:00:00:00:04' )

    s5 = net.addSwitch( 's5', listenPort=6674, mac='00:00:00:00:00:05' )

    c7 = net.addController( 'c7', controller=RemoteController, ip='127.0.0.1', port=6633 )

 

    print ("*** Creating links")

    net.addLink(s4, h3, 2, 0)

    #net.addLink(h1, s4, 0, 1)

    Link(h1, s4, intfName1='h1-eth0')

    net.addLink(s5, h2, 2, 0)

    #net.addLink(h1, s5, 0, 1)

    Link(h1, s5, intfName1='h1-eth1')

    h1.cmd('ifconfig h1-eth1 10.0.10.1 netmask 255.255.255.0')

 

    print ("*** Starting network")

    net.build()

    c7.start()

    s4.start( [c7] )

    s5.start( [c7] )

 

    print ("*** Running CLI")

    CLI( net )

 

    print ("*** Stopping network")

    net.stop()

 

if __name__ == '__main__':

    setLogLevel( 'info' )

    topology()