

public class battery {
    int power;
    int maxPower;
    int minPower;

    public battery() {
        this.maxPower = 100;
        this.minPower = 0;
        this.power = getPower();
    }
    public int getPower() {
        // need to add power consumption with time
        return power;
    }

}
