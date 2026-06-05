package client;

import java.util.Random;

import server.IMagazzino;

public class ClientThread extends Thread{
    private final String method;
    private final IMagazzino proxy;
    private final int NUM_REQS = 3;
    private final String[] articoli = {"smartphone", "laptop"};
    private static final Random random = new Random();

    public ClientThread(String m, IMagazzino p){
        method = m;
        proxy = p;
    }

    public void run(){
        
        int id = -1;
        boolean isDeposita = method.equals("deposita");
        try {
            for (int i = 0; i < NUM_REQS; i++) {
                Thread.sleep(random.nextInt(2, 4)*1000);
                String articolo = articoli[random.nextInt(2)];
                if (isDeposita){
                    id = random.nextInt(101);
                    proxy.deposita(articolo, id);
                    System.out.println(String.format("[CLIENT] - [%s] Depositato %s id: %d", Thread.currentThread().getName(), articolo, id));
                } else {
                    id = proxy.preleva(articolo);
                    System.out.println(String.format("[CLIENT] - [%s] Prelevato %s id: %d", Thread.currentThread().getName(), articolo, id));
                }
            }
        } catch (InterruptedException e){
            e.printStackTrace();
        }
    }
}
