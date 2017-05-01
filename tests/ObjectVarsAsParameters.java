public class Rectangle {
    public int x, X, y, Y;
    public Rectangle(int x, int y, int X, int Y) {
        this.x = x;
        this.y = y;
        this.X = X;
        this.Y = Y;
    }
    public setSize(int delX, int delY) {
        X = x + delX;
        Y = y + delY;
    }
}

public class ObjectVarsAsParameters {
    public static void alterPointee(Rectangle r) {
        System.out.println("In method alterPointee. r " + r + "\n");
        r.setSize(20, 30);
        System.out.println("In method alterPointee. r " + r + "\n");
    }

    public static void alterPointer(Rectangle r) {
        System.out.println("In method alterPointer. r " + r + "\n");
        r = new Rectangle(5, 10, 30, 35);
        System.out.println("In method alterPointer. r " + r + "\n");
    }

    public static void go() {
        Rectangle r1 = new Rectangle(0,0,5,5);
        System.out.println("In method go. r1 " + r1 + "\n");
        // could have been
        //System.out.prinltn("r1" + r1.toString());
        r1.setSize(10, 15);
        System.out.println("In method go. r1 " + r1 + "\n");
        alterPointee(r1);
        System.out.println("In method go. r1 " + r1 + "\n");

        alterPointer(r1);
        System.out.println("In method go. r1 " + r1 + "\n");
    }

    public static void main(String[] args) {
        go();
    }
}
