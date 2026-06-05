package client;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;

import server.IMagazzino;

public class Proxy implements IMagazzino{
    private String address;
    private int port;

    public Proxy(String address, int port){
        this.address = address;
        this.port = port;
    }

    public void deposita(String articolo, int id){

        String msg = "deposita#" + articolo + "#" + String.valueOf(id);

        try (Socket socket = new Socket(address, port);
            DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));) {
        
                System.out.println(String.format("[PROXY] - Sending: %s", msg));
                output.writeUTF(msg);
                output.flush();
                System.out.println(String.format("[PROXY] - Sent: %s", msg));
                
                String response = input.readUTF();
                System.out.println(String.format("[PROXY] - Received: %s", response));
        
            } catch (IOException e) {
            e.printStackTrace();
        }
        return;
    }

    public int preleva(String articolo){
        String msg = "preleva#" + articolo + "#";
        int id_reponse = -1; 
        try (Socket socket = new Socket(address, port);
            DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));) {
        
                System.out.println(String.format("[PROXY] - Sending: %s", msg));
                output.writeUTF(msg);
                output.flush();
                System.out.println(String.format("[PROXY] - Sent: %s", msg));
                
                id_reponse = input.readInt();
                System.out.println(String.format("[PROXY] - Received: %d", id_reponse));
        
            } catch (IOException e) {
            e.printStackTrace();
        }
        return id_reponse;
    }
}
