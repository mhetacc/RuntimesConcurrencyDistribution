# Design
Design philosophy of the infrastructure, from why a technology has been chosen instead of another, to the actual architecture.

## Requirements
Since the focus is showing a fun implementation of the Raft algorithm, a complex overhead is not needed i.e. there is no need to use advanced game engines with multiple languages involved (e.g. Godot, Unity, Cocos, etc.). \
It would be instead preferable to make the whole project with a single language, as to simplify the programming process and, since Raft is an algorithm made for *shared consensus*, so for the web, it would be ideal to have our game run in a web browser. \
To summarize, our core requirements are:

1. One language
2. Run in browser
3. 2D graphics

This is all done to keep things outside "doing Raft" as simple as possible.