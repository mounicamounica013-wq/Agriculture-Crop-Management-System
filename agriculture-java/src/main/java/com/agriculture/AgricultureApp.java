
package com.agriculture;

import java.util.Scanner;

public class AgricultureApp {

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n==================================");
            System.out.println(" AGRICULTURE MANAGEMENT SYSTEM");
            System.out.println("==================================");
            System.out.println("1. Farmer Management");
            System.out.println("2. Farm Management");
            System.out.println("3. Crop Management");
            System.out.println("4. Cultivation Management");
            System.out.println("5. Irrigation Management");
            System.out.println("6. Harvest Management");
            System.out.println("7. Agricultural Input Management");
            System.out.println("8. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    FarmerManagement.main(args);
                    break;

                case 2:
                    FarmManagement.main(args);
                    break;

                case 3:
                    CropManagement.main(args);
                    break;

                case 4:
                    CultivationManagement.main(args);
                    break;

                case 5:
                    IrrigationManagement.main(args);
                    break;

                case 6:
                    HarvestManagement.main(args);
                    break;

                case 7:
                    InputManagement.main(args);
                    break;

                case 8:
                    System.out.println("Thank you for using Agriculture Management System!");
                    break;

                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 8);

        sc.close();
    }
}
