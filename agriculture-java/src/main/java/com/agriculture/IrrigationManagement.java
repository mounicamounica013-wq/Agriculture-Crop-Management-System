
package com.agriculture;

import java.sql.*;
import java.util.Scanner;

public class IrrigationManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n===== IRRIGATION MANAGEMENT =====");
            System.out.println("1. Add Irrigation");
            System.out.println("2. View All Irrigation Records");
            System.out.println("3. Update Irrigation");
            System.out.println("4. Delete Irrigation");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    addIrrigation();
                    break;
                case 2:
                    viewIrrigation();
                    break;
                case 3:
                    updateIrrigation();
                    break;
                case 4:
                    deleteIrrigation();
                    break;
                case 5:
                    System.out.println("Thank you!");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 5);
    }

    static void addIrrigation() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Cultivation ID: ");
            int cultivationId = sc.nextInt();

            System.out.print("Enter Irrigation Date (YYYY-MM-DD): ");
            String date = sc.next();

            System.out.print("Enter Water Quantity: ");
            double water = sc.nextDouble();
            sc.nextLine();

            System.out.print("Enter Irrigation Method: ");
            String method = sc.nextLine();

            String sql = "INSERT INTO irrigation " +
                "(cultivation_id, irrigation_date, water_quantity, irrigation_method) " +
                "VALUES (?, ?, ?, ?)";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, cultivationId);
                ps.setDate(2, Date.valueOf(date));
                ps.setDouble(3, water);
                ps.setString(4, method);

                ps.executeUpdate();
                System.out.println("Irrigation record added successfully!");
            }

        } catch (SQLException | IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewIrrigation() {

        String sql = "SELECT * FROM irrigation";

        try (Connection con = DBConnection.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            System.out.println("\n----- IRRIGATION DETAILS -----");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("irrigation_id") + " | " +
                    rs.getInt("cultivation_id") + " | " +
                    rs.getDate("irrigation_date") + " | " +
                    rs.getBigDecimal("water_quantity") + " | " +
                    rs.getString("irrigation_method")
                );
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateIrrigation() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Irrigation ID to Update: ");
            int id = sc.nextInt();

            System.out.print("Enter Cultivation ID: ");
            int cultivationId = sc.nextInt();

            System.out.print("Enter Irrigation Date (YYYY-MM-DD): ");
            String date = sc.next();

            System.out.print("Enter Water Quantity: ");
            double water = sc.nextDouble();
            sc.nextLine();

            System.out.print("Enter Irrigation Method: ");
            String method = sc.nextLine();

            String sql = "UPDATE irrigation SET cultivation_id=?, " +
                "irrigation_date=?, water_quantity=?, irrigation_method=? " +
                "WHERE irrigation_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, cultivationId);
                ps.setDate(2, Date.valueOf(date));
                ps.setDouble(3, water);
                ps.setString(4, method);
                ps.setInt(5, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Irrigation record updated successfully!");
                } else {
                    System.out.println("Irrigation ID not found!");
                }
            }

        } catch (SQLException | IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteIrrigation() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Irrigation ID to Delete: ");
            int id = sc.nextInt();

            String sql = "DELETE FROM irrigation WHERE irrigation_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Irrigation record deleted successfully!");
                } else {
                    System.out.println("Irrigation ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
