
package com.agriculture;

import java.sql.*;
import java.util.Scanner;

public class FarmerManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n===== FARMER MANAGEMENT =====");
            System.out.println("1. Add Farmer");
            System.out.println("2. View All Farmers");
            System.out.println("3. Update Farmer");
            System.out.println("4. Delete Farmer");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    addFarmer();
                    break;
                case 2:
                    viewFarmers();
                    break;
                case 3:
                    updateFarmer();
                    break;
                case 4:
                    deleteFarmer();
                    break;
                case 5:
                    System.out.println("Returning to Main Menu...");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 5);
    }

    static void addFarmer() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farmer Name: ");
            String name = sc.nextLine();

            System.out.print("Enter Contact Number: ");
            String contact = sc.nextLine();

            System.out.print("Enter Address: ");
            String address = sc.nextLine();

            String sql = "INSERT INTO farmer(name, contact, address) VALUES (?, ?, ?)";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, name);
                ps.setString(2, contact);
                ps.setString(3, address);
                ps.executeUpdate();

                System.out.println("Farmer added successfully!");
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewFarmers() {

        String sql = "SELECT * FROM farmer";

        try (Connection con = DBConnection.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            System.out.println("\n----- FARMER DETAILS -----");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("farmer_id") + " | " +
                    rs.getString("name") + " | " +
                    rs.getString("contact") + " | " +
                    rs.getString("address")
                );
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateFarmer() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farmer ID to Update: ");
            int id = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter New Name: ");
            String name = sc.nextLine();

            System.out.print("Enter New Contact: ");
            String contact = sc.nextLine();

            System.out.print("Enter New Address: ");
            String address = sc.nextLine();

            String sql = "UPDATE farmer SET name=?, contact=?, address=? WHERE farmer_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, name);
                ps.setString(2, contact);
                ps.setString(3, address);
                ps.setInt(4, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Farmer updated successfully!");
                } else {
                    System.out.println("Farmer ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteFarmer() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farmer ID to Delete: ");
            int id = sc.nextInt();
            sc.nextLine();

            String sql = "DELETE FROM farmer WHERE farmer_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Farmer deleted successfully!");
                } else {
                    System.out.println("Farmer ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
            System.out.println("Farmer may be linked to an existing farm.");
        }
    }
}
