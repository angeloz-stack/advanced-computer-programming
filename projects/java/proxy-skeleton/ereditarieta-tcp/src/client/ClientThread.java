package client;

import java.util.Random;

public class ClientThread extends Thread{
    private Proxy proxy;
    private final int NUM_REQS = 3;

    public ClientThread(String address, int port){
        proxy = new Proxy(address, port);
    }

    public void run(){
        Random rand = new Random();

        for (int i = 0; i < NUM_REQS; i++){
            int t = rand.nextInt(2,5);

            try {
                Thread.sleep(t*1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            int cmd = rand.nextInt(0,4);
            System.out.println(String.format("[CLIENT] [%s] sendCmd: %d", Thread.currentThread().getName(), cmd));
            proxy.sendCmd(cmd);
        }
    }
}
