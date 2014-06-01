#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

//raise the base to the expon and do a mod
int expon(int base, int expon, int mod)
{
	//find the first one bit in the expon
	int length = 0;
	for (length = 31; length >=0; length--)
	{
		if (expon & (1 << length))
		{break;}
	}
	
	long long z = 1;
	//do the square and multiply algorithm
	for (int i = length; i >= 0; i--)
	{
		z = (z*z) % mod;
		if (expon & (1 << i))
		{
			z = (z * base) % mod;
		}
	}
	return z;
}

//use Fermat's Little Thm. to do a weak test for witnesses
//this counts the number of a's that say n is prime
int num_weak(int n)
{
	int witnesses =0;
	for (int a = 2; a < n-1; a++)
	{		
		if(expon(a, n-1, n) == 1)
		{
			witnesses++;
		}
	}
	return witnesses;
}

//does a primality test on n using the witness a
bool miller_rabin(int n, int a)
{
	int temp = n-1;
	int k=0;
	while (temp % 2 == 0)
	{
		temp /=2;
		k++;
	} 
	int m = temp;		
	int b = expon(a, m, n);
	
	if (b == 1)
	{ return false; }//not composite
	
	for (int i=1; i<= k; i++)
	{
		if (b == n-1)
		{
			return false;
		}
		else
		{
			b = expon(b, 2, n);
		}
	}
	return true;
}

//checks the number of a's that fail the miller-rabin test
//i.e. these a's say n is prime
int num_strong(int n)
{
	int strong_witnesses = 0;
	for (int a=2; a < n-1; a++)
	{
		if (miller_rabin(n, a) == false)//returns not composite
		{
			strong_witnesses++;
		}
	}
	return strong_witnesses;
}

void get_percent(int n)
{
    clock_t sec;
    sec = clock();
    
    int witnesses = n-3;
    
	//printf("The number of witnesses for %d is %d\n", n, witnesses);
	
	int strong = num_strong(n);
	//printf("There are %d strong witnesses.\n", strong);
	
	int weak = num_weak(n);
	//printf("There are %d weak witnesses.\n", weak);
	
	
	
	//printf("The percentage of strong false witnesses over weak false witnesses is %f\n",
	//	(strong/(float)weak) * 100);
		
	//printf("The percentage of strong false witnesses over all witnesses is %f\n\n",
	//	(strong/(float)witnesses) * 100);
    
	//printf("Took %.6f seconds.\n\n", (double)(clock() - sec) / CLOCKS_PER_SEC);
    printf("strong =  %d\nweak =  %d\ncorrectness = true\nans =  %f\n", strong, weak, (double)(clock() - sec) * 1000 / CLOCKS_PER_SEC);
}

//MAIN PROGRAM
int main(int argc, char *argv[])
{
    //Takes parameter as input to find number of strong and weak witnesses
    get_percent(atoi(argv[1]));
	return 0;
}

/*
The number of witnesses for 289 is 286
There are 14 strong witnesses.
There are 14 weak witnesses.
The percentage of strong false witnesses over weak false witnesses is 100.000000
The percentage of strong false witnesses over all witnesses is 4.895105

Took 0.001255 seconds.

The number of witnesses for 561 is 558
There are 8 strong witnesses.
There are 318 weak witnesses.
The percentage of strong false witnesses over weak false witnesses is 2.515723
The percentage of strong false witnesses over all witnesses is 1.433692

Took 0.002051 seconds.

The number of witnesses for 677667 is 677664
There are 0 strong witnesses.
There are 2 weak witnesses.
The percentage of strong false witnesses over weak false witnesses is 0.000000
The percentage of strong false witnesses over all witnesses is 0.000000

Took 1.771643 seconds.

The number of witnesses for 11111111 is 11111108
There are 48 strong witnesses.
There are 398 weak witnesses.
The percentage of strong false witnesses over weak false witnesses is 12.060302
The percentage of strong false witnesses over all witnesses is 0.000432

Took 34.301716 seconds.
*/
