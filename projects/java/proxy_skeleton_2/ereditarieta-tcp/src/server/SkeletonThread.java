package server;

import java.io.*;
import java.net.Socket;
import java.util.StringTokenizer;

public class SkeletonThread extends Thread{
    private final Socket socket;
    private final IMagazzino skeleton;
    private final String separator = "#";

    public SkeletonThread(Socket sock, IMagazzino skel){
        socket = sock;
        skeleton = skel;
    }

    public void run(){
        try (
            socket;
            DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
        ) {

            System.out.println(String.format("[SKELETON] [%s] Running...", Thread.currentThread().getName()));
            String msg = input.readUTF();
            StringTokenizer tokenizer = new StringTokenizer(msg, separator);

            String method = tokenizer.nextToken();
            String articolo = tokenizer.nextToken(); // articolo c'è sempre nella request
            String response = "FAILED";
            int id = -1;

            if (method.compareTo("deposita") == 0){
                id = Integer.valueOf(tokenizer.nextToken());
                System.out.println(String.format("[SKELETON] [%s] - %s - %d", Thread.currentThread().getName(), method, id));
                skeleton.deposita(articolo, id);
                response = "SUCCESS";
                output.writeUTF(response);
                output.flush();
            } else if (method.compareTo("preleva") == 0){
                id = skeleton.preleva(articolo);
                System.out.println(String.format("[SKELETON] [%s] - %s - %d", Thread.currentThread().getName(), method, id));
                output.writeInt(id);
                output.flush();
            } else {
                System.out.println(String.format("+++[SKELETON] [%s] - %s not recognized!", Thread.currentThread().getName(), method));
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
}
