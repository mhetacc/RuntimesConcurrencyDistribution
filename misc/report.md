*This document is not intended to be the actual final report, it is just a place to keep track of important information and intuitions that would otherwise be lost during the development of the project.*

---

# Design

Design philosophy of the infrastructure, from why a technology has been chosen instead of another, to the actual architecture.

## Requirements

Since the focus is showing a fun implementation of the Raft algorithm, a complex overhead is not needed i.e. there is no need to use advanced game engines with multiple languages involved (e.g. Godot, Unity, Cocos, etc.). \
It would be instead preferable to make the whole project with a single language, to simplify the programming process and we want our game to be 2D for ease of development. Moreover, we don't really care about portability since we are not making a "real" game. \
Hence, our **GUI-engine requirements** are:
 
1. One language
2. 2D graphics

This is all done to keep things outside "doing Raft" as simple as possible. Lets talk about **language requirements**:

1. Native RPC support
2. Native, bottom-up image processing support
 
By "bottom-up" we mean a "code-first" approach, i.e. instead of making the graphical elements first and then going down-to-code as-need for scripting, we want to start from the code in order to create the graphical components. \
This should facilitate the development process since we will "implant" the UI on our Raft elements which are, and should be, the better part of the project both in term of lines of code and complexity.

These conditions (for engines and languages) are both complementary and exclusive: if a language (eg Go) has a built-in image processing tool (eg Go's *image* module) a game engine might not be necessary.

## Technology  

### Programming Languages

Since this is a Computer Science project, of course it will be done using some (ideally one) programming languages. Which one is not a trivial choice. \
Having done a bit of research, it is clear that there are two extremely dominant languages in the world of computing right now, with no sign of slowing down ie:
1. JavaScript
2. Python
   
While, in the "serious" game development world, we can once again see two (three) languages coming on top:
1. JavaScript (scripting)
2. C++ (core engine)
3. C# (because of Unity)

It can be easily inferred that having a solid base in either of these three languages (JS, Python, C++) will be greatly beneficial.

Finally we cannot forget that we want to implement Raft, and the official page collect a lot of implementations in various languages, whose most popular (and supported) are:
1. C++
2. Java
3. Go

There are some implementation in Javascript and Python but not nearly as big or followed. 

### Game Engines 

Since the idea is to make a game, which would need a GUI (graphical user interface), it is likely easier to use an actual game engine instead of trying some workaround (eg command line tricks like [htop](https://htop.dev/)). 
![htop](https://htop.dev/images/htop-2.0.png)
Moreover, and perhaps more importantly, using an established game engine will yield valuable learning experience. \
We focused on open source game engines, both for ease of development, pedagogical and ethical reasons. \
Here follows the most interesting engines we found:

- ![](https://www.pygame.org/docs/_static/pygame_powered_lowres.png)[Pygame](https://www.pygame.org/news)
  - Python module for 2D games
  - Multi platform
  - Small community
- ![](https://cdn.phaser.io/images/logo/logo-download-vector.png) [Phaser](https://phaser.io/)
  - All JavaScript framework
  - Made for web browser 
  - 2D only
  - Can be used with TypeScript
  - It is a JavaScript library 
- ![](./imgs/godot_logo.png)https://godotengine.org/  
  - C++
  - VisualScript
  - Multi platform
- ![](./imgs/cocos_logo.png)https://www.cocos.com/en/cocos2d-x
  - C++
  - JavaScript
  - Python
  - Multi platform

Godot and Cocos are more "serious" engines, used to make a lot of famous and successful games but, at the same time, are of course more complex to use.

### gRPC

https://grpc.io/
gRPC is a modern open source high performance Remote Procedure Call (RPC) framework that can run in any environment. \
Used by:
- Google
- Netflix
- Slack
- Cisco
- Cockroach Labs
- and more

Uses **Protocol Buffer** which is a language and platform agnostic data passing mechanism which supports strong typing. \
These buffers are up to 5 times faster than JSON. \
Browsers still not support HTTP/2 primitives [(source)](https://learn.microsoft.com/en-us/aspnet/core/grpc/browser?view=aspnetcore-9.0) which gRPC relies upon, making it necessary to use a proxy called gRPC-web that does not provide all speed-up advantages of gRPC. \
**So where it is used?**  Microservices communications in data centers and in native mobile clients. 

### Putting Things Together  

- C++:
  - [xmlrpc](https://xmlrpc-c.sourceforge.io/) non-native RPCs support
  - [gRPC](https://github.com/grpc/grpc/tree/master) non-native high performance RPCs support
  - [Godot](https://godotengine.org/) top-down game engine
  - [wxWidget](https://www.wxwidgets.org/) native bottom-up UI 
- JavaScript:
  - [gRPC-web](https://github.com/grpc/grpc-web) non-native high performance RPCs support
  - [Phaser](https://phaser.io/) bottom-up game engine
  - HTML+CSS native bottom-up UI 
- Python:
  - [xmlrpc](https://docs.python.org/3/library/xmlrpc.html) native RPCs support
  - [Pygame](https://www.pygame.org/news) bottom-up game engine
  - [TkInter](https://docs.python.org/3/library/tkinter.html) native bottom-up UI support
  - [Dear PyGui](https://dearpygui.readthedocs.io/en/latest/) non-native bottom-up UI support

Python is the only language that has both:
1. Native RPCs support
2. Bottom-Up (code-first) UI approach

Hence it is the language of choice to make this project. 
Moreover: it is one of the most prominent languages today, without any sign of stopping in popularity, coveted by both companies and public institutions and it is also widely used in research, from data science to cyber security to machine learning and AI. Lastly, thanks to it being an interpreted language, considerable time during program development should be saved because no compilation and linking is necessary. \
The interpreter can be used interactively, which makes it easy to experiment with features of the language, to write throw-away programs, or to test functions during bottom-up program development.

## Components

The whole project sits on top of two core components:

- Raft nodes, which behave both like clients and servers
- A game loop that behaves like a client for the Raft cluster

### Game Loop

Each loop follows these steps:

1. checks Raft's log
2. compares its own local log to it
3. applies all Raft's committed commands locally
4. update local log 

By separating the logs we can separate local and server logics, leaving Raft free to do its own thing while the game runs. It will probably be necessary to run game loop and Raft loop in separate threads.

We need just three commands:

1. `X attack Y`: player X attack player Y
2. `add Z`: new player Z joined
3. `del Z`: player Z left the lobby

The engine then handles everything locally: it does not need to communicate all changes to the Raft cluster. What it needs to communicate is its intention to attack another player.

Every action must pass through the Leader: lets imagine player Alice wants to attack player Bob:

1. Alice sends RPC to Leader "Alice attacks Bob"
2. Leader propagates "Alice attacks Bob" to the whole cluster
3. Once RPC is committed, Alice checks its Raft log and compares it to its own local log
4. Updates Bob's health points
5. Adds "Alice attacks Bob" to local log

If a server *Z* wants out, it can simply shut down on its own. Once Leader does not receive ack after heartbeat it will broadcast `del Z` to the whole cluster (Z included) before removing it from its list of alive servers. If Z then wakes up it can just ask Leader to be re-admitted. Admission is considered done once `add Z` is committed.   

### Raft



# Development

## User Interface

### Technologies Showdown

To produce the wanted results with **Tkinter**, ie making an app in the guise of a game, two components are needed:

- a geometry manger between:
  - tkinter.pack
  - tkinter.place
  - tkinter.grid
- tkinter.canvas

The idea is to use canvases as the various windows of our game, since they allow us extreme flexibility and control on what to place inside them (with precise coordinates). \
We can also create interactable objects with the `bind` command, like so:

```python
# to create a interactable game sprite we can 
# bind left mouse button event to it

sprite = PhotoImage(file='sprite.png')
canvas.create_image(10, 10, image=sprite)

sprite.bind("<Button-1>", lambda e: print("Sprite Clicked"))
```

On the other hand in **Pygame** we can do everything using `Rect` objects: rectangles that expose a lot of useful functions like `collidepoint((x,y))` that returns `True` if a point is inside the rectangle. Again, we can use this to check if a sprite has been clicked:

```python
# gets mouse position
pos = pygame.mouse.get_pos()

# test if a point (ie mouse) is inside the rectangle (ie button)
if sprite.collidepoint(pos):
  print("Sprite Clicked")
```

We can safely say that, at least in the project's scope, Tkinter and Pygame can produce the same UIs with the same level of interactability, which would led us to believe that the former should be chosen since its much easier to handle and requires a third of the lines of code.

The key here is "in the project's scope": the "game" part of this project is little more than a proof of concept, so it can be done with a simple app's UI camouflaged in the guise of an actual game. As soon as we try to think about the project's expandability though, it all falls apart since Tkinter does not implements any of the following (without some nasty workarounds):

- Real sprite animations
- Background music
- VFX sounds
- Real game loop 

Let's briefly explain each one. \
**Real sprite animations:** in a real game we want stuff to move, eg when a city in Raftian gets damaged it should provide a pleasing visual feedback that something is going on.\
**Background music and VFX sounds:** no one would watch a movie without sounds, and the same is true for games: to follow up on the previous example, when a city is attacked we would like to provide a sound feedback to the player.\
**Real game loop:** this is were we actually get into the weeds of the project: if our objective is to evaluate the possibility of using Raft in a game, we *must* have a game loop to answer some very fundamental questions, like:

- Do the Raft routines work when there is a game loop running at 60 cycles per seconds?
- Does framerate (ie game loop frequency / frames per second) have an impact on the Raft's performance (30fps, 60fps, 120fps, 240fps etc)?

These are essential questions since 60fps is the standard framerate in a game, 30fps the minimum acceptable, and other framerates while irrelevant for a static game like Raftian are very relevant in games like first person shooters, where we would like to have as many frames per second as we can get.\
Tkinter cannot provides us with answers, but **Pygame**  can: not only it natively implements all the above mentioned functionalities (animations, VFXs and music), but also has a real game loop that we can limit to a precise amount of frames per seconds with the command `pygame.time.Clock().tick(fps)`.

These reasons, along with the fact that using Pygame would be a valuable learning experience (getting "hands on" on a game engine), make the whole project more interesting from an outsider's perspective and, lastly, be more fun to make, led me to ultimately choose Pygame as the project's UI library.