package loggingServer;

import java.util.Hashtable;
import javax.jms.*;
import javax.naming.*;

public class LoggingServerImpl extends LoggingServerSkeleton{
    
    // ------------------------------------------------------------------------------------------------------------------
    private Hashtable<String, String> prop = new Hashtable<String, String> ();
    private QueueConnection conn;
    private Queue queue_info;
    private Queue queue_error;
    
    public LoggingServerImpl(){
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put( "java.naming.provider.url", "tcp://127.0.0.1:61616" );
        prop.put("queue.info", "infoqueue");
        prop.put("queue.error", "errorqueue");
        
        try {
            Context jndiContext = new InitialContext(prop);
            QueueConnectionFactory connFactory = (QueueConnectionFactory) jndiContext.lookup("QueueConnectionFactory");
            queue_info = (Queue) jndiContext.lookup("info");
            queue_error = (Queue) jndiContext.lookup("error");
            conn = connFactory.createQueueConnection();
        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
    }
    // ------------------------------------------------------------------------------------------------------------------

    public void log(String messaggioLog, int tipo){
        Queue to_send;

        if (tipo == 2){
            to_send = queue_error;
        } else {
            to_send = queue_info;
        }

        boolean conn_is_valid = true;
        if (conn == null) conn_is_valid = false;

        System.out.println(String.format("[DEBUG] [SERVER] - Creo thread, conn is valid: %b", conn_is_valid));
        Thread logginThread = new LoggingThread(conn, to_send, messaggioLog, tipo);
        logginThread.start();
        
        try {
            logginThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
