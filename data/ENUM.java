public class Test {
    
    public static void main(String[] args) {

        int [] x = { 2,5,7,4,3,3};

        System.out.println(maxE(x,x.length));

    }

    static int maxE(int[] a, int i){


        if(a.length == 1)
            return a[0];

        if(i >= a.length-1)
            return a[i];

        int m = max(a,i-1);

        if (m > a[0])
            return m;
        else
            return a[0];
    }
}
