
package com.agriculture;

import java.sql.*;
import java.util.Scanner;

public class CropManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {
        int choice;

        do {
            System.out.println("\n===== CROP MANAGEMENT =====");
            System.out.println("1. Add Crop");
            System.out.println("2. View All Crops");
            System.out.println("3. Update Crop");
            System.out.println("4. Delete Crop");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1: addCrop(); break;
                case 2: viewCrops(); break;
                case 3: updateCrop(); break;
                case 4: deleteCrop(); break;
                case 5: System.out.println("Returning to Main Menu..."); break;
                default: System.out.println("Invalid choice!");
            }
        } while (choice != 5);
    }

    static void addCrop() {
        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farm ID: ");
            int farmId = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter Crop Name: ");
            String cropName = sc.nextLine();

            System.out.print("Enter Season: ");
            String season = sc.nextLine();

            System.out.print("Enter Crop Category: ");
            String category = sc.nextLine();

            System.out.print("Enter Expected Cultivation Duration (Days): ");
            int duration = sc.nextInt();
            sc.nextLine();

            String sql = "INSERT INTO crop " +
                "(farm_id, crop_name, season, crop_category, expected_duration_days) " +
                "VALUES (?, ?, ?, ?, ?)";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, farmId);
                ps.setString(2, cropName);
                ps.setString(3, season);
                ps.setString(4, category);
                ps.setInt(5, duration);

                ps.executeUpdate();
                System.out.println("Crop added successfully!");
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewCrops() {
        String sql = "SELECT * FROM crop";

        try (Connection con = DBConnection.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            System.out.println("\n----- CROP DETAILS -----");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("crop_id") + " | " +
                    rs.getInt("farm_id") + " | " +
                    rs.getString("crop_name") + " | " +
                    rs.getString("season") + " | " +
                    rs.getString("crop_category") + " | " +
                    rs.getInt("expected_duration_days") + " days"
                );
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateCrop() {
        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Crop ID to Update: ");
            int id = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter New Farm ID: ");
            int farmId = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter New Crop Name: ");
            String cropName = sc.nextLine();

            System.out.print("Enter New Season: ");
            String season = sc.nextLine();

            System.out.print("Enter New Crop Category: ");
            String category = sc.nextLine();

            System.out.print("Enter New Expected Cultivation Duration (Days): ");
            int duration = sc.nextInt();
            sc.nextLine();

            String sql = "UPDATE crop SET farm_id=?, crop_name=?, season=?, " +
                "crop_category=?, expected_duration_days=? WHERE crop_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, farmId);
                ps.setString(2, cropName);
                ps.setString(3, season);
                ps.setString(4, category);
                ps.setInt(5, duration);
                ps.setInt(6, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Crop updated successfully!");
                } else {
                    System.out.println("Crop ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteCrop() {
        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Crop ID to Delete: ");
            int id = sc.nextInt();
            sc.nextLine();

            String sql = "DELETE FROM crop WHERE crop_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Crop deleted successfully!");
                } else {
                    System.out.println("Crop ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
            System.out.println("Crop may be linked to cultivation records.");
        }
    }
}
