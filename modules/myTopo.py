#!/usr/bin/python
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Node
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.util import pmonitor
from signal import SIGINT
import time
import os

# Creating all the router

class Router1( Node ):
    def config( self, **params ):
        super( Router1, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.0.1/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 192.168.100.1/24 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 192.168.100.2/24 brd + dev r0-eth2' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router1, self ).terminate()
        
class Router2( Node ):
    def config( self, **params ):
        super( Router2, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.0.2/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 192.168.100.5/24 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 192.168.100.6/24 brd + dev r0-eth2' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router2, self ).terminate()

class Router3( Node ):
    def config( self, **params ):
        super( Router3, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.1.1/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 192.168.100.3/24 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 192.168.100.4/24 brd + dev r0-eth2' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router3, self ).terminate()
        
class Router4( Node ):
    def config( self, **params ):
        super( Router4, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.1.2/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 192.168.100.7/24 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 192.168.100.8/24 brd + dev r0-eth2' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router4, self ).terminate()


# Creating host and Link

topos = { 'mytopo': ( lambda: NetworkTopo() ) }
class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        # Add Router
        router1 = self.addNode( 'r1', cls=Router1, ip='192.168.0.1/24' )
        router2 = self.addNode( 'r2', cls=Router2, ip='192.168.0.2/24' )
        router3 = self.addNode( 'r3', cls=Router3, ip='192.168.1.1/24' )
        router4 = self.addNode( 'r4', cls=Router4, ip='192.168.1.2/24' )
        
        # Add Host
        h0 = self.addHost( 'h0', ip='192.168.0.3/24', defaultRoute='via 192.168.0.1' )
        h1 = self.addHost( 'h1', ip='192.168.1.3/24', defaultRoute='via 192.168.1.1' )

        # Add Link from Host to Router
        self.addLink( h0, router1, intfName2='r0-eth0', bw=1 ) 
        self.addLink( h0, router2, intfName2='r0-eth0', bw=1 )
        self.addLink( h1, router3, intfName2='r0-eth0', bw=1 )
        self.addLink( h1, router4, intfName2='r0-eth0', bw=1 )
        
        # Add link from Router to Router
        self.addLink( router1, router3, intfName1='r0-eth1', intfName2='r0-eth1' )
        self.addLink( router1, router4, intfName1='r0-eth2', intfName2='r0-eth2' )
        
        self.addLink( router2, router3, intfName1='r0-eth2', intfName2='r0-eth2' )
        self.addLink( router2, router4, intfName1='r0-eth1', intfName2='r0-eth1' )






# def initializeTopo():
#     print('Running Debug Mode')
#     os.system( 'mn --topo=mytopo' )
#     setLogLevel( 'info' )
    
# if __name__ == '__main__':
#     os.system( 'mn -c' )
#     print('==========================================================================')
#     setLogLevel( 'info' )
