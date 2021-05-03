#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from time import time
from mininet.util import pmonitor
from signal import SIGINT
import os

def testIperf( net, server='h0', clients=('h1', 'h2') ):
    popens = {}
    tperf = 20
    tout = ( tperf + 1 ) * 4
    stopPerf = time() + tout + 5
    inv = 4

    popens[ net[ server ] ] = net[ server ].popen( 'iperf -s -t '+str( tout ) )
    for client in clients:
        popens[ net[ client ] ] = net[ client ].popen( 'iperf -c '+net[ server ].IP()+' -i '+str(inv)+' -t '+str( tperf ) )
    
    logserver = logclient1 = logclient2 = ""

    for host, line in pmonitor(popens, timeoutms=(tperf + tout) * 4):
    	if host:
            if host.name == server: logserver += (host.name +": "+line)
            elif host.name == clients[0]: logclient1 += (host.name +": "+line)
            elif host.name == clients[1]: logclient2 += (host.name +": "+line)


    	if time() >= stopPerf:
    		for p in popens.values(): p.send_signal(SIGINT)

    print(logserver)
    print(logclient1)
    print(logclient2)


def openSwitchNet():

    net = Mininet( controller=Controller, switch=OVSSwitch, link=TCLink )

    info( "*** Creating (reference) controllers\n" )
    c = net.addController( 'c1', port=6633 )

    info( "*** Creating switches\n" )
    #add switch here
    s0 = net.addSwitch('s0')
    
    #add h0,h1,h2 here
    info( "*** Creating hosts\n" )
    h0 = net.addHost( 'h0', ip = '192.168.1.1/25' )
    h1 = net.addHost( 'h1', ip = '192.168.1.2/25' )
    h2 = net.addHost( 'h2', ip = '192.168.1.3/25' )
        
    #add link h0-s0 include interface s0-eth
    info( "*** Creating links\n" )
    net.addLink(h0, s0, intfName2='s0-eth0', bw=10, use_htb=True )
    net.addLink(h1, s0, intfName2='s0-eth1', bw=10, use_htb=True )
    net.addLink(h2, s0, intfName2='s0-eth2', bw=10, use_htb=True )
    

    info( "*** Starting network\n" )
    net.build()
    c.start()
    s0.start([c])

    # Ping All Host
    info( '\n', net.ping() ,'\n' )
    
    # Set Queue Discipline to htb
    info( '\n*** Queue Disicline :\n' )
    
    # reset queue discipline
    s0.cmdPrint( 'tc qdisc del dev s0-eth0 root' ) 

    # add queue discipline root
    s0.cmdPrint( 'tc qdisc add dev s0-eth0 root handle 1:0 htb ' ) 

    #Add classs for root
    s0.cmdPrint( 'tc class add dev s0-eth0 parent 1: classid 1:1 htb rate 10Mbit ' )
    
    # add queue dicipline classes  
    s0.cmdPrint( 'tc class add dev s0-eth0 parent 1:1 classid 1:2 htb rate 4Mbit ceil 3Mbit ' )
    s0.cmdPrint( 'tc class add dev s0-eth0 parent 1:1 classid 1:3 htb rate 4Mbit ceil 1Mbit ' ) 

    #Add pfifo queuing
    s0.cmdPrint( ' tc class add dev s0-eth0 parent 1:2 classid 1:21 htb rate 2Mbit ceil 2Mbit')
    s0.cmdPrint( ' tc class add dev s0-eth0 parent 1:3 classid 1:31 htb rate 3Mbit ceil 2Mbit')
    
    s0.cmdPrint( ' tc qdisc add dev s0-eth0 parent 1:21 handle 210: pfifo limit 20')
    s0.cmdPrint( ' tc qdisc add dev s0-eth0 parent 1:31 handle 310: pfifo limit 10')
    
    # add queue dicipline filters (can use port to divide based on data delivery port)
    s0.cmdPrint( 'tc filter add dev s0-eth0 parent 1: protocol ip prio 1 u32 match ip src '+net[ 'h0' ].IP()+' flowid 1:21' ) 
    s0.cmdPrint( 'tc filter add dev s0-eth0 parent 1: protocol ip prio 1 u32 match ip src '+net[ 'h1' ].IP()+' flowid 1:31' ) 
    
    s0.cmdPrint( 'tc qdisc show dev s0-eth0' )
    info( '\n' )

    # Test Iperf
    testIperf( net, 'h0', ('h1', 'h2') )
    
    # Stop Network
    net.stop()

if __name__ == '__main__':
    os.system( 'mn -c' )
    os.system( 'clear' )
    setLogLevel( 'info' )  # for CLI output
    openSwitchNet()
