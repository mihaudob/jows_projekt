#!/usr/bin/python

"""
linuxrouter.py: Example network with Linux IP router
This example converts a Node into a router using IP forwarding
already built into Linux.
The example topology creates a router and three IP subnets:
    - 192.168.1.0/24 (r0-eth1, IP: 192.168.1.1)
    - 172.16.0.0/12 (r0-eth2, IP: 172.16.0.1)
    - 10.0.0.0/8 (r0-eth3, IP: 10.0.0.1)
Each subnet consists of a single host connected to
a single switch:
    r0-eth1 - s1-eth1 - h1-eth0 (IP: 192.168.1.100)
    r0-eth2 - s2-eth1 - h2-eth0 (IP: 172.16.0.100)
    r0-eth3 - s3-eth1 - h3-eth0 (IP: 10.0.0.100)
The example relies on default routing entries that are
automatically created for each router interface, as well
as 'defaultRoute' parameters for the host interfaces.
Additional routes may be added to the router or hosts by
executing 'ip route' or 'route' commands on the router or hosts.
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):
        info( '*** Setup of IP adresses\n' )
        r1_IP = '192.168.1.1/24'  # IP address for r0-eth1
        r2_IP = '192.168.2.1/24'  # IP address for r0-eth1
        r3_IP = '192.168.3.1/24'  # IP address for r0-eth1

        info( '*** Creating Routers\n' )
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip=r1_IP )
        r2 = self.addNode( 'r2', cls=LinuxRouter, ip=r2_IP )
        r3 = self.addNode( 'r3', cls=LinuxRouter, ip=r3_IP )
     

        info( '*** Creating Switches\n' )
        s1, s2, s3 = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        info( '*** Linking Switches\n' )
        self.addLink( s1, r1, intfName2='r1-eth1',
                      params2={ 'ip' : r1_IP } ) 
        self.addLink( s2, r2, intfName2='r2-eth1',
                      params2={ 'ip' : r2_IP } )
        self.addLink( s3, r3, intfName2='r3-eth1',
                      params2={ 'ip' : r3_IP } )

        info( '*** Creating Hosts\n' )
        h11 = self.addHost( 'h11', ip='192.168.1.11/24',
                           defaultRoute='via 192.168.1.1' )
        h12 = self.addHost( 'h12', ip='192.168.1.12/24',
                           defaultRoute='via 192.168.1.1' )

        h21 = self.addHost( 'h21', ip='192.168.2.21/24',
                           defaultRoute='via 192.168.2.1' )
        h22 = self.addHost( 'h22', ip='192.168.2.22/24',
                           defaultRoute='via 192.168.2.1' )

        h31 = self.addHost( 'h31', ip='192.168.3.31/24',
                           defaultRoute='via 192.168.3.1' )
        h32 = self.addHost( 'h32', ip='192.168.3.32/24',
                           defaultRoute='via 192.168.3.1' )

        info( '*** Linking Hosts\n' )
        for h, s in [ (h12, s1), (h11, s1)]:
            self.addLink( h, s )

        for h, s in [ (h22, s2), (h21, s2)]:
            self.addLink( h, s )

        for h, s in [ (h32, s3), (h31, s3)]:
            self.addLink( h, s )

        info( '*** Linking Routers\n' )
        self.addLink( r1, r2,
                    intfName1='r1-eth2',
                    params1={ 'ip' : '192.168.12.1/24'},
                    intfName2='r2-eth2',
                    params2={ 'ip' : '192.168.12.2/24' } )  

        self.addLink( r2, r3,
                    intfName1='r2-eth3',
                    params1={ 'ip' : '192.168.23.2/24'},
                    intfName2='r3-eth3',
                    params2={ 'ip' : '192.168.23.3/24' } )  

        self.addLink( r3, r1,
                    intfName1='r3-eth2',
                    params1={ 'ip' : '192.168.31.3/24'},
                    intfName2='r1-eth3',
                    params2={ 'ip' : '192.168.31.1/24' } )  
def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Routers:\n' )
    info( net[ 'r1' ].cmd( 'ip route add 192.168.2.0/24 via 192.168.12.2 dev r1-eth2' ) )
    info( net[ 'r1' ].cmd( 'ip route add 192.168.3.0/24 via 192.168.31.3 dev r1-eth3' ) )
    info( net[ 'r1' ].cmd( 'route' ) )

    info( net[ 'r2' ].cmd( 'ip route add 192.168.1.0/24 via 192.168.12.1 dev r2-eth2' ) )
    info( net[ 'r2' ].cmd( 'ip route add 192.168.3.0/24 via 192.168.23.3 dev r2-eth3' ) )
    info( net[ 'r2' ].cmd( 'route' ) )

    info( net[ 'r3' ].cmd( 'ip route add 192.168.1.0/24 via 192.168.31.1 dev r3-eth2' ) )
    info( net[ 'r3' ].cmd( 'ip route add 192.168.2.0/24 via 192.168.23.2 dev r3-eth3' ) )
    info( net[ 'r3' ].cmd( 'route' ) )    

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
