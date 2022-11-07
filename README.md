# PIZZABOT
#### Short description
The program receives coordinates of drop points (delivery destination points) and calculates the route 
as a concatenated string of N's (North), S's (South), E's (East), W's (West), and 'D's (for Drop Point).

#### Example
You call the executable passing the plot description as an argument in the
following way:
```
./pizzabot "5x5(0,0)(1,3)(4,4)(4,2)(4,2)(0,1)(3,2)(2,3)(4,1)"
```
Note the format of plot description: first comes the descriplion of plot size
(kind of pizza delivery area) immediately followed by coordinates of drop points.

Example of output...
```
DNDENNDEDEDEDNDDNND
```
...which is Drop -> North -> Drop -> East -> ... -> Drop (see the description above).

#### Requirements
`Python3`, which is highly likely pre-installed on your machine.

#### Downloading and launching
In the terminal window mkdir and cd into it.
To download and unpack the tarball, issue:
```
wget -c https://github.com/paul-michelle/pizzabot/raw/master/pizzabot.tar.gz -O - | tar -xz
```
Copy and paste the command from the example section above, to test the program.
Pass your own plot description, to get the route.

#### Important
Currently, only single digit positive values of coordinates supported, i.e.
points from (0, 0) to (9, 9).