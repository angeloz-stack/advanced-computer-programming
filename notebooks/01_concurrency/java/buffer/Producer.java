package buffer;

public class Producer extends Thread {

    private Buffer buffer;

    public Producer(Buffer b, String name) {
        super(name);
        buffer = b;
    }

    @Override
    public void run() {
        buffer.produci();
    }
}
