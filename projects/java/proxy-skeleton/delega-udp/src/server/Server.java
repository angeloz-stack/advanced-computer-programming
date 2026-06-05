package server;

public class Server {
    public static void main(String[] args) {
        DispatcherImpl server = new DispatcherImpl(5);
        DispatcherSkeleton skeleton = new DispatcherSkeleton(server);
        skeleton.runSkeleton();
    }
}
