package buffer;

public class Consumer extends Thread {

    private Buffer buffer;

    public Consumer(Buffer b, String name) {
        super(name);
        buffer = b;
    }

    @Override
    public void run() {
        buffer.consuma();
    }
}
