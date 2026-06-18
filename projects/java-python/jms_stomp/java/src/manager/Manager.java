package manager;

import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;

public class Manager {
    public static void main(String args[]) throws NamingException, JMSException{

        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
        prop.put("topic.request", "request_topic");
        prop.put("topic.tickets", "tickets_topic");
        prop.put("topic.stats", "stats_topic");

        Context ctx = new InitialContext(prop);

        TopicConnectionFactory tf = (TopicConnectionFactory) ctx.lookup("TopicConnectionFactory");
        Topic request_topic = (Topic) ctx.lookup("request");

        TopicConnection conn = tf.createTopicConnection();
        TopicSession session = conn.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);
        TopicSubscriber sub = session.createSubscriber(request_topic);
        sub.setMessageListener(new ManagerListener(conn, ctx));
        conn.start();
    }
}
