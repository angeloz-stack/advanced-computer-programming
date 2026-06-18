package manager;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import javax.jms.*;
import javax.naming.*;

public class ManagerListener implements MessageListener{
    
    private TopicConnection conn;
    private Context jndiContext;
    private TopicSession session;
    private Topic tickets;
    private Topic stats;

    public ManagerListener(TopicConnection c, Context ctx){
        conn = c;
        jndiContext = ctx;

        try {
            session = conn.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);
            tickets = (Topic) jndiContext.lookup("tickets");
            stats = (Topic) jndiContext.lookup("stats");
        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }

        System.out.println("[MESSAGE LISTENER] Running...");
        
    }
    
    public void onMessage(Message message){
        MapMessage msg = (MapMessage) message;

        try{
            String type = msg.getString("type");

            System.out.println(String.format("[MESSAGE LISTENER] Ricevuta richiesta %s - %s", type, msg.getString("value")));

            TopicPublisher pub = null;
            TextMessage txt = session.createTextMessage();
            txt.setText(msg.getString("value"));

            if (type.equals("buy")){
                pub = session.createPublisher(tickets);

                // scrive su file tickets.txt

                try (
                    FileOutputStream file = new FileOutputStream("./tickets.txt", true);
                    PrintStream out = new PrintStream(file);
                ) {
                    // in questo caso il campo value contiene il nome
                    // di un cantante
                    out.println(msg.getString("value"));
                } catch (IOException e) {
                    e.printStackTrace();
                }

            } else if (type.equals("stats")){
                pub = session.createPublisher(stats);
            }

            pub.publish(txt);

        } catch (JMSException e){
            e.printStackTrace();
        }

        return;
    }
}
