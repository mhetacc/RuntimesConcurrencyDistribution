*This document is not intended to be the actual final report, it is just a place to keep important informations and intuitions that would otherwise be lost during the development of the project.*

---

# Design
Design philosophy of the infrastructure, from why a technology has been chosen instead of another, to the actual architecture.

## Requirements
Since the focus is showing a fun implementation of the Raft algorithm, a complex overhead is not needed i.e. there is no need to use advanced game engines with multiple languages involved (e.g. Godot, Unity, Cocos, etc.). \
It would be instead preferable to make the whole project with a single language, to simplify the programming process and, since Raft is an algorithm made for *shared consensus*, hence for the web, it would be ideal to use a framework with native networking components. Moreover we want our game to be 2D, for ease of development of course, hence we don't need a powerful 3D game engine. Lastly, we don't really care about portability since we are not making a "real" game. \
To summarize, our core ideal requirements are:
 
1. One language
2. 2D graphics

This is all done to keep things outside "doing Raft" as simple as possible.

Lets talk about language requirements:
1. Native RPC support
2. Native image processing support
 
Theese conditions (for engines and languages) are both complementary and exclusive: if a language (eg Go) has a built-in image processing tool (eg Go's *image* module) a **game engine might not be necessary**.

## Technology  

### Programming Languages
Since this is a Computer Science project, of course it will be done using some (ideally one) programming languages. Which one is not a trivial choice. \
Having done a bit of research, it is clear that there are two extremely dominant languages in the world of computing right now, with no sign of slowing down ie:
1. JavaScript
2. Python
   
While, in the "serious" game development world, we can once again see two (three) languages coming on top:
1. JavaScript (scripting)
2. C++ (core engine)
3. C# (beacouse of Unity)

It can be easly inferred that having a solid base in either of theese three languages (JS, Python, C++) will be greatly beneficial.

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

- ![](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/29e25571-eb24-4381-9a2d-bde0ba52be2e/df3uxma-90078aec-f043-423b-8adf-68b0db323607.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzI5ZTI1NTcxLWViMjQtNDM4MS05YTJkLWJkZTBiYTUyYmUyZVwvZGYzdXhtYS05MDA3OGFlYy1mMDQzLTQyM2ItOGFkZi02OGIwZGIzMjM2MDcucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Pap7EkIxDlgZ1dFLyEK_MOlPIQGjvJVm5T8adKtnAn0)[Pygame](https://www.pygame.org/news)
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
