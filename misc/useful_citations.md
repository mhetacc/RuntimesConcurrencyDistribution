## Byzantine Generals Problem - Leslie Lamport
### §6: Reliable Systems
https://www.microsoft.com/en-us/research/uploads/prod/2016/12/The-Byzantine-Generals-Problem.pdf
> [...] the only way we know to implement a reliable computer system is to use several different "processors" to compute the same result, and then to perform a majority vote on their outputs to obtain a single value. [...] \
This is true whether one is implementing a reliable computer using redundant circuitry to protect against the failure of individual chips, or a ballistic missile defense system using redundant computing sites to protect against the destruction of individual sites by a nuclear attack.

## Python Wikipedia
https://en.wikipedia.org/wiki/Python_(programming_language)[[https://www.roundhillinvestments.com/etf/nerd/?utm_source=vcweb&utm_medium=datastream&utm_id=viscap-roundhill  ](https://www.visualcapitalist.com/sp/video-games-industry-revenue-growth-visual-capitalist/#:~:text=The%20Industry's%20Revenue%20Model,%2C%20and%20PUBG%2C%20are%20F2P.)](https://www.visualcapitalist.com/sp/video-games-industry-revenue-growth-visual-capitalist/#:~:text=The%20Industry's%20Revenue%20Model,%2C%20and%20PUBG%2C%20are%20F2P.)
70bln revenue  should be one—and preferably only one—obvious way to do it." philosophy
In practice, however, Python provides many ways to achieve the same task. There are, for example, at least three ways to format a string literal, with no certainty as to which one a programmer should use.

## Python Docs Tutorial
https://docs.python.org/3.12/tutorial/stdlib.html#batteries-included[]([[about:reader?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FConsensus_(computer_science)#cite_note-aguilera_stumbling-4](https://link.springer.com/chapter/10.1007/978-3-642-11294-2_4)](https://link.springer.com/chapter/10.1007/978-3-642-11294-2_4))
## Realpython on asyncio
https://realpython.com/async-io-python/

Coroutines are repurposed generators that take advantage of the peculiarities of generator methods.

## Consensus and Distributed Systems
Key characteristic of a distributed system:
- scalability
- concurrency
- availability
- transparency 

In the most traditional single-value consensus protocols such as Paxos, cooperating nodes agree on a single value such as an integer, while in multi-valued consensus protocols such as Multi-Paxos and Raft, the goal is to agree on not just a single value but a series of values over time, forming a progressively-growing history

## Asynchrony
https://link.springer.com/chapter/10.1007/978-3-642-11294-2_4 
While real world communications are often inherently asynchronous, it is more practical and often easier to model synchronous systems 

## FLP impossibility result
https://dl.acm.org/doi/10.1145/3149.214121

a deterministic algorithm for achieving consensus is impossible.
This impossibility result derives from worst-case scheduling scenarios, which are unlikely to occur in practice except in adversarial situations such as an intelligent denial-of-service attacker in the network. In most normal situations, process scheduling has a degree of natural randomness

## Randomized consensus 
https://www.sciencedirect.com/science/article/abs/pii/S0196677483710229?via%3Dihub
Randomized consensus algorithms can circumvent the FLP impossibility result by achieving both safety and liveness with overwhelming probability, even under worst-case scheduling scenarios such as an intelligent denial-of-service attacker in the network

## Gaming
https://www.statista.com/outlook/amo/media/games/online-games/worldwide

Revenue in the Online Games market in the world is projected to reach US$29.48bn in 2025.

In the Online Games market in the world, the number of users is expected to amount to 1.3bn users by 2030.


Oss: data differs between different sources, point is: everyone agrees that most revenue is made by free to play games, which gain revenue by selling things trough web services 

https://www.statista.com/statistics/324129/arpu-f2p-mmo/#:~:text=Free%2Dto%2Dplay%20(F2P)%20games%20market%20revenue%20worldwide,2024%20(in%20billion%20U.S.%20dollars)&text=Data%20from%202022%20onwards%20are,was%20published%20by%20SuperData%20Research.
In 2023, F2P games have generated around $111.37 billion worldwide

https://www.visualcapitalist.com/sp/video-games-industry-revenue-growth-visual-capitalist/#:~:text=The%20Industry's%20Revenue%20Model,%2C%20and%20PUBG%2C%20are%20F2P.

70bln revene social/casual gaming -> intertwined with web

https://best-of-gaming.be/wp-content/uploads/2024/09/2024_Newzoo_Global_Games_Market_Report.pdf
In 2024, the revenue from the worldwide gaming market was 187.7bln

https://www.pwc.com/gx/en/news-room/press-releases/2025/pwc-global-entertainment-media-outlook.html
Global entertainment and media industry revenues to hit US$3.5 trillion by 2029, driven by advertising, live events, and video games: PwC Global Entertainment & Media Outlook 

## Distributed computing
https://www.distributed-systems.net/index.php/books/ds3/
https://link.springer.com/chapter/10.1007/978-1-84882-745-5_11



Distributed computing is a field of computer science that studies distributed systems, defined as computer systems whose inter-communicating components are located on different networked computers.