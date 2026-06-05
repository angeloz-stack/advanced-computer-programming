package client;

import java.io.*;
import java.net.*;

import dispatcher.IDispatcher;

public class Proxy implements IDispatcher{
    private String address;
    private int port;
    private DatagramSocket sock;

    public Proxy(String a, int p){
        address = a;
        port = p;

        try {
            sock = new DatagramSocket();
        } catch (SocketException e) {
            e.printStackTrace();
        }
    }

    public void sendCmd(int i){
        byte data[] = ("sendCmd#" + i + "#").getBytes();
        
        try{
            System.out.println(String.format("[PROXY] - Sending cmd: %d", i));
            
            InetAddress addr = InetAddress.getByName(address);
            DatagramPacket pkt = new DatagramPacket(data, data.length, addr, port);
            
            sock.send(pkt);
            System.out.println(String.format("[PROXY] - Sent cmd: %d", i));
            byte r[] = new byte[100];
            DatagramPacket response = new DatagramPacket(r, r.length);
            sock.receive(response);
            
            String msg = new String(response.getData(), 0, response.getLength());
            
            System.out.println(String.format("[PROXY] - Response: %s", msg));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public int getCmd(){
        int cmd = -1;
        byte data[] = ("getCmd#").getBytes();
        
        try{
            System.out.println("[PROXY] - Getting cmd...");
            
            DatagramPacket pkt = new DatagramPacket(data, data.length, InetAddress.getByName(address), port);
            sock.send(pkt);
            
            byte r[] = new byte[100];
            DatagramPacket response = new DatagramPacket(r, r.length);
            sock.receive(response);

            String msg = new String(response.getData(), 0, response.getLength());
            cmd = Integer.valueOf(msg);
            System.out.println(String.format("[PROXY] - Response: %d", cmd));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return cmd;
    }
}
