public class A1 {
    
    public static int binaryOddonacci(int k)
	{
		int fibVal;
		
		if(k <= 3)
		{
			fibVal = 1;
		}
		else
		{
			fibVal = binaryOddonacci(k-1) + binaryOddonacci(k-2) + binaryOddonacci(k-3);
		}
        	
		return fibVal;
	}

    public static int[] linearOddonacci(int k)
	{
		
		int[] A = new int[2]; 
		int i = 0, j = 0;
		
		if (k == 0)
		{
			i=k;
			j=0;
			
			A[0] = i; A[1] = j;
			System.out.print((i+j) + " ");
			
			return (A);		// this will return (k, 0)
		}
		else if (k == 1)
		{
			i=k;
			j=0;
			
			A[0] = i; A[1] = j;
			System.out.print(j + " " + i + " ");
			
			return (A);		// this will return (k, 0)
		}
		else
		{
			
			A = linearFib(k - 1);
			i = A[0];
			j = A[1];
			System.out.print((i+j) + " ");
			A[0] = i + j;
			A[1] = i;
			return (A);		// this will return (i+j, j)
		}
	}


    public static void main(String[] args) {

        
        for (int i = 1; i <=20; i++) {
            System.out.print(binaryOddonacci(i)+",");
        }


        // for (int i = 0; i <20; i++) {
        //     System.out.print(linearFib(i)+",");
        // }
    }

}
