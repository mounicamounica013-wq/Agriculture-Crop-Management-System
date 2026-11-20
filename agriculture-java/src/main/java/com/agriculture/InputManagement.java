
package com.agriculture;

import java.sql.*;
import java.util.Scanner;

public class InputManagement {

    static Scanner sc = AgricultureApp.sc;

    public static void main(String[] args) {

        int choice;

        do {
            System.out.println("\n===== AGRICULTURAL INPUT MANAGEMENT =====");
            System.out.println("1. Add Input");
            System.out.println("2. View All Input Records");
            System.out.println("3. Update Input");
            System.out.println("4. Delete Input");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    addInput();
                    break;

                case 2:
                    viewInputs();
                    break;

                case 3:
                    updateInput();
                    break;

                case 4:
                    deleteInput();
                    break;

                case 5:
                    System.out.println("Exiting Input Management...");
                    break;

                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 5);
    }

    // ADD INPUT
    public static void addInput() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Cultivation ID: ");
            int cultivationId = sc.nextInt();

            sc.nextLine();

            System.out.print("Enter Fertilizer Type: ");
            String fertilizerType = sc.nextLine();

            System.out.print("Enter Quantity Used: ");
            double quantity = sc.nextDouble();

            System.out.print("Enter Input Cost: ");
            double cost = sc.nextDouble();

            sc.nextLine();

            System.out.print("Enter Application Date (YYYY-MM-DD): ");
            String date = sc.nextLine();

            String sql = "INSERT INTO input " +
                    "(cultivation_id, fertilizer_type, quantity_used, input_cost, application_date) " +
                    "VALUES (?, ?, ?, ?, ?)";

            PreparedStatement ps = con.prepareStatement(sql);

            ps.setInt(1, cultivationId);
            ps.setString(2, fertilizerType);
            ps.setDouble(3, quantity);
            ps.setDouble(4, cost);
            ps.setDate(5, Date.valueOf(date));

            ps.executeUpdate();

            System.out.println("Input Added Successfully!");

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    // VIEW INPUTS
    public static void viewInputs() {

        try (Connection con = DBConnection.getConnection()) {

            String sql = "SELECT * FROM input";

            Statement st = con.createStatement();
            ResultSet rs = st.executeQuery(sql);

            System.out.println("\n----- AGRICULTURAL INPUT DETAILS -----");

            while (rs.next()) {

                System.out.println(
                        rs.getInt("input_id") + " | " +
                        rs.getInt("cultivation_id") + " | " +
                        rs.getString("fertilizer_type") + " | " +
                        rs.getDouble("quantity_used") + " | " +
                        rs.getDouble("input_cost") + " | " +
                        rs.getDate("application_date")
                );
            }

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    // UPDATE INPUT
    public static void updateInput() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Input ID to Update: ");
            int inputId = sc.nextInt();

            System.out.print("Enter Cultivation ID: ");
            int cultivationId = sc.nextInt();

            sc.nextLine();

            System.out.print("Enter Fertilizer Type: ");
            String fertilizerType = sc.nextLine();

            System.out.print("Enter Quantity Used: ");
            double quantity = sc.nextDouble();

            System.out.print("Enter Input Cost: ");
            double cost = sc.nextDouble();

            sc.nextLine();

            System.out.print("Enter Application Date (YYYY-MM-DD): ");
            String date = sc.nextLine();

            String sql = "UPDATE input SET cultivation_id=?, fertilizer_type=?, " +
                    "quantity_used=?, input_cost=?, application_date=? WHERE input_id=?";

            PreparedStatement ps = con.prepareStatement(sql);

            ps.setInt(1, cultivationId);
            ps.setString(2, fertilizerType);
            ps.setDouble(3, quantity);
            ps.setDouble(4, cost);
            ps.setDate(5, Date.valueOf(date));
            ps.setInt(6, inputId);

            int rows = ps.executeUpdate();

            if (rows > 0) {
                System.out.println("Input Updated Successfully!");
            } else {
                System.out.println("Input ID Not Found!");
            }

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    // DELETE INPUT
    public static void deleteInput() {

        try (Connection con = DBConnection.getConnection()) {

            System.out.print("Enter Input ID to Delete: ");
            int inputId = sc.nextInt();

            String sql = "DELETE FROM input WHERE input_id=?";

            PreparedStatement ps = con.prepareStatement(sql);
            ps.setInt(1, inputId);

            int rows = ps.executeUpdate();

            if (rows > 0) {
                System.out.println("Input Deleted Successfully!");
            } else {
                System.out.println("Input ID Not Found!");
            }

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
