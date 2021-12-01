public class T2 {
    
    public static int max(int[] a, int i)
	{
		if (i == a.length-1)  	//one element list
	    	return a[i];  		// max value is the only value
		int m = max(a,i+1);	 	// recurs over the 2nd element
		if (m > a[i])	 		//and beyond
			return m;
		else
			return a[i];
	}

	public static void main(String[] args) {
		int[] a1 = {2};
		int[] a2 = {2,10,7,4,3,8};
		int[] a3 = {2,0,7,4,17,8};
		int[] a4 = {20,10,7,4,3,8};
		int[] a5 = {2,3,4,9,9,10,20,20,40};

		System.out.println(max(a1,0));
		System.out.println(max(a2,0));
		System.out.println(max(a3,0));
		System.out.println(max(a4,0));

		//System.out.println("fRepeat:");
		//System.out.println(fRepeat(a5,0));
        
    }
	
    public static int fRepeat(int[] a, int i)
	{
		if (a.length < 2)			// list too small to find a pair?
			return 0;				// fail
		if (a[0] == a[1])			// first two elements match?
			return a[0];	    	// return value of first element
		else			    		// otherwise 
			return fRepeat(a,i+1); 	// recur over the second element onward
		
	}


    

}
