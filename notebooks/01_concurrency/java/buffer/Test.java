package buffer;

import java.io.*;

public class Test {

    public static void main(String[] args) {
        Buffer buf = new Buffer();
        BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
        int choice = 0, id = 1;

        while (true) {
            System.out.println("0 (Consumer) / 1 (Producer) >> ");

            try {
                choice = Integer.parseInt(stdin.readLine());
            } catch (IOException e) {
                e.printStackTrace();
            }

            if (choice == 0) {
                new Consumer(buf, "consumer_" + id).start();
            } else {
                new Producer(buf, "producer_" + id).start();
            }

            id++;
        }
    }
}
