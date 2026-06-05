package server;

import java.io.IOException;
import java.net.*;
import java.util.StringTokenizer;

import dispatcher.IDispatcher;

public class SkeletonThread extends Thread{
    private final DatagramSocket socket; // al try-with-resources serve final
    private DatagramPacket packet;
    private IDispatcher dispatcher;

    private final String separator = "#";

    public SkeletonThread(DatagramSocket s, DatagramPacket pkt, IDispatcher disp){
        socket = s;
        packet = pkt;
        dispatcher = disp;
    }

    public void run(){
        System.out.println(String.format("[DISPATCHER THREAD] [%s] - Running", Thread.currentThread().getName()));
        
        // il thread deve leggere il metodo invocato
        // e chiamare il metodo locale corrispondete.
        // try-with-resources: chiude automaticamente input, output e socket
        // (anche in caso di eccezione), e solo le risorse effettivamente aperte
        try {
            String msg = new String(packet.getData(), 0, packet.getLength());

            // parsing del messaggio
            StringTokenizer tokenizer = new StringTokenizer(msg, separator);
            String method = tokenizer.nextToken();
            
            System.out.println(String.format("[DISPATCHER THREAD] [%s] - Received cmd: ##%s##", Thread.currentThread().getName(), method));
            int x;
            
            String risp;
            DatagramPacket response;

            if (method.compareTo("sendCmd") == 0){
                x = Integer.valueOf(tokenizer.nextToken());
                System.out.println(String.format("[DISPATCHER THREAD] [%s] - received cmd: %d", Thread.currentThread().getName(), x));
                dispatcher.sendCmd(x);
                risp = "OK";
                response = new DatagramPacket(risp.getBytes(), risp.getBytes().length, packet.getAddress(), packet.getPort());
                socket.send(response);
            }
            else if (method.compareTo("getCmd") == 0){
                x = dispatcher.getCmd();
                System.out.println(String.format("[DISPATCHER THREAD] [%s] - extracted cmd: %d", Thread.currentThread().getName(), x));
                risp = String.valueOf(x);
                response = new DatagramPacket(risp.getBytes(), risp.getBytes().length, packet.getAddress(), packet.getPort());
                socket.send(response);
            } else {
                System.out.println(String.format("[DISPATCHER THREAD] [%s] - %s is not a valid command!", Thread.currentThread().getName(), method));
                risp = "FAILED";
                response = new DatagramPacket(risp.getBytes(), risp.getBytes().length, packet.getAddress(), packet.getPort());
                socket.send(response);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
