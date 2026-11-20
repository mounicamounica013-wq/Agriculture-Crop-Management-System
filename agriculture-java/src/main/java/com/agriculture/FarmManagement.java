
package com.agriculture;

import java.sql.*;
import java.util.Scanner;
import java.math.BigDecimal;

public class FarmManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n===== FARM MANAGEMENT =====");
            System.out.println("1. Add Farm");
            System.out.println("2. View All Farms");
            System.out.println("3. Update Farm");
            System.out.println("4. Delete Farm");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    addFarm();
                    break;
                case 2:
                    viewFarms();
                    break;
                case 3:
                    updateFarm();
                    break;
                case 4:
                    deleteFarm();
                    break;
                case 5:
                    System.out.println("Returning to Main Menu...");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 5);
    }

    static void addFarm() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farmer ID: ");
            int farmerId = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter Farm Location: ");
            String location = sc.nextLine();

            System.out.print("Enter Total Area: ");
            BigDecimal area = sc.nextBigDecimal();
            sc.nextLine();

            String sql = "INSERT INTO farm(farmer_id, location, total_area) VALUES (?, ?, ?)";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, farmerId);
                ps.setString(2, location);
                ps.setBigDecimal(3, area);
                ps.executeUpdate();

                System.out.println("Farm added successfully!");
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewFarms() {

        String sql = "SELECT * FROM farm";

        try (Connection con = DBConnection.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            System.out.println("\n----- FARM DETAILS -----");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("farm_id") + " | " +
                    rs.getInt("farmer_id") + " | " +
                    rs.getString("location") + " | " +
                    rs.getBigDecimal("total_area")
                );
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateFarm() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farm ID to Update: ");
            int id = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter New Farmer ID: ");
            int farmerId = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter New Location: ");
            String location = sc.nextLine();

            System.out.print("Enter New Total Area: ");
            BigDecimal area = sc.nextBigDecimal();
            sc.nextLine();

            String sql = "UPDATE farm SET farmer_id=?, location=?, total_area=? WHERE farm_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, farmerId);
                ps.setString(2, location);
                ps.setBigDecimal(3, area);
                ps.setInt(4, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Farm updated successfully!");
                } else {
                    System.out.println("Farm ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteFarm() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farm ID to Delete: ");
            int id = sc.nextInt();
            sc.nextLine();

            String sql = "DELETE FROM farm WHERE farm_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Farm deleted successfully!");
                } else {
                    System.out.println("Farm ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
            System.out.println("Farm may be linked to crop or cultivation records.");
        }
    }
}
