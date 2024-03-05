//Health Queries
MATCH (deployment:Deployment)-[:DEPLOYED_ON]->(server)
WHERE server.name = 'Server-1'
RETURN deployment.start_time AS Start_Time, deployment.end_time AS End_Time, deployment.cpu_watt AS CPU_Watt, deployment.gpu_watt AS GPU_Watt, deployment.pid AS PID, deployment.process AS Process_Name, deployment.accuracy AS Accuracy
