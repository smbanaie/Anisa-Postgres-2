# Highly Available PostgreSQL Cluster using Patroni and HAProxy

![](Images\postgres_streaming.jpg)

### **Introduction:**

High availability is a vital part of today’s architecture and modern systems. This blog post describes a possible approach to create a highly available PostgreSQL cluster using Patroni and HAProxy. The high availability allows a PostgreSQL DB node to automatically reroute work to another available PostgreSQL DB node in case of a failure. It’s important to note that this blog is not associated with JFrog products, but rather my personal experience.

## Who is the Leader? 

![](.\Images\Julian_Patroni_Blogpost_V2.png)



### HA Proxy 

![](Images\PatroniDiagram.jpeg)

#### Full Architecture

![](Images\typea.png)



#### Notes

Use official patroni repository to setup a test cluster 

	- use `docker build -t patroni .` to create the patroni image
	- add HAProxy web UI to the docker compose `7000:7000`
	- use WSL to run the cluster (it has some issues in windows (line ending in some bash scripts))
