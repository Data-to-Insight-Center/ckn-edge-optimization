// Create without Deployment nodes
// Create Edge Servers with coordinates (latitude and longitude) and IP address
CREATE (es1:EdgeServer {name:'Server-1', bandwidth: '100Gbps', location: 'MESH_158A', status: 'ACTIVE', latitude: 40.7128, longitude: -74.0060, ipAddress: '172.217.22.10'})
CREATE (es2:EdgeServer {name:'Server-2', bandwidth: '100Gbps', location: 'MESH_158B', status: 'ACTIVE', latitude: 34.0522, longitude: -118.2437, ipAddress: '172.217.22.11'})
CREATE (es3:EdgeServer {name:'Server-3', bandwidth: '100Gbps', location: 'MESH_158C', status: 'ACTIVE', latitude: 41.8781, longitude: -87.6298, ipAddress: '172.217.22.12'})


// Create Edge Devices with coordinates for each Edge Server
CREATE (ed1:EdgeDevice {name:'Device-1', location: 'MESH_158A', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 41.7137, longitude: -71.1059})
CREATE (ed2:EdgeDevice {name:'Device-2', location: 'MESH_158A', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 42.7146, longitude: -72.2061})
CREATE (ed3:EdgeDevice {name:'Device-3', location: 'MESH_158A', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 43.7155, longitude: -73.0062})
CREATE (ed4:EdgeDevice {name:'Device-4', location: 'MESH_158B', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 34.0522, longitude: -119.2437})
CREATE (ed5:EdgeDevice {name:'Device-5', location: 'MESH_158B', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 35.0532, longitude: -116.2437})
CREATE (ed6:EdgeDevice {name:'Device-6', location: 'MESH_158B', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 36.0542, longitude: -113.2437})
CREATE (ed7:EdgeDevice {name:'Device-7', location: 'MESH_158C', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 47.8751, longitude: -82.6298})
CREATE (ed8:EdgeDevice {name:'Device-8', location: 'MESH_158C', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 48.8731, longitude: -85.6298})
CREATE (ed9:EdgeDevice {name:'Device-9', location: 'MESH_158C', bandwidth: '10Gbps', status: 'ACTIVE', latitude: 49.8721, longitude: -89.6298})


// Create Cloud Server
CREATE (cs:CloudServer {name: 'Cloud', ipAddress: '172.217.22.14'})


// Create Service
CREATE (service1:Service {name: 'Image Classification'})
CREATE (service2:Service {name: 'Sound Identification'})


// Create AI Models for each Service
CREATE (ai1:AIModel {name:'GoogLeNet', accuracy: 0.80, latency: 0.01, location: 'torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_1", pretrained=True)', type: 'cnn'})
CREATE (ai2:AIModel {name:'SqueezeNet', accuracy: 0.85, latency: 0.02, location: 'torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_1", pretrained=True)', type: 'cnn'})
CREATE (ai3:AIModel {name:'ShuffleNet', accuracy: 0.75, latency: 0.03, location: 'torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_1", pretrained=True)', type: 'cnn'})
CREATE (ai4:AIModel {name:'YAMNet', accuracy: 0.80, latency: 0.01, location: 'tensorflow_hub.load("https://tfhub.dev/google/yamnet/1")', type: 'cnn'})
CREATE (ai5:AIModel {name:'VGGish', accuracy: 0.85, latency: 0.02, location: 'tensorflow_hub.load("https://tfhub.dev/google/vggish/1")', type: 'cnn'})


// Connect AI Models with Services
CREATE (ai1)-[:USED_BY]->(service1)
CREATE (ai2)-[:USED_BY]->(service1)
CREATE (ai3)-[:USED_BY]->(service1)
CREATE (ai4)-[:USED_BY]->(service2)
CREATE (ai5)-[:USED_BY]->(service2)


// Connect Edge Server with Cloud Server
CREATE (es1)-[:CONNECTS_TO {distance: 20000, latency: 2000, timestamp: datetime()}]->(cs)
CREATE (es2)-[:CONNECTS_TO {distance: 25000, latency: 2500, timestamp: datetime()}]->(cs)
CREATE (es3)-[:CONNECTS_TO {distance: 30000, latency: 3000, timestamp: datetime()}]->(cs)


// Connect Edge Servers between each other
CREATE (es1)-[:CONNECTED_TO {distance: 1000, latency: 100, timestamp: datetime()}]->(es2)
CREATE (es2)-[:CONNECTED_TO {distance: 1000, latency: 100, timestamp: datetime()}]->(es1)
CREATE (es1)-[:CONNECTED_TO {distance: 1500, latency: 150, timestamp: datetime()}]->(es3)
CREATE (es3)-[:CONNECTED_TO {distance: 1500, latency: 150, timestamp: datetime()}]->(es1)
CREATE (es2)-[:CONNECTED_TO {distance: 1000, latency: 100, timestamp: datetime()}]->(es3)
CREATE (es3)-[:CONNECTED_TO {distance: 1000, latency: 100, timestamp: datetime()}]->(es2)


// Connect Edge Devices with Edge Server
CREATE (ed1)-[:CONNECTED_TO {distance: 500, latency: 10, timestamp: datetime()}]->(es1)
CREATE (ed2)-[:CONNECTED_TO {distance: 550, latency: 12, timestamp: datetime()}]->(es1)
CREATE (ed3)-[:CONNECTED_TO {distance: 600, latency: 15, timestamp: datetime()}]->(es1)
CREATE (ed4)-[:CONNECTED_TO {distance: 700, latency: 17, timestamp: datetime()}]->(es2)
CREATE (ed5)-[:CONNECTED_TO {distance: 800, latency: 19, timestamp: datetime()}]->(es2)
CREATE (ed6)-[:CONNECTED_TO {distance: 900, latency: 21, timestamp: datetime()}]->(es2)
CREATE (ed7)-[:CONNECTED_TO {distance: 100, latency: 3, timestamp: datetime()}]->(es3)
CREATE (ed8)-[:CONNECTED_TO {distance: 300, latency: 7, timestamp: datetime()}]->(es3)
CREATE (ed9)-[:CONNECTED_TO {distance: 500, latency: 10, timestamp: datetime()}]->(es3)


// Connect AI Models with Edge Server using Deployment nodes
CREATE (ai1)-[:DEPLOYED_ON {start_time: datetime(), end_time: datetime() + duration('PT1H'), accuracy: 0.80, cpu_watt: 8.369286, gpu_watt: 48.57,  pid: "337263", process: "python"}]->(es1)

CREATE (ai1)-[:DEPLOYED_ON {start_time: datetime(), end_time: datetime() + duration('PT1H'), accuracy: 0.72, cpu_watt: 8.153751, gpu_watt: 47.49, pid: "337263", process: "python"}]->(es1)

CREATE (ai2)-[:DEPLOYED_ON {start_time: datetime(), end_time: datetime() + duration('PT1H'), accuracy: 0.89, cpu_watt: 7.726121, gpu_watt: 53.4, pid: "337263", process: "python"}]->(es1)

CREATE (ai4)-[:DEPLOYED_ON {start_time: datetime(), end_time: datetime() + duration('PT1H'), accuracy: 0.53, cpu_watt: 8.300131, gpu_watt: 47.5, pid: "337263", process: "python"}]->(es2)