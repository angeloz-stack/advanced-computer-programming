package loggingServer;

public class MainServer {
    public static void main(String[] args) {
        
        LoggingServerImpl server = new LoggingServerImpl();
        server.runSkeleton();

        // usage da jms_socket/
        // $ java -cp "lib/activemq-all-5.16.6.jar:out" loggingServer.MainServer
    }
}
