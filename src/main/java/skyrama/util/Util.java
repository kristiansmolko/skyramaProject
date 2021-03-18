package skyrama.util;

public class Util {

    public int getFlightTime(String time){
        String[] temp = time.split(":");
        int hours = Integer.parseInt(temp[0]) * 3600;
        int mins = Integer.parseInt(temp[1]) * 60;
        return hours + mins;
    }

    public String getFlight(int time){
        int hours = time / 3600;
        int minutes = (time % 3600) / 60;
        return String.format("%02d:%02d", hours, minutes);
    }
}
