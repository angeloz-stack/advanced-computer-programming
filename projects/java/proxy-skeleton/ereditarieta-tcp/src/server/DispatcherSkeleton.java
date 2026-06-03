package server;

import java.io.IOException;
import java.net.*;

import dispatcher.IDispatcher;

public abstract class DispatcherSkeleton implements IDispatcher{
    // costruttore
    private int backlog;

    public DispatcherSkeleton(int backlog){
        this.backlog = backlog;
    }

    public void runSkeleton(){

        try (ServerSocket socket = new ServerSocket(0, backlog);) {
            System.out.println("[DISPATCHER] - In ascolto sulla porta: " + socket.getLocalPort());

            while (true){
                Socket conn = socket.accept();
                // qui passo allo skeleton thread conn e una ref all'istanza
                // per chiamare i metodi preleva e inserisci (this)
                Thread thread = new SkeletonThread(conn, this);
                thread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


        return;
    }
}
