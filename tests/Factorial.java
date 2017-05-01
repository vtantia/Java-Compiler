public class Factorial {
    int base;
    int base_factorial;

    public static int factorial(int n){
        int result = 1;
        for(int i = 2; i <= n; i++)
            result *= i;
        return result;
    }

    public Factorial(int num) {
        base = num;
        base_factorial = factorial(num);
    }

    public static void main(String[] args) {
        final int NUM_FACTS = 100;
        Factorial arr[] = new Factorial[] {new Factorial(1), new Factorial(3)};
        int i = 0;
        while (i < NUM_FACTS) {
            System.out.println( i + "! is " + factorial(i));
            i++;
        }
    }
}
