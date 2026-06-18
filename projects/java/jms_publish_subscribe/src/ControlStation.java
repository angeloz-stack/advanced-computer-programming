
import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;
import java.util.Random;

public class ControlStation {

    private static final String cmds[] = {"startSensor", "stopSensor", "read"};

    public static void main(String args[]) throws NamingException, JMSException{

        TopicConnection conn;
        TopicSession session;
        TopicPublisher pub;
        Topic topic;

        Random random = new Random();

        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
        prop.put("topic.cmds", "commands_topic");

        Context ctx = new InitialContext(prop);
        TopicConnectionFactory tf = (TopicConnectionFactory) ctx.lookup("TopicConnectionFactory");
        topic = (Topic) ctx.lookup("cmds");

        conn = tf.createTopicConnection();
        session = conn.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);
        pub = session.createPublisher(topic);

        int N = Integer.valueOf(args[0]);
        TextMessage msg = session.createTextMessage();
        String cmd;

        for(int i = 0; i < N; i++){
            cmd = cmds[random.nextInt(cmds.length)];
            msg.setText(cmd);
            pub.publish(msg);
        }

        conn.close();
        session.close();
        pub.close();
    }
}
