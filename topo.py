# -*- coding: utf-8 -*-
from mininet.topo import Topo

class MaTopologie(Topo):
    def build(self):
        # Creation des switchs
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Creation des hotes
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Connexion des hotes aux switchs
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)

        # Connexion des switchs entre eux
        self.addLink(s1, s2)
        self.addLink(s2, s3)

# Definition de la topologie pour Mininet
topos = { 'matopo': (lambda: MaTopologie()) }