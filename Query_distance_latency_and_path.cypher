//Query distance, latency, and path
WITH 'Device-1' AS startName, 'Server-3' AS endName
MATCH (startNode)-[:CONNECTED_TO*]-(endNode)
WHERE startNode.name = startName AND endNode.name = endName
MATCH path = shortestPath((startNode)-[:CONNECTED_TO*]-(endNode))
RETURN path, reduce(distanceSum = 0, r in relationships(path) | distanceSum + r.latency) AS TotalLatency, reduce(distanceSum = 0, r in relationships(path) | distanceSum + r.distance) AS TotalDistance
