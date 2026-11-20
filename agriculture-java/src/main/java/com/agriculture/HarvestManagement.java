
package com.agriculture;

import java.sql.*;
import java.util.Scanner;

public class HarvestManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n===== HARVEST MANAGEMENT =====");
            System.out.println("1. Add Harvest");
            System.out.println("2. View All Harvest Records");
            System.out.println("3. Update Harvest");
            System.out.println("4. Delete Harvest");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    addHarvest();
                    break;
                case 2:
                    viewHarvest();
                    break;
                case 3:
                    updateHarvest();
                    break;
                case 4:
                    deleteHarvest();
                    break;
                case 5:
                    System.out.println("Thank you!");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 5);
    }

    static void addHarvest() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Cultivation ID: ");
            int cultivationId = sc.nextInt();

            System.out.print("Enter Harvest Date (YYYY-MM-DD): ");
            String date = sc.next();

            System.out.print("Enter Quantity Harvested: ");
            double quantity = sc.nextDouble();

            System.out.print("Enter Selling Price: ");
            double price = sc.nextDouble();
            sc.nextLine();

            System.out.print("Enter Quality Category: ");
            String quality = sc.nextLine();

            String sql = "INSERT INTO harvest " +
                "(cultivation_id, harvest_date, quantity_harvested, quality_category, selling_price) " +
                "VALUES (?, ?, ?, ?, ?)";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, cultivationId);
                ps.setDate(2, Date.valueOf(date));
                ps.setDouble(3, quantity);
                ps.setString(4, quality);
                ps.setDouble(5, price);

                ps.executeUpdate();

                System.out.println("Harvest record added successfully!");
            }

        } catch (SQLException | IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewHarvest() {

        String sql = "SELECT * FROM harvest";

        try (Connection con = DBConnection.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            System.out.println("\n----- HARVEST DETAILS -----");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("harvest_id") + " | " +
                    rs.getInt("cultivation_id") + " | " +
                    rs.getDate("harvest_date") + " | " +
                    rs.getBigDecimal("quantity_harvested") + " | " +
                    rs.getString("quality_category") + " | " +
                    rs.getBigDecimal("selling_price")
                );
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateHarvest() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Harvest ID to Update: ");
            int id = sc.nextInt();

            System.out.print("Enter Cultivation ID: ");
            int cultivationId = sc.nextInt();

            System.out.print("Enter Harvest Date (YYYY-MM-DD): ");
            String date = sc.next();

            System.out.print("Enter Quantity Harvested: ");
            double quantity = sc.nextDouble();

            System.out.print("Enter Selling Price: ");
            double price = sc.nextDouble();
            sc.nextLine();

            System.out.print("Enter Quality Category: ");
            String quality = sc.nextLine();

            String sql = "UPDATE harvest SET cultivation_id=?, harvest_date=?, " +
                "quantity_harvested=?, quality_category=?, selling_price=? " +
                "WHERE harvest_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, cultivationId);
                ps.setDate(2, Date.valueOf(date));
                ps.setDouble(3, quantity);
                ps.setString(4, quality);
                ps.setDouble(5, price);
                ps.setInt(6, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Harvest record updated successfully!");
                } else {
                    System.out.println("Harvest ID not found!");
                }
            }

        } catch (SQLException | IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteHarvest() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Harvest ID to Delete: ");
            int id = sc.nextInt();

            String sql = "DELETE FROM harvest WHERE harvest_id=?";

            try (PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, id);

                int rows = ps.executeUpdate();

                if (rows > 0) {
                    System.out.println("Harvest record deleted successfully!");
                } else {
                    System.out.println("Harvest ID not found!");
                }
            }

        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
