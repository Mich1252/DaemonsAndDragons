<h1>DESCRIPTION</h1>
This is a work in progress program which aims to make being a DM simpler. It provides the user with a console to perform functionsThe end goal for this project is to be able to automate combat encounters with large groups of low-level monsters. 
<h1>KNOWN ISSUES</h1>
You will probably find some syntax to put into the terminal which crashes the program. I am working on making all the inputs as idiot proof as I can. If it's crashing while you're trying to do something, check the comments and make sure you've got the exact right syntax. It's a pain.

The function for loading data from a file only works when main is executed. This means you can only load new data when the program is first run.

<h1>TODO</h2>
The attack function literally hasn't been programmed yet.<br>
Fix the load function.<br>
Implement rolling initiave.<br>
The command to load a new file should probably work.

<h1>DEPENDANCIES</h1>
 =< Python 3.6
<h1>Usage</h1>
<h2>add</h2>

Adds players or enemies to the game!<br>   Parameters-<br>    
* p or e, for player or enemy<br>   
* number of players to add<br>
<h2>status</h2>

Gathers the current hp of a player or enemy<br>     Parameters-<br>  
* p or e, for player or enemy<br>    
* name of player or enemy

<h2>attack</h2>

Deals damage. Hasn't been coded yet.<br>    Parameters-<br>    
* p or e, for player or enemy<br>   
* name of player or enemy<br>    
* damage to deal (can be an int, or a string in the form of ydn+z, where y is the number of dice, n is the type of dice, and z is the modifier)

<h2>help</h2>

Reads this list<br>    Parameters-<br>    
* None

<h2>exit</h2>

Saves and exits!<br>  Parameters-<br>    
* filename to save to (has to end in .json)

<h2>save</h2>

Saves and exits!<br>  Parameters-<br>    
* filename to save to (has to end in .json)

<h2>list</h2>

Lists all the players and enemies in the game<br>    Parameters-<br>
* None

<h2>load</h2>

Loads the data from another .json. Currently broken. Loading only works when the program is first run for now. TODO.<br>    Parameters-<br>    
* filename to load from (must end in .json)
<h2>remove</h2>

Removes players or enemies from the game.<br>Parameters-<br>     
* team, either players or enemies<br>
* names of the players/emeies to remove