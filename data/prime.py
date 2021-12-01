import math

def is_prime(x, k):
	if ( k <= 1):
		return True
	elif (x % k == 0):
		return False
	else:
		return is_prime(x, k-1)

def prime(n):
	return is_prime(n, round(math.sqrt(n)))



print(prime(int(input("Enter a Number:"))))