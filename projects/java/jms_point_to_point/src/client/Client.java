package client;

import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;
import java.util.Random;

public class Client {
    public static void main(String args[]) throws NamingException, JMSException{
        Random random = new Random();
        String clientCorrelationID = null;
        
        try {
            clientCorrelationID = args[0];
        } catch (IndexOutOfBoundsException e) {
            clientCorrelationID = "client-" + String.valueOf(random.nextInt());
        }
        System.out.println(String.format("[CLIENT] CorrelationID = %s", clientCorrelationID));
        
        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
        prop.put("queue.requests", "requests_queue");
        prop.put("queue.responses", "responses_queue");

        Context ctx = new InitialContext(prop);
        QueueConnectionFactory qf = (QueueConnectionFactory) ctx.lookup("QueueConnectionFactory");
        Queue queue_requests = (Queue) ctx.lookup("requests");
        Queue queue_responses = (Queue) ctx.lookup("responses");

        QueueConnection conn = qf.createQueueConnection();
        
        QueueSession session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
        
        QueueSender sender = session.createSender(queue_requests);
        QueueReceiver receiver = session.createReceiver(queue_responses, String.format("JMSCorrelationID = '%s'", clientCorrelationID));
        ClientListener listner = new ClientListener();
        receiver.setMessageListener(listner);
        conn.start();

        MapMessage msg = session.createMapMessage();

        for (int i = 0; i < 10; i++) {
            if (i<=4){
                //deposita
                msg.setString("operazione", "deposita");
                msg.setInt("valore", random.nextInt(101));      
                System.out.println(String.format("[CLIENT] (deposita n. %d) - Deposito %d", i, msg.getInt("valore")));
            } else {
                // preleva
                msg.setString("operazione", "preleva");
                System.out.println("[CLIENT] (preleva n. " + i + ")");
            }

            msg.setJMSReplyTo(queue_responses);
            msg.setJMSCorrelationID(clientCorrelationID);
            sender.send(msg);
        }
    }
}
 
 
 