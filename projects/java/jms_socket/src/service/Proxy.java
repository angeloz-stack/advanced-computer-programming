package service;

import java.io.*;
import java.net.Socket;

import loggingServer.ILogging;

public class Proxy implements ILogging{

    private final int port;

    public Proxy(int port){
        this.port = port;
    }

    public void log(String messaggioLog,  int tipo){
        
        try (
            Socket socket = new Socket("localhost", port);
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
        ) {

            System.out.println(String.format("[PROXY] Invoco log con msg: %s tipo: %d", messaggioLog, tipo));
            
            String request = String.format("%s#%d", messaggioLog, tipo);
            
            output.writeUTF(request);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
