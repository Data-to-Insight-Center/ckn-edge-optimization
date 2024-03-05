//Reproducibililty queries
MATCH (n)
WHERE n:EdgeServer OR n:EdgeDevice
RETURN DISTINCT n.name AS Name, n.status AS Status