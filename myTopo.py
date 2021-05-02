#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Node

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


# Jangan lupa selesaikan ini!        
class PC1( Node ):
    def config( self, **params ):
        super( Router4, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.1.2/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 192.168.100.7/24 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 192.168.100.8/24 brd + dev r0-eth2' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router4, self ).terminate()
        
class PC2( Node ):
    def config( self, **params ):
        super( Router4, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'ip addr add 192.168.1.2/24 brd + dev r0-eth0' )
        self.cmd( 'ip addr add 192.168.100.7/24 brd + dev r0-eth1' )
        self.cmd( 'ip addr add 192.168.100.8/24 brd + dev r0-eth2' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router4, self ).terminate()

def myNet():
    net = Mininet(build=False, ipBase='192.168.0.0/23')
    
    print("Creating Router")
    # Checkpoint! 03-05-2021 00:14,
    # Belum selesai Ngebuat Host berdasarkan kelas2nya
    # Ikuti contoh dari ./module_example/gachiemhiep.py
    # Setelah buat host router, buat host computer dengan kelas PC1 dan PC2
    r1 = net.addHost('r1', cls=Router1, ip='192.168.0.1/24')
    r1 = net.addHost('r1', cls=Router1, ip='192.168.0.2/24')
    r1 = net.addHost('r1', cls=Router1, ip='192.168.0.1/24')
    r1 = net.addHost('r1', cls=Router1, ip='192.168.0.1/24')
    
if __name__=='__init__':
    # global net
    info( 'Initializing Mininet' )
    Mininet.init()
    myNet()