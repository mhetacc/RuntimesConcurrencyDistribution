## Raft-using products and services
### CockroachDB
https://en.wikipedia.org/wiki/CockroachDB
CockroachDB stores copies of data in multiple locations to deliver quick access
It is described as a scalable, consistently-replicated, transactional data store.[14]
https://www.informationweek.com/software-services/cockroachdb-ultimate-in-database-survival
"Consistency is very important. But consistency is very, very hard," Kimball said.
*eventual consistency*: for NoSQL systems. The user can't be sure the information used in an attempted transaction reflects the most recent changes
CockroachDB [...] If new servers are **added to the cluster**, it recognizes the fact, propagates data to them, and adds it to its processing operations. 
https://www.cockroachlabs.com/docs/v24.2/architecture/replication-layer#raft
makes sure that your data is safely stored on multiple machines, and that those machines agree on the current state even if some of them are temporarily disconnected.
Raft organizes all nodes that contain a replica of a *range* (ie maps of key-value pairs)
**so: Raft manges duplicated db descriptors**

### Consul
https://developer.hashicorp.com/consul
![](https://developer.hashicorp.com/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1679087694-devdot-consul_dm.png&w=3840&q=75&dpl=dpl_AHEeipEXds2r9yyJk3CRHnRaQC9s)
manage secure network connectivity between services and across multi-cloud environments and runtimes
https://developer.hashicorp.com/consul/docs/architecture/consensus
Consul uses a consensus protocol to provide Consistency 
in Consul's case, we use MemDB to maintain cluster state. Consul's writes block until it is both committed and applied. This achieves read after write semantics when used with the consistent mode for queries.
Consensus is fault-tolerant up to the point where **quorum** is available: suppose there are only 2 peers: A and B. The quorum size is also 2, meaning both nodes must agree to commit a log entry. If either A or B fails, it is now impossible to reach quorum. At this point, manual intervention would be required 
Only Consul server nodes participate in Raft, as more members are added the size of the quorum also increases
When getting started, a single Consul server is put into "**bootstrap**" mode. This mode allows it to self-elect as a leader. Once a leader is elected, other servers can be added to the peer set in a way that preserves consistency and safety. Eventually, bootstrap mode can be disabled

| Servers | Quorum | Failure Tolerance |
| :-: | :-: | :-: |
|5|2|2|
|6|4|2|
|7|4|3|