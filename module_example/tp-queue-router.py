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

class LinuxRouter( Node ):
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.1.1/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 172.16.0.1/12 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 200.100.1.1/24 brd + dev r0-eth2' )
        self.cmd( 'ip addr add 10.10.0.1/12 brd + dev r0-eth3' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        # Add Router
        router = self.addNode( 'r0', cls=LinuxRouter, ip='192.168.1.1/24' )
        
        # Add Host
        h0 = self.addHost( 'h0', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
        h1 = self.addHost( 'h1', ip='172.16.0.100/12', defaultRoute='via 172.16.0.1' )
        h2 = self.addHost( 'h2', ip='200.100.1.100/24', defaultRoute='via 200.100.1.1' )
        h3 = self.addHost( 'h3', ip='10.10.0.100/12', defaultRoute='via 10.10.0.1' )

        # Add Link
        self.addLink( h0, router, intfName2='r0-eth0', bw=10 ) 
        self.addLink( h1, router, intfName2='r0-eth1', bw=10 )
        self.addLink( h2, router, intfName2='r0-eth2', bw=10, use_htb=True )
        self.addLink( h3, router, intfName2='r0-eth3', bw=10 )

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
        
def runQueue():
    # Run Mininet
    net = Mininet( topo=NetworkTopo(), link=TCLink )
    net.start()

    # Test Ping All Host
    info("\n\n", net.ping() ,"\n")
    
    info( '\n****Start Analysis *****\n' )
    
    # Set Queue Discipline to CBQ Bounded
    info( '\n*** Queue Disicline = CBQ [bounded] :\n' )
    net[ 'r0' ].cmdPrint( 'tc qdisc del dev r0-eth0 root' ) 
    net[ 'r0' ].cmdPrint( 'tc qdisc add dev r0-eth0 root handle 1: cbq rate 7Mbit avpkt 1000' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth0 parent 1: classid 1:1 cbq rate 1Mbit avpkt 1000 bounded' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth0 parent 1: classid 1:2 cbq rate 3Mbit avpkt 1000 bounded' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth0 parent 1: classid 1:3 cbq rate 5Mbit avpkt 1000 bounded' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth0 parent 1: protocol ip u32 match ip src '+net[ 'h1' ].IP()+' flowid 1:1' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth0 parent 1: protocol ip u32 match ip src '+net[ 'h2' ].IP()+' flowid 1:2' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth0 parent 1: protocol ip u32 match ip src '+net[ 'h3' ].IP()+' flowid 1:3' ) 
    net[ 'r0' ].cmdPrint( 'tc qdisc show dev r0-eth0' )
    info( "\n" )
    
    # Test Iperf CBQ Bounded
    testIperf( net, 'h0', ('h1', 'h2', 'h3') )


    # Set Queue Discipline to CBQ Isolated 
    info( '\n*** Queue Disicline = CBQ [isolated] :\n' )
    net[ 'r0' ].cmdPrint( 'tc qdisc del dev r0-eth1 root' ) 
    net[ 'r0' ].cmdPrint( 'tc qdisc add dev r0-eth1 root handle 2: cbq rate 7Mbit avpkt 1000' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth1 parent 2: classid 2:1 cbq rate 1Mbit avpkt 1000 isolated' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth1 parent 2: classid 2:2 cbq rate 3Mbit avpkt 1000 isolated' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth1 parent 2: classid 2:3 cbq rate 5Mbit avpkt 1000 isolated' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth1 parent 2: protocol ip u32 match ip src '+net[ 'h0' ].IP()+' flowid 2:1' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth1 parent 2: protocol ip u32 match ip src '+net[ 'h2' ].IP()+' flowid 2:2' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth1 parent 2: protocol ip u32 match ip src '+net[ 'h3' ].IP()+' flowid 2:3' ) 
    net[ 'r0' ].cmdPrint( 'tc qdisc show dev r0-eth1' )
    info( "\n" )

    # Test Iperf CBQ Isolated
    testIperf( net, 'h1', ('h0', 'h2', 'h3') )

    
    # Set Queue Discipline to HTB 
    info( '\n*** Queue Disicline = HTB :\n' )
    net[ 'r0' ].cmdPrint( 'tc qdisc del dev r0-eth2 root' ) 

    # add queue discipline root
    net[ 'r0' ].cmdPrint( 'tc qdisc add dev r0-eth2 root handle 3:0 htb ' ) 
    
    # add queue dicipline classes  
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth2 parent 3: classid 3:1 htb rate 5Mbit ceil 4Mbit burst 2k' )
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth2 parent 3: classid 3:2 htb rate 4Mbit ceil 2Mbit burst 2k' ) 
    net[ 'r0' ].cmdPrint( 'tc class add dev r0-eth2 parent 3: classid 3:3 htb rate 2Mbit ceil 3Mbit burst 2k' ) 
    
    #Add pfifo queuing  
    net[ 'r0' ].cmdPrint( ' tc qdisc add dev r0-eth2 parent 3:1 handle 31 pfifo limit 10')
    net[ 'r0' ].cmdPrint( ' tc qdisc add dev r0-eth2 parent 3:2 handle 32 pfifo limit 10')
    net[ 'r0' ].cmdPrint( ' tc qdisc add dev r0-eth2 parent 3:3 handle 33 pfifo limit 10')

    # add queue dicipline filters
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth2 parent 3: protocol ip u32 match ip src '+net[ 'h0' ].IP()+' flowid 3:1' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth2 parent 3: protocol ip u32 match ip src '+net[ 'h1' ].IP()+' flowid 3:2' ) 
    net[ 'r0' ].cmdPrint( 'tc filter add dev r0-eth2 parent 3: protocol ip u32 match ip src '+net[ 'h2' ].IP()+' flowid 3:3' )
    
    net[ 'r0' ].cmdPrint( 'tc qdisc show dev r0-eth2' )
    info( "\n" )

    # Test Iperf HTB
    testIperf( net, 'h2', ('h0', 'h1', 'h3') )


    # Set Queue Discipline to No Queue
    info( '\n*** Queue Disicline = No Queue :\n' )
    net[ 'r0' ].cmdPrint( 'tc qdisc del dev r0-eth3 root' ) 
    net[ 'r0' ].cmdPrint( 'tc qdisc show dev r0-eth3' )
    info( "\n" )

    # Test Iperf No Queue
    testIperf( net, 'h3', ('h0', 'h1', 'h2') )

    # Stop Mininet
    net.stop()

if __name__ == '__main__':
    os.system( 'mn -c' )
    print('==========================================================================')
    setLogLevel( 'info' )
    runQueue()
