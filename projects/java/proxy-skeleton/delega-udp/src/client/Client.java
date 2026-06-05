package client;

public class Client {

    private static final int NUM_THREADS = 5;

    public static void main(String[] args) {
        // args[0] è address
        // agrs[1] è port

        String address = args[0];
        int port = Integer.valueOf(args[1]);

        ClientThread threads[] = new ClientThread[NUM_THREADS];

        for (int i = 0; i < NUM_THREADS; i++){
            threads[i] = new ClientThread(address, port);
            threads[i].start();
        }

        for (int i = 0; i < NUM_THREADS; i++){
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
