
import javax.naming.*;
import java.util.Hashtable;
import javax.jms.*;
import java.util.Random;

public class Client {
    
    private static final int NUM_REQS = 20;
    private static final long t_wait_ms = 2000;
    private static final String[] tipi_di_richiesta = {"buy", "stats"};
    private static final String[] campi_buy = {"Jovanotti", "Ligabue", "Negramaro"};

    public static void main(String[] args) throws NamingException, JMSException {

        String tipo_di_richiesta = args[0].toLowerCase().strip();

        boolean tipo_valido = false;
        int i = 0;

        while (i < tipi_di_richiesta.length && !tipo_valido){
            if (tipo_di_richiesta.equals(tipi_di_richiesta[i])) {
                tipo_valido = true;
            }
            i++;
        }

        if (!tipo_valido){
            throw new IllegalArgumentException(String.format("[CLIENT ERROR] Tipo di richiesta %s non valido", tipo_di_richiesta));
        }
        
        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
        prop.put("topic.request", "request_topic");

        Context ctx = new InitialContext(prop);

        TopicConnectionFactory tf = (TopicConnectionFactory) ctx.lookup("TopicConnectionFactory");
        Topic request_topic = (Topic) ctx.lookup("request");

        TopicConnection conn = tf.createTopicConnection();
        TopicSession session = conn.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);
        TopicPublisher pub = session.createPublisher(request_topic);

        Random random = new Random();

        MapMessage msg = session.createMapMessage();
        msg.setString("type", tipo_di_richiesta);

        for (int j = 0; j < NUM_REQS; j++) {
            if (tipo_di_richiesta.equals("buy")){
                String value = campi_buy[random.nextInt(campi_buy.length)];
                System.out.println("[INVIO BUY] - "+ value);
                msg.setString("value", value);
            } else if (tipo_di_richiesta.equals("stats")){
                msg.setString("value", "Sold");
                System.out.println("[INVIO STATS] - Sold");
            }
            
            pub.publish(msg);
        }





    }
}
