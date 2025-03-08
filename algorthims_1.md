# NOTE_for_algorithm

## basic knowledge

### Algorithms Definition

So, what is an algorithm? Someone might say it is just an approach to solve a math problem, but now I'm going to define it:

**Definition:** An algorithm is the theoretical study of computer program **performance** and resource usage.  

Actually, we often focus on the performance of an algorithm, although there are many other important factors beyond performance.  

So why do we study algorithms and performance?  

One reason is that with its help, we can make feasible versions of an algorithm out of previously infeasible ones.  
Another reason is that it provides a language to communicate about program behavior, no matter what programming language someone is using.  

Before we dive into the first problem, let's address some preliminary questions.

### Running Time

In the previous section, we discussed that algorithms are the art of performance, but what does that really mean? The answer lies in **running time**.

In computer science, we use time and space as key metrics to assess every program, much like you assess the cost-effectiveness of a product.  

Running time always depends on the input: if the input is the solution, your program will be as fast as possible.  
It also depends on the size of the input; the difference between an input size of 6 and 6*10^9 is substantial.  

In algorithms, we parameterize the input size using `n -> ∞` and often calculate the upper bound because it serves as a guarantee to the user, telling them "the code will not exceed this time.  

### Kinds of analysis  

In total there three situation we should think about  

first the worst case: this is the case we always concentrate on, t(N)= MAX time on any input of size.  
//but you should remanber that T(n) is just a equation of time not a true and correct time  

second case the averange csse: we sometimes think sbout it. T(N)=eccpetion time over all input of size, what we need is a sumption of statisical distribution of input;  

and for the last sicuation is the best case: but unfortunaly we almost never meet this case for it just cheat to user and ouselg.  

### BIG IDEA  

there are some options you should have while you learning algorithms  

first Ignore machine-dependent constants  

second look at the grown of the running time just focus on the trend  

there is a good example of it.  

### Asymptotic notation

Just like we said at before agorithms is not just a tool but a kind of language.  

as a language there must be some notation to describe it:  
**θ- notation** it mean we drop low order terms and igonre leading coustant.  

for instant 3*n^3+90*n^2-*n+6064 = θ(n^3);

as n->inity the low order subject are faster than the high one.

now the pre parts is over let"s going to the Problem one  

## Problem one -sort

### INSERTION SORT

at first we just use an instant to make it explicitation:  

almost everyone have played poker we always put the small in left and the bigs in right;  

for one of the poker **we just compare it with the pokers before it and insert it in the correct location;**  

it's the main idea in insertion sort  

so first let's look at the pseudocode:

INSERTION SORT(A,N)//sort a[1->n]
for j=2->n;  
 do key<-a[j]  
 i=j-1;  
 while i>0 and a[i]>key
  |do a[i+1]<-a[i]  
  |i=i-1  
  |a[i+1]<-key  

finish of all  

by using C++ we can write it as:

``` c++

void insertionsort(int &arr,int n){
    for(int i=1;i<n;i++>){
        int key=arr[i];
        int j=i-1;
        while(j>0&&arr[j]><key){
            arr[j+1]=arr[j];
            j--;
        }
        a[j+1]=key;
    }
}
```  
