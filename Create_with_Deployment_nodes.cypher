// Create with Deployment nodes
// Create Edge Servers with coordinates (latitude and longitude) and IP address
CREATE (es1:EdgeServer {id: 1, name:'Server-1', location: 'MESH_158A', status: 'ACTIVE', latitude: 40.7128, longitude: -74.0060, ipAddress: '172.217.22.10'})
CREATE (es2:EdgeServer {id: 2, name:'Server-2', location: 'MESH_158B', status: 'ACTIVE', latitude: 34.0522, longitude: -118.2437, ipAddress: '172.217.22.11'})
CREATE (es3:EdgeServer {id: 3, name:'Server-3', location: 'MESH_158C', status: 'INACTIVE', latitude: 41.8781, longitude: -87.6298, ipAddress: '172.217.22.12'})


// Create Edge Devices with coordinates for each Edge Server
CREATE (ed1:EdgeDevice {id: 1, name:'Device-1', location: 'MESH_158A', status: 'ACTIVE', latitude: 41.7137, longitude: -71.1059})
CREATE (ed2:EdgeDevice {id: 2, name:'Device-2', location: 'MESH_158A', status: 'ACTIVE', latitude: 42.7146, longitude: -72.2061})
CREATE (ed3:EdgeDevice {id: 3, name:'Device-3', location: 'MESH_158A', status: 'ACTIVE', latitude: 43.7155, longitude: -73.0062})
CREATE (ed4:EdgeDevice {id: 4, name:'Device-4', location: 'MESH_158B', status: 'ACTIVE', latitude: 34.0522, longitude: -119.2437})
CREATE (ed5:EdgeDevice {id: 5, name:'Device-5', location: 'MESH_158B', status: 'ACTIVE', latitude: 35.0532, longitude: -116.2437})
CREATE (ed6:EdgeDevice {id: 6, name:'Device-6', location: 'MESH_158B', status: 'ACTIVE', latitude: 36.0542, longitude: -113.2437})
CREATE (ed7:EdgeDevice {id: 7, name:'Device-7', location: 'MESH_158C', status: 'ACTIVE', latitude: 47.8751, longitude: -82.6298})
CREATE (ed8:EdgeDevice {id: 8, name:'Device-8', location: 'MESH_158C', status: 'ACTIVE', latitude: 48.8731, longitude: -85.6298})
CREATE (ed9:EdgeDevice {id: 9, name:'Device-9', location: 'MESH_158C', status: 'ACTIVE', latitude: 49.8721, longitude: -89.6298})


// Create Cloud Server
CREATE (cs:CloudServer {id: 1, name: 'Cloud', ipAddress: '172.217.22.14'})


// Create Service
CREATE (service1:Service {id: 1, name: 'Image Classification'})
CREATE (service2:Service {id: 2, name: 'Sound Identification'})


// Create AI Models for each Service
CREATE (ai1:AIModel {id: 1, name:'GoogLeNet', accuracy: 0.80, latency: 0.01, location: 'torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_1", pretrained=True)', type: 'cnn'})
CREATE (ai2:AIModel {id: 2, name:'SqueezeNet', accuracy: 0.85, latency: 0.02, location: 'torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_1", pretrained=True)', type: 'cnn'})
CREATE (ai3:AIModel {id: 3, name:'ShuffleNet', accuracy: 0.75, latency: 0.03, location: 'torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_1", pretrained=True)', type: 'cnn'})
CREATE (ai4:AIModel {id: 4, name:'YAMNet', accuracy: 0.80, latency: 0.01, location: 'tensorflow_hub.load("https://tfhub.dev/google/yamnet/1")', type: 'cnn'})
CREATE (ai5:AIModel {id: 5, name:'VGGish', accuracy: 0.85, latency: 0.02, location: 'tensorflow_hub.load("https://tfhub.dev/google/vggish/1")', type: 'cnn'})


// Connect AI Models with Services
CREATE (ai1)-[:USED_BY]->(service1)
CREATE (ai2)-[:USED_BY]->(service1)
CREATE (ai3)-[:USED_BY]->(service1)
CREATE (ai4)-[:USED_BY]->(service2)
CREATE (ai5)-[:USED_BY]->(service2)


// Connect Edge Server with Cloud Server
CREATE (es1)-[:CONNECTS_TO {distance: 20000, latency: 2000, bandwidth: '100Gbps', timestamp: datetime()}]->(cs)
CREATE (es2)-[:CONNECTS_TO {distance: 25000, latency: 2500, bandwidth: '100Gbps', timestamp: datetime()}]->(cs)
CREATE (es3)-[:CONNECTS_TO {distance: 30000, latency: 3000, bandwidth: '100Gbps', timestamp: datetime()}]->(cs)


// Connect Edge Servers between each other
CREATE (es1)-[:CONNECTED_TO {distance: 1000, latency: 100, bandwidth: '10Gbps', timestamp: datetime()}]->(es2)
CREATE (es2)-[:CONNECTED_TO {distance: 1000, latency: 100, bandwidth: '10Gbps', timestamp: datetime()}]->(es1)
CREATE (es1)-[:CONNECTED_TO {distance: 1500, latency: 150, bandwidth: '10Gbps', timestamp: datetime()}]->(es3)
CREATE (es3)-[:CONNECTED_TO {distance: 1500, latency: 150, bandwidth: '10Gbps', timestamp: datetime()}]->(es1)
CREATE (es2)-[:CONNECTED_TO {distance: 1000, latency: 100, bandwidth: '10Gbps', timestamp: datetime()}]->(es3)
CREATE (es3)-[:CONNECTED_TO {distance: 1000, latency: 100, bandwidth: '10Gbps', timestamp: datetime()}]->(es2)


// Connect Edge Devices with Edge Server
CREATE (ed1)-[:CONNECTED_TO {distance: 500, latency: 10, bandwidth: '50Gbps', timestamp: datetime()}]->(es1)
CREATE (ed2)-[:CONNECTED_TO {distance: 550, latency: 12, bandwidth: '50Gbps', timestamp: datetime()}]->(es1)
CREATE (ed3)-[:CONNECTED_TO {distance: 600, latency: 15, bandwidth: '50Gbps', timestamp: datetime()}]->(es1)
CREATE (ed4)-[:CONNECTED_TO {distance: 700, latency: 17, bandwidth: '50Gbps', timestamp: datetime()}]->(es2)
CREATE (ed5)-[:CONNECTED_TO {distance: 800, latency: 19, bandwidth: '50Gbps', timestamp: datetime()}]->(es2)
CREATE (ed6)-[:CONNECTED_TO {distance: 900, latency: 21, bandwidth: '50Gbps', timestamp: datetime()}]->(es2)
CREATE (ed7)-[:CONNECTED_TO {distance: 100, latency: 3, bandwidth: '50Gbps', timestamp: datetime()}]->(es3)
CREATE (ed8)-[:CONNECTED_TO {distance: 300, latency: 7, bandwidth: '50Gbps', timestamp: datetime()}]->(es3)
CREATE (ed9)-[:CONNECTED_TO {distance: 500, latency: 10, bandwidth: '50Gbps', timestamp: datetime()}]->(es3)

// Assuming AI Models and Edge Servers are correctly identified by their `id` property

// Define a list of deployments with attributes
WITH [
  {aiId: 2, esId: 2, startTime: "2022-05-22T00:00:00", endTime: "2022-05-22T01:00:00", accuracy: 0.78, cpuWatt: 8.6, gpuWatt: 49.5, pid: "337266", process: "python"},
  {aiId: 2, esId: 2, startTime: "2022-05-23T01:00:00", endTime: "2022-05-23T02:00:00", accuracy: 0.79, cpuWatt: 8.7, gpuWatt: 51.0, pid: "337267", process: "python"},
  {aiId: 3, esId: 1, startTime: "2022-05-24T02:00:00", endTime: "2022-05-24T03:00:00", accuracy: 0.80, cpuWatt: 8.8, gpuWatt: 52.0, pid: "337268", process: "python"},
  {aiId: 3, esId: 1, startTime: "2022-05-25T03:00:00", endTime: "2022-05-25T04:00:00", accuracy: 0.81, cpuWatt: 9.0, gpuWatt: 53.0, pid: "337269", process: "python"},
  {aiId: 4, esId: 1, startTime: "2022-05-26T04:00:00", endTime: "2022-05-26T05:00:00", accuracy: 0.82, cpuWatt: 9.1, gpuWatt: 54.0, pid: "337270", process: "python"},
  {aiId: 4, esId: 1, startTime: "2022-05-27T05:00:00", endTime: "2022-05-27T06:00:00", accuracy: 0.83, cpuWatt: 9.2, gpuWatt: 55.0, pid: "337271", process: "python"},
  {aiId: 5, esId: 2, startTime: "2022-05-28T06:00:00", endTime: "2022-05-28T07:00:00", accuracy: 0.84, cpuWatt: 9.3, gpuWatt: 56.0, pid: "337272", process: "python"},
  {aiId: 5, esId: 2, startTime: "2022-05-29T07:00:00", endTime: "2022-05-29T08:00:00", accuracy: 0.85, cpuWatt: 9.4, gpuWatt: 57.0, pid: "337273", process: "python"},
  {aiId: 1, esId: 1, startTime: "2022-05-30T08:00:00", endTime: "2022-05-30T09:00:00", accuracy: 0.86, cpuWatt: 9.5, gpuWatt: 58.0, pid: "337274", process: "python"},
  {aiId: 1, esId: 1, startTime: "2022-05-31T09:00:00", endTime: "2022-05-31T10:00:00", accuracy: 0.87, cpuWatt: 9.6, gpuWatt: 59.0, pid: "337275", process: "python"},
    {aiId: 2, esId:1, startTime: "2022-06-05T20:00:00", endTime: "2022-06-05T21:00:00", accuracy: 0.98, cpuWatt: 10.8, gpuWatt: 70.0, pid: "337286", process: "python"},
  {aiId: 2, esId: 1, startTime: "2022-06-20T22:00:00", endTime: "2022-06-20T23:00:00", accuracy: 0.99, cpuWatt: 10.9, gpuWatt: 71.0, pid: "337287", process: "python"},
  {aiId: 3, esId: 1, startTime: "2022-06-01T00:00:00", endTime: "2022-06-01T01:00:00", accuracy: 0.78, cpuWatt: 11.0, gpuWatt: 72.0, pid: "337288", process: "python"},
  {aiId: 3, esId: 1, startTime: "2022-06-16T02:00:00", endTime: "2022-06-16T03:00:00", accuracy: 0.79, cpuWatt: 11.1, gpuWatt: 73.0, pid: "337289", process: "python"},
  {aiId: 4, esId: 2, startTime: "2022-06-03T04:00:00", endTime: "2022-06-03T05:00:00", accuracy: 0.80, cpuWatt: 11.2, gpuWatt: 74.0, pid: "337290", process: "python"},
  {aiId: 4, esId: 2, startTime: "2022-06-18T06:00:00", endTime: "2022-06-18T07:00:00", accuracy: 0.81, cpuWatt: 11.3, gpuWatt: 75.0, pid: "337291", process: "python"},
  {aiId: 5, esId: 1, startTime: "2022-06-06T08:00:00", endTime: "2022-06-06T09:00:00", accuracy: 0.82, cpuWatt: 11.4, gpuWatt: 76.0, pid: "337292", process: "python"},
  {aiId: 5, esId: 1, startTime: "2022-06-21T10:00:00", endTime: "2022-06-21T11:00:00", accuracy: 0.83, cpuWatt: 11.5, gpuWatt: 77.0, pid: "337293", process: "python"},
  {aiId: 1, esId: 1, startTime: "2022-06-08T12:00:00", endTime: "2022-06-08T13:00:00", accuracy: 0.84, cpuWatt: 11.6, gpuWatt: 78.0, pid: "337294", process: "python"},
  {aiId: 1, esId: 1, startTime: "2022-06-23T14:00:00", endTime: "2022-06-23T15:00:00", accuracy: 0.85, cpuWatt: 11.7, gpuWatt: 79.0, pid: "337295", process: "python"}
] AS deployments
UNWIND deployments AS dep
// Ensure AI models are matched correctly, possibly correcting the label or property if necessary
MATCH (ai:AIModel {id: dep.aiId})
// Ensure Edge Servers are matched correctly
MATCH (es:EdgeServer {id: dep.esId})
// Create Deployment nodes and relationships
CREATE (deployment:Deployment {
  start_time: datetime(dep.startTime), 
  end_time: datetime(dep.endTime), 
  accuracy: dep.accuracy, 
  cpu_watt: dep.cpuWatt, 
  gpu_watt: dep.gpuWatt,  
  pid: dep.pid, 
  process: dep.process
})
CREATE (ai)-[:HAS_DEPLOYMENT]->(deployment)
CREATE (deployment)-[:DEPLOYED_ON]->(es)