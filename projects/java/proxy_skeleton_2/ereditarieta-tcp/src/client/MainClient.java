package client;

import server.IMagazzino;

public class MainClient {

    private static final int NUM_THREADS = 5;

    public static void main(String[] args) {
        /*
        usage:
        args[0] address
        args[1] port
        args[2] method
        e.g. java client.MainClient localhost 59013 deposita
        */

        String address = args[0];
        int port = Integer.valueOf(args[1]);
        String method = args[2];

        IMagazzino proxy = new Proxy(address, port);

        Thread threads[] = new Thread[NUM_THREADS];

        for (int i = 0; i < NUM_THREADS; i++) {
            threads[i] = new ClientThread(method, proxy);
            threads[i].start();
        }

        try {
            for (int i = 0; i < NUM_THREADS; i++) {
                threads[i].join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();    
        }
    }
}
