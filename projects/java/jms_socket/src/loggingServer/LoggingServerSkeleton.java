package loggingServer;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public abstract class LoggingServerSkeleton implements ILogging{

    void runSkeleton(){
        try (
            ServerSocket socket = new ServerSocket(0);
        ) {
            System.out.println(String.format("[SERVER] In ascolto sulla porta: %d", socket.getLocalPort()));
            Socket conn;
            while (true){
                conn  = socket.accept();
                Thread t = new Worker(conn, this);
                t.start();
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
