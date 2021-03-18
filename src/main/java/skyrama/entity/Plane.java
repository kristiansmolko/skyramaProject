package skyrama.entity;

public class Plane {
    String name;
    int delivery;
    int exp;
    int cost;
    String flight;
    boolean mastery;
    boolean cargo;
    String type;

    public Plane(String name, String type, boolean cargo, String flight, int delivery, int exp, int cost, boolean mastery) {
        this.name = name;
        this.delivery = delivery;
        this.exp = exp;
        this.cost = cost;
        this.flight = flight;
        this.mastery = mastery;
        this.cargo = cargo;
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public int getDelivery() {
        return delivery;
    }

    public int getExp() {
        return exp;
    }

    public int getCost() {
        return cost;
    }

    public String getFlight() {
        return flight;
    }

    public boolean isMastery() {
        return mastery;
    }

    public boolean isCargo() {
        return cargo;
    }

    public String getType() {
        return type;
    }
}
