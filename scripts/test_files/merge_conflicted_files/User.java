public class User {
    private String name;
    private int age;

    public User(String name, int age) {
<<<<<<< HEAD
        this.name = name;
        this.age = age;
        System.out.println("User created.");
=======
        this.name = name.toUpperCase();
        this.age = age;
        System.out.println("User created with uppercase name.");
>>>>>>> feature-branch
    }
}
