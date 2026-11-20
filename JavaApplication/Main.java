
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        int choice;

        do {
            System.out.println("\n================================");
            System.out.println(" AGRICULTURE MANAGEMENT SYSTEM");
            System.out.println("================================");
            System.out.println("1. Farmer Management");
            System.out.println("2. Farm Management");
            System.out.println("3. Crop Management");
            System.out.println("4. Irrigation Management");
            System.out.println("5. Harvest Management");
            System.out.println("6. Exit");

            System.out.print("Enter your choice: ");
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.println("Farmer Management Selected");
                    break;

                case 2:
                    System.out.println("Farm Management Selected");
                    break;

                case 3:
                    System.out.println("Crop Management Selected");
                    break;

                case 4:
                    System.out.println("Irrigation Management Selected");
                    break;

                case 5:
                    System.out.println("Harvest Management Selected");
                    break;

                case 6:
                    System.out.println("Thank you for using the system!");
                    break;

                default:
                    System.out.println("Invalid choice! Try again.");
            }

        } while (choice != 6);

        sc.close();
    }
}
