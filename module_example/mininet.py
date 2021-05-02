from mininet.link import TCLink	# Import lib link dari mininet
from mininet.topo import Topo		# Import lib topo dari mininet

class MyTopo(Topo):			# Buat kelas MyTopo
    def build(self):			# Buat function build
	# Buat host dengan nama 'hX' dan ip '192.168.1.X' dan mac addr '90:40:10:00:00:0X' 
        h1 = self.addHost('h1', ip='192.168.1.1/24', mac='90:40:10:00:00:01')
        h2 = self.addHost('h2', ip='192.168.1.2/24', mac='90:40:10:00:00:02')
        h3 = self.addHost('h3', ip='192.168.1.3/24', mac='90:40:10:00:00:03')
        h4 = self.addHost('h4', ip='192.168.1.4/24', mac='90:40:10:00:00:04')
        h5 = self.addHost('h5', ip='192.168.1.5/24', mac='90:40:10:00:00:05')

	# Buat switch dengan nama 'sX'
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

	# Buat option
        linkopt = {'bw': 20, 'delay': '10ms', 'loss': 5}
        
        # Menghubungkan link antara Host dan Switch
        self.addLink(s1, h1, cls=TCLink, **linkopt)	# (s1, h1)
        self.addLink(s1, h2, cls=TCLink, **linkopt)	# (s1, h2)
        self.addLink(s2, h3, cls=TCLink, **linkopt)	# (s2, h3)
        self.addLink(s3, h4, cls=TCLink, **linkopt)	# (s3, h4)
        self.addLink(s4, h5, cls=TCLink, **linkopt)	# (s4, h5)
        self.addLink(s1, s2, cls=TCLink, **linkopt)	# (s1, s2)
        self.addLink(s2, s3, cls=TCLink, **linkopt)	# (s2, s3)
        self.addLink(s4, s1, cls=TCLink, **linkopt)	# (s4, s1)

topos = { 'mytopo': ( lambda: MyTopo() ) }
