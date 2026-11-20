
package com.agriculture;

import java.sql.*;
import java.util.Scanner;

public class CultivationManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n===== CULTIVATION MANAGEMENT =====");
            System.out.println("1. Add Cultivation");
            System.out.println("2. View All Cultivations");
            System.out.println("3. Update Cultivation");
            System.out.println("4. Delete Cultivation");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    addCultivation();
                    break;
                case 2:
                    viewCultivations();
                    break;
                case 3:
                    updateCultivation();
                    break;
                case 4:
                    deleteCultivation();
                    break;
                case 5:
                    System.out.println("Thank you!");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 5);
    }

    static void addCultivation() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Farm ID: ");
            int farmId = sc.nextInt();

            System.out.print("Enter Crop ID: ");
            int cropId = sc.nextInt();

            System.out.print("Enter Cultivation Date (YYYY-MM-DD): ");
            String date = sc.next();

            System.out.print("Enter Cultivated Area: ");
            double area = sc.nextDouble();
            sc.nextLine();

            System.out.print("Enter Season: ");
            String season = sc.nextLine();

            String sql = "INSERT INTO cultivation " +
                "(farm_id, crop_id, cultivation_date, cultivated_area, season) " +
                "VALUES (?, ?, ?, ?, ?)";

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, farmId);
                ps.setInt(2, cropId);
                ps.setDate(3, Date.valueOf(date));
                ps.setDouble(4, area);
                ps.setString(5, season);

                ps.executeUpdate();
                System.out.println("Cultivation added successfully!");
            }

        } catch (SQLException | IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewCultivations() {

        String sql = "SELECT * FROM cultivation";

        try (Connection con = DBConnection.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            System.out.println("\n----- CULTIVATION DETAILS -----");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("cultivation_id") + " | " +
                    rs.getInt("farm_id") + " | " +
                    rs.getInt("crop_id") + " | " +
                    rs.getDate("cultivation_date") + " | " +
                    rs.getBigDecimal("cultivated_area") + " | " +
                    rs.getString("season")
                );
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateCultivation() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Cultivation ID to Update: ");
            int id = sc.nextInt();

            System.out.print("Enter Farm ID: ");
            int farmId = sc.nextInt();

            System.out.print("Enter Crop ID: ");
            int cropId = sc.nextInt();

            System.out.print("Enter Cultivation Date (YYYY-MM-DD): ");
            String date = sc.next();

            System.out.print("Enter Cultivated Area: ");
            double area = sc.nextDouble();
            sc.nextLine();

            System.out.print("Enter Season: ");
            String season = sc.nextLine();

            String sql = "UPDATE cultivation SET farm_id=?, crop_id=?, " +
                "cultivation_date=?, cultivated_area=?, season=? " +
                "WHERE cultivation_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, farmId);
                ps.setInt(2, cropId);
                ps.setDate(3, Date.valueOf(date));
                ps.setDouble(4, area);
                ps.setString(5, season);
                ps.setInt(6, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Cultivation updated successfully!");
                } else {
                    System.out.println("Cultivation ID not found!");
                }
            }

        } catch (SQLException | IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteCultivation() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Cultivation ID to Delete: ");
            int id = sc.nextInt();

            String sql = "DELETE FROM cultivation WHERE cultivation_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Cultivation deleted successfully!");
                } else {
                    System.out.println("Cultivation ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Cannot delete this cultivation. " +
                "It may be linked to irrigation or harvest records.");
        }
    }
}
