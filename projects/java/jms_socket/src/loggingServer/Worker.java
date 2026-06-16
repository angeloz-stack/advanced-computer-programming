package loggingServer;

import java.io.*;
import java.net.Socket;
import java.util.StringTokenizer;

public class Worker extends Thread{
    private final Socket socket;
    private final ILogging server;
    private final String separator = "#";
    
    public Worker(Socket conn, ILogging ref){
        socket = conn;
        server = ref;
    }

    public void run(){
        try (
            socket;
            DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
        ) {
            
            String request = input.readUTF();
            StringTokenizer tokenizer = new StringTokenizer(request, separator);
            String messaggioLog = tokenizer.nextToken();
            int tipo = Integer.valueOf(tokenizer.nextToken());

            System.out.println(String.format("[WORKER] - (%s) - Invoco log con msg: %s tipo: %d",
                                Thread.currentThread().getName(), messaggioLog, tipo));

            server.log(messaggioLog, tipo);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
