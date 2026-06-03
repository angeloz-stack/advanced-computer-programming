package client;

import java.io.*;
import java.net.*;

import dispatcher.IDispatcher;

public class Proxy implements IDispatcher{
    private String address;
    private int port;

    public Proxy(String a, int p){
        address = a;
        port = p;
    }

    public void sendCmd(int i){
        try (
            Socket sock = new Socket(address, port);
            DataInputStream input = new DataInputStream(new BufferedInputStream(sock.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(sock.getOutputStream()));
        ) {
            System.out.println(String.format("[PROXY] - Sending cmd: %d", i));
            
            output.writeUTF("sendCmd");
            System.out.println("[PROXY] - Sent: sendCmd");
            output.writeInt(i);
            System.out.println(String.format("[PROXY] - Sent: %d", i));
            output.flush();

            String response = input.readUTF();
            System.out.println(String.format("[PROXY] - Response: %s", response));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public int getCmd(){
        int cmd = -1;
        try (
            Socket sock = new Socket(address, port);
            DataInputStream input = new DataInputStream(new BufferedInputStream(sock.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(sock.getOutputStream()));
        ) {
            System.out.println("[PROXY] - Getting cmd...");
            
            output.writeUTF("getCmd");
            output.flush();

            cmd = input.readInt();
            System.out.println(String.format("[PROXY] - Response: %d", cmd));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return cmd;
    }
}
