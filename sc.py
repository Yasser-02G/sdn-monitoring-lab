# -*- coding: utf-8 -*-
import time
import requests
from influxdb import InfluxDBClient

AUTH = ('admin', 'admin')
HEADERS = {'Accept': 'application/json'}
# Assurez-vous que la base 'sdn_monitor' existe
INFLUX_CLIENT = InfluxDBClient(host='localhost', port=8086, database='sdn_monitor')

def get_stats():
    try:
        # 1. Topologie
        url_topo = "http://localhost:8181/rests/data/network-topology:network-topology"
        res_topo = requests.get(url_topo, auth=AUTH, headers=HEADERS, timeout=5).json()
        links = res_topo['network-topology:network-topology']['topology'][0].get('link', [])
        
        points = []
        for link in links:
            points.append({
                "measurement": "topology_links",
                "tags": {"source": link['source']['source-node'], "target": link['destination']['dest-node']},
                "fields": {"exists": 1}
            })

        # 2. Trafic (Stats ports)
        url_stats = "http://localhost:8181/rests/data/opendaylight-inventory:nodes"
        res_stats = requests.get(url_stats, auth=AUTH, headers=HEADERS, timeout=5).json()
        
        # Simple exemple : compter le total des paquets reçus (à ajuster selon votre JSON)
        # Ici on envoie un point par switch pour l'exemple
        points.append({
            "measurement": "network_data",
            "fields": {"received_packets": 22, "total_nodes": len(res_topo['network-topology:network-topology']['topology'][0].get('node', []))}
        })

        if points:
            INFLUX_CLIENT.write_points(points)
            print("Données envoyées avec succès.")
            
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    while True:
        get_stats()
        time.sleep(10)