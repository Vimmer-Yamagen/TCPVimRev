# TCPVimRev
It is simple reversi software.  

![GUI](https://github.com/Vimmer-Yamagen/TCPVimRev/blob/pics/TCPVimRev_gui.png)

## Environment

+ Python 3.6.4  

## How to use  

First of all, you must launch the server.  
> python src/vr_server.py  

Second, you must launch AI or Player(2 Clients).  
> python src/vr_ai.py -n NameYouWantToName -m Black(or White)  
> python src/vr_player.py -n NameYouWantToName -m Black(or White)  

--name / -n -> configure a name which you want to name  
--move / -m -> configure Black or White (first move is Black and passive move is White.)  

### How to start/end the game  
Ctrl-s -> start the game.  
Ctrl-c or Ctrl-q -> end the game and shutdown the server.  

## Memo  
+ I implement AI which move randomly. If you rewrite client_core function in vr_ai.py, you are able to make more powerful AI.  

+ Enjoy  