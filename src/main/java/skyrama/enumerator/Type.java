package skyrama.enumerator;

public enum Type {
    CARGO (true), PASSENGER (false);

    private boolean value;

    Type(boolean value){
        this.value = value;
    }

    public boolean getValue() {
        return value;
    }
}
