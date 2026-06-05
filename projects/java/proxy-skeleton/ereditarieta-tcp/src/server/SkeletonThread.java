package server;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.*;

import dispatcher.IDispatcher;

public class SkeletonThread extends Thread{
    private final Socket conn; // al try-with-resources serve final
    private IDispatcher dispatcher;

    public SkeletonThread(Socket s, IDispatcher disp){
        conn = s;
        dispatcher = disp;
    }

    public void run(){
        System.out.println(String.format("[DISPATCHER THREAD] [%s] - Running", Thread.currentThread().getName()));
        
        // il thread deve leggere il metodo invocato
        // e chiamare il metodo locale corrispondete.
        // try-with-resources: chiude automaticamente input, output e conn
        // (anche in caso di eccezione), e solo le risorse effettivamente aperte
        try (
            conn;
            DataInputStream input = new DataInputStream(new BufferedInputStream(conn.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(conn.getOutputStream()))
        ) {
            String method = input.readUTF();
            System.out.println(String.format("[DISPATCHER THREAD] [%s] - Received method: ##%s##", Thread.currentThread().getName(), method));
            int x;

            if (method.compareTo("sendCmd") == 0){
                x = input.readInt();
                System.out.println(String.format("[DISPATCHER THREAD] [%s] - received cmd: %d", Thread.currentThread().getName(), x));
                dispatcher.sendCmd(x);
                output.writeUTF("OK");
            }
            else if (method.compareTo("getCmd") == 0){
                x = dispatcher.getCmd();
                System.out.println(String.format("[DISPATCHER THREAD] [%s] - extracted cmd: %d", Thread.currentThread().getName(), x));
                output.writeInt(x);
            } else {
                System.out.println(String.format("[DISPATCHER THREAD] [%s] - %s is not a valid command!", Thread.currentThread().getName(), method));
                output.writeUTF("FAILED");
            }
            output.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
