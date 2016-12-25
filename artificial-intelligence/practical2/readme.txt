[Description]
I have chosen a vector with eight elements (called people) to represent the people to find presents for. 
The domain of each element is (4,7,10,12) which represents the possible gifts (4 = box of chocolate, 7 = socks, 10 = cd, 12 = coffee mill).
By using this domain, constraint #1 is guaranteed by design. 
The indices of the vector are defined as follows:
people[0] - mum
people[1] - brother
people[2] - grandma
people[3] - grandpa
people[4] - cousin
people[5] - aunt
people[6] - uncle
people[7] - so
For easier indexing of people within the vector I defined the types of people (brother, so, etc.) as constants. 
For example:
letting   mum=0
letting	  brother=1
letting	  grandma=2
So if I would like to assign a cd to mum it would be people[mum] = 10.  

[Solutions]
There exist only solutions to CSP3, CSP4 and CSP5. 
The other problems are over-constraint.
Please find the solutions below. The first line contains the people vector as it can be found in each solution file.
The following lines respectively contain the interpreted people vector.

[Solution to CSP3]
letting people be [7, 10, 7, 7, 10, 7, 7, 12;int(0..7)]
mum = 7
brother = 10
grandma = 7
grandpa = 7
cousin = 10
aunt = 7
uncle = 7
so = 12

[Solution to CSP4]
letting people be [12, 10, 7, 10, 10, 7, 7, 7;int(0..7)]
mum = 12
brother = 10
grandma = 7
grandpa = 10
cousin = 10
aunt = 7
uncle = 7
so = 7

[Solution to CSP5]
letting people be [7, 10, 4, 7, 4, 4, 10, 12;int(0..7)]
mum = 7
brother = 10
grandma = 4
grandpa = 7
cousin = 4
aunt = 4
uncle = 10
so = 12