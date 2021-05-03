#!/usr/bin/python

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Node
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.util import pmonitor
from signal import SIGINT
from time import time
import os

def testIperf( net, server='h0', clients=('h1', 'h2', 'h3') ):
    popens = {}
    tperf = 20
    tout = ( tperf + 1 ) * 4
    stopPerf = time() + tout + 5
    inv = 4

    popens[ net[ server ] ] = net[ server ].popen( 'iperf -s -t '+str( tout ) )
    for client in clients:
        popens[ net[ client ] ] = net[ client ].popen( 'iperf -c '+net[ server ].IP()+' -i '+str(inv)+' -t '+str( tperf ) )
    
    logserver = logclient1 = logclient2 = logclient3 = ""

    for host, line in pmonitor(popens, timeoutms=(tperf + tout) * 4):
    	if host:
            if host.name == server: logserver += (host.name +": "+line)
            elif host.name == clients[0]: logclient1 += (host.name +": "+line)
            elif host.name == clients[1]: logclient2 += (host.name +": "+line)
            elif host.name == clients[2]: logclient3 += (host.name +": "+line)

    	if time() >= stopPerf:
    		for p in popens.values(): p.send_signal(SIGINT)

    print(logserver)
    print(logclient1)
    print(logclient2)
    print(logclient3)
      
def routerNet():
    # Run Mininet
    net = Mininet( link=TCLink )
    
    # Add Router
    net.addHost( 'r0', ip='192.168.1.1/24' )
    
    # Add Host h0,h1,h2,h3
    h0 = net.addHost('h0', ip='192.168.1.2/29', defaultRoute='via 192.168.1.1')
    h1 = net.addHost('h1', ip='192.168.3.2/29', defaultRoute='via 192.168.3.1')
    h2 = net.addHost('h2', ip='192.168.4.2/29', defaultRoute='via 192.168.4.1')
    h3 = net.addHost('h3', ip='192.168.5.2/29', defaultRoute='via 192.168.5.1')

    # Add Link
    net.addLink( net[ 'h0' ], net[ 'r0' ], intfName2='r0-eth0', bw=10 ) 
    net.addLink( net[ 'h1' ], net[ 'r0' ], intfName2='r0-eth1', bw=10 ) 
    net.addLink( net[ 'h2' ], net[ 'r0' ], intfName2='r0-eth2', bw=10 )
    net.addLink( net[ 'h3' ], net[ 'r0' ], intfName2='r0-eth3', bw=10 )

    # Add IP Address for Router
    net[ 'r0' ].cmd( 'ip addr add 192.168.1.1/29 brd + dev r0-eth0' )
    net[ 'r0' ].cmd( 'ip addr add 192.168.3.1/29 brd + dev r0-eth1' )
    net[ 'r0' ].cmd( 'ip addr add 192.168.4.1/29 brd + dev r0-eth2' )
    net[ 'r0' ].cmd( 'ip addr add 192.168.5.1/29 brd + dev r0-eth3' )
    
    # Start IP Forward on Router
    net[ 'r0' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    
    # Start Network
    net.start()
    
    # Ping All Host
    info( '\n', net.ping() ,'\n' )
    
    # Set Queue Discipline to CBQ
    info( '\n*** Queue Disicline :\n' )
    
    # reset queue discipline
    net[ 'r0' ].cmdPrint( 'tc qdisc del dev r0-eth0 root' ) 

    # add queue discipline root here
    net['r0'].cmdPrint('tc qdisc add dev r0-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
    
    # add queue dicipline classes here 
    net['r0'].cmdPrint('tc class add dev r0-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
    net['r0'].cmdPrint('tc class add dev r0-eth0 parent 1: classid 1:2 cbq rate 5Mbit avpkt 1000 isolated')

    # add queue dicipline filters
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth0 parent 1: protocol ip u32 match ip src '+net[ 'h1' ].IP()+' flowid 1:1' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth0 parent 1: protocol ip u32 match ip src '+net[ 'h2' ].IP()+' flowid 1:2' ) 
    net[ 'r0' ].cmdPrint( 'tc qdisc show dev r0-eth0' )
    info( '\n' )

    # Test Iperf
    testIperf( net, 'h0', ('h1', 'h2', 'h3') )

    # Stop Network
    net.stop()

if __name__ == '__main__':
    os.system('mn -c')
    os.system( 'clear' )
    setLogLevel( 'info' )
    routerNet()
