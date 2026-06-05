package server;

import java.io.IOException;
import java.net.*;

import dispatcher.IDispatcher;

public class DispatcherSkeleton implements IDispatcher{
    // costruttore
    private IDispatcher dispatcher;

    public DispatcherSkeleton(IDispatcher dispatcher){
        this.dispatcher = dispatcher;
    }

    public void sendCmd(int cmd){
        dispatcher.sendCmd(cmd);
    }

    public int getCmd(){
        return dispatcher.getCmd();
    }

    public void runSkeleton(){

        try (DatagramSocket socket = new DatagramSocket()) {
            System.out.println("[DISPATCHER] - In ascolto sulla porta: " + socket.getLocalPort());

            while (true){
                // qui passo allo skeleton thread conn e una ref all'istanza
                // per chiamare i metodi preleva e inserisci (this)

                byte data[] = new byte[100];
                DatagramPacket response = new DatagramPacket(data, data.length);
                socket.receive(response);

                Thread thread = new SkeletonThread(socket, response, this);
                thread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return;
    }
}
