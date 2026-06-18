package client;

import javax.jms.*;

public class ClientListener implements MessageListener{

    public void onMessage(Message message){
        TextMessage msg = (TextMessage) message;

        try {
            System.out.println(String.format("[CLIENT - LISTENER] - Ricevuto: %s", msg.getText()));
        } catch (JMSException e){
            e.printStackTrace();
        }
    }


}
