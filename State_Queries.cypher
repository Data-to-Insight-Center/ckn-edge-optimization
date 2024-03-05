// State Queries
MATCH (deployment:Deployment)-[:DEPLOYED_ON]->(server),
      (aiModel:AIModel)-[:HAS_DEPLOYMENT]->(deployment)
WHERE server.name = 'Server-1'
AND date(deployment.start_time) >= date("2022-05-01")
AND date(deployment.start_time) <= date("2022-06-30")

RETURN deployment.start_time AS Start_Time, 
       deployment.end_time AS End_Time,
       (duration.between(deployment.start_time, deployment.end_time).minutes) AS Duration_Minutes, 
       deployment.cpu_watt AS CPU_Watt, 
       deployment.gpu_watt AS GPU_Watt, 
       deployment.pid AS PID, 
       deployment.process AS Process_Name, 
       deployment.accuracy AS Accuracy,
       aiModel.name AS Model_Name
