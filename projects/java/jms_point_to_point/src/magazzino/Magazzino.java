package magazzino;
import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;
import coda.impl.*;

public class Magazzino implements MessageListener{

    private QueueConnection conn;
    private QueueSession session;
    private QueueReceiver receiver;
    private Queue queue_requests;
    private final CodaWrapperLock coda;

    public Magazzino(){

        CodaCircolare coda_circolare = new CodaCircolare(10);
        coda = new CodaWrapperLock(coda_circolare);

        try {
            Hashtable<String, String> prop = new Hashtable<String, String>();
            
            prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
            prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
            prop.put("queue.requests", "requests_queue");

            Context ctx = new InitialContext(prop);
            QueueConnectionFactory qf = (QueueConnectionFactory) ctx.lookup("QueueConnectionFactory");
            queue_requests = (Queue) ctx.lookup("requests");

            conn = qf.createQueueConnection();
            session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
            receiver = session.createReceiver(queue_requests);
            receiver.setMessageListener(this);
            conn.start();
        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }


    }


    public void onMessage(Message message){
        
        MapMessage msg = (MapMessage) message;
        Thread t = new Worker(conn, msg, coda);
        t.start();
    
        return;
    }

    public static void main(String args[]){
        Magazzino m = new Magazzino();
        System.out.println("[MAGAZZINO] Running...");
    }

}
