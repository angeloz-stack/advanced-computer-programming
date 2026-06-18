package sensor;

import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;
import coda.interfacce.*;
import coda.impl.*;

public class Sensor implements MessageListener{

    private TopicConnection conn;
    private TopicSession session;
    private TopicSubscriber sub;
    private Topic topic;
    private Coda coda;
    private final int queue_size = 10;

    public Sensor(){

        Coda c = new CodaCircolare(queue_size);
        coda = new CodaWrapperLock(c);

        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
        prop.put("topic.cmds", "commands_topic");

        try {
            Context ctx = new InitialContext(prop);
            TopicConnectionFactory tf = (TopicConnectionFactory) ctx.lookup("TopicConnectionFactory");
            topic = (Topic) ctx.lookup("cmds");

            conn = tf.createTopicConnection();
            session = conn.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);
            sub = session.createSubscriber(topic);
            sub.setMessageListener(this);
            conn.start();
        } catch (NamingException | JMSException e){
            e.printStackTrace();
        }
    }


    public void onMessage(Message message) {
        TextMessage msg = (TextMessage) message;
        String cmd = null;
        try {cmd = msg.getText();} catch (JMSException e) {e.printStackTrace();}

        if (cmd != null){
            Thread t = new TManager(coda, cmd);
            t.start();
        }
    }

    public void run(){
        Thread t = new TExecutor(coda);
        t.start();
    }
    public static void main(){
        Sensor s = new Sensor();
        s.run();
    }
}
