


int expon(int base, int expon, int mod)
{
	int length = 0;
	for (length = 31; length >=0; length--)
	{
		if (expon & (1 << length))
		{break;}
	}
	
	long long z = 1;
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
	{ return false; }
	
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

int num_strong(int n)
{
	int strong_witnesses = 0;
	for (int a=2; a < n-1; a++)
	{
		if (miller_rabin(n, a) == false)
		{
			strong_witnesses++;
		}
	}
	return strong_witnesses;
}

void get_percent(int n)
{
   
    int witnesses = n-3;
    	
	int strong = num_strong(n);
	int weak = num_weak(n);

}

//MAIN PROGRAM
int main(int argc, char *argv[])
{
    int n = 100;
    get_percent(n);
    //atoi(argv[1]));
	return 0;
}

