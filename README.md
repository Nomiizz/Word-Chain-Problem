# Graph Solution using Dijkstra, for the Word Chain problem

The problem says two words (strings) x and y are linked from x to y if  
• you can get y from x by deleting exactly one letter from x (a “deletion”); or  
• you can get y from x by inserting exactly one new letter (an “insertion”); or  
• you can get y from x by interchanging two adjacent letters (this is called a twiddle); or  
• you can get y by reversing the order of the letters in x ( a “reversal”).  

For example  
• **loose** is linked to **lose** because you can delete one of the o’s in loose to get lose;  
• **cat** is linked to **cart** because you can insert the letter r;  
• **alter** is linked to **later** because you can get one from the other by a twiddle at positions 1 and 2;  
• **drawer** is linked to **reward** because you can get one from the other by a reversal.  

A word chain is a sequence of words w1,w2, . . . ,wn, where for each i with 1 < i < n we have that wi is linked to wi+1. We say the chain links w1 with wn. For example

**spam, maps, map, amp, ramp**  

is a word chain because  

• **spam** and **maps** are reversals;  
• **maps** goes to **map** by a deletion;  
• **map** goes to **amp** by a twiddle;  
• **amp** goes to **ramp** by an insertion.  

The cost of a word chain is obtained by summing the cost of each link of the chain where  
  
• a deletion costs 3;  
• an insertion costs 1;  
• a twiddle costs 2;  
• a reversal of a n-letter word costs n.  

If none of these cases apply, you can say that the link has infinite cost.  

The total cost of the chain is therefore 4 + 3 + 2 + 1 = 10.

**This program** reads a dictionary file **'dict.txt'** and then performs two possible operations:  
1) Given a start and end word output the shortest chain path and the cost of the path.  
2) Output the longest shortest path chain in the dictionary file.  

By default operation '1' is performed unless the -l flag is provided.  

For example, an input might be  
**spam ramp**  
**tippy sappy**

For the input above, if dict.txt were  
spam  
maps  
map  
amp  
sap  
sappy  
tip  
tippy  
ramp  

the output would be  
**10 spam maps map amp ramp**  
**-1**  

