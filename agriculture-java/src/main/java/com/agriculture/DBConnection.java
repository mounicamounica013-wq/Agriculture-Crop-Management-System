
package com.agriculture;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {

    public static Connection getConnection() throws SQLException {

        String url = System.getenv("DB_URL");
        String user = System.getenv("DB_USER");
        String password = System.getenv("DB_PASSWORD");

        if (url == null || user == null || password == null) {
            throw new SQLException(
                "Database environment variables are not configured."
            );
        }

        return DriverManager.getConnection(url, user, password);
    }

    public static void main(String[] args) {

        try (Connection connection = getConnection()) {
            System.out.println("MySQL Database Connected Successfully!");
        } catch (SQLException e) {
            System.out.println("Database Connection Failed!");
            System.out.println(e.getMessage());
        }
    }
}
