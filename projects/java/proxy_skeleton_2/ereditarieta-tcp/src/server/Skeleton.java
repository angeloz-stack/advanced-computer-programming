package server;

import java.io.IOException;
import java.net.*;

public abstract class Skeleton implements IMagazzino{
    private final int backlog = 10;

    public void runSkeleton(){
        try (ServerSocket socket = new ServerSocket(0, backlog)) {
            System.out.println(String.format("[SERVER] - Listening on port: %d", socket.getLocalPort()));
            while (true){
                Socket conn = socket.accept();
                SkeletonThread t = new SkeletonThread(conn, this);
                t.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
