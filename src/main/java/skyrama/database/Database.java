package skyrama.database;

import com.google.gson.Gson;
import skyrama.entity.Plane;
import skyrama.enumerator.Type;
import skyrama.util.Util;

import java.io.IOException;
import java.io.InputStream;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Properties;

public class Database {
    Util util = new Util();
    private final String insertPlane = "INSERT INTO planes(name, type, cargo, cost, flight, delivery, exp, mastery) " +
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?)";
    private final String getAllPlanes = "SELECT * FROM planes";
    private final String findPlane = "SELECT * FROM planes WHERE name like ?";
    private final String getPlanesByType = "SELECT * FROM planes WHERE type like ?";
    private final String getPlanesByCargo = "SELECT * FROM planes WHERE cargo = ?";
    private final String updateEventCurrency = "UPDATE event SET currency = ?";
    private final String getEventCurrency = "SELECT * FROM event";
    private final String deletePlane = "DELETE FROM planes WHERE name like ?";

    public Connection getConnection() throws IOException, SQLException {
        Properties prop = new Properties();
        InputStream loader = getClass().getClassLoader().getResourceAsStream("dat.properties");
        prop.load(loader);
        String url = prop.getProperty("url");
        String name = prop.getProperty("name");
        String pass = prop.getProperty("password");
        Connection connection = DriverManager.getConnection(url, name, pass);
        return connection;
    }

    public boolean insertPlane(Plane plane){
        try (Connection connection = getConnection()) {
            if (connection != null) {
                PreparedStatement ps = connection.prepareStatement(insertPlane);
                if (util.getFlightTime(plane.getFlight()) == 0)
                    return false;
                ps.setString(1, plane.getName());
                ps.setString(2, plane.getType().toLowerCase());
                ps.setBoolean(3, plane.isCargo());
                ps.setInt(4, plane.getCost());
                ps.setInt(5, util.getFlightTime(plane.getFlight()));
                ps.setInt(6, plane.getDelivery());
                ps.setInt(7, plane.getExp());
                ps.setBoolean(8, plane.isMastery());
                return ps.executeUpdate() == 1;
            }
        } catch (Exception e) { e.printStackTrace(); }
        return false;
    }

    private List<Plane> executeSelect(PreparedStatement ps) throws SQLException {
        ResultSet rs = ps.executeQuery();
        List<Plane> list = new ArrayList<>();
        while (rs.next()){
            String name = rs.getString("name");
            String type = rs.getString("type");
            boolean cargo = rs.getBoolean("cargo");
            int cost = rs.getInt("cost");
            String flight = util.getFlight(rs.getInt("flight"));
            int delivery = rs.getInt("delivery");
            int exp = rs.getInt("exp");
            boolean mastery = rs.getBoolean("mastery");
            list.add(new Plane(name, type, cargo, flight, cost, delivery, exp, mastery));
        }
        return list;
    }

    public List<Plane> getAllPlanes(){
        try (Connection connection = getConnection()) {
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(getAllPlanes);
                return executeSelect(ps);
            }
        } catch (Exception e) { e.printStackTrace(); }
        return null;
    }

    public List<Plane> getPlanesByType(String type){
        try (Connection connection = getConnection()) {
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(getPlanesByType);
                ps.setString(1, type.toLowerCase());
                return executeSelect(ps);
            }
        } catch ( Exception e) { e.printStackTrace(); }
        return null;
    }


    public List<Plane> getPlanesByCargo(String cargo) {
        try (Connection connection = getConnection()){
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(getPlanesByCargo);
                ps.setInt(1, cargo.equalsIgnoreCase("cargo")?1:0);
                return executeSelect(ps);
            }
        } catch (Exception e) { e.printStackTrace(); }
        return null;
    }

    public boolean updateCurrency(int value) {
        try (Connection connection = getConnection()) {
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(updateEventCurrency);
                ps.setInt(1, value);
                return ps.executeUpdate() == 1;
            }
        } catch (Exception e) { e.printStackTrace(); }
        return false;
    }

    public int getCurrency(){
        int currency = 0;
        try (Connection connection = getConnection()){
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(getEventCurrency);
                ResultSet rs = ps.executeQuery();
                if (rs.next()) {
                    currency = rs.getInt("currency");
                    return currency;
                }
            }
        } catch (Exception e) { e.printStackTrace(); }
        return currency;
    }

    public boolean exist(String name){
        try (Connection connection = getConnection()){
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(findPlane);
                ps.setString(1, name);
                ResultSet rs = ps.executeQuery();
                return rs.next();
            }
        } catch (Exception e) { e.printStackTrace(); }
        return false;
    }

    public boolean deletePlane(String name){
        try (Connection connection = getConnection()){
            if (connection != null){
                PreparedStatement ps = connection.prepareStatement(deletePlane);
                ps.setString(1, name);
                return ps.executeUpdate() == 1;
            }
        } catch (Exception e) { e.printStackTrace(); }
        return false;
    }
}
