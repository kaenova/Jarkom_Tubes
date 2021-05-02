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


def myNetwork():
    net = Mininet ( Topo=None,
                    build=False,
                    ipBase='192.168.0.0/24')