package magazzino;

import coda.interfacce.*;
import javax.jms.*;

public class Worker extends Thread{
    private Coda coda;
    private QueueConnection conn;
    private QueueSession session;
    private QueueSender sender;
    private MapMessage msg;

    public Worker(QueueConnection c, MapMessage m, Coda coda){
        this.coda = coda;
        conn = c;
        msg = m;

        try {
            session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
        } catch (JMSException e){
            e.printStackTrace();
        }
    }

    public void run(){
        try {
            String operazione = msg.getString("operazione");
            String corrID = msg.getJMSCorrelationID();
            Queue queue_responses = (Queue) msg.getJMSReplyTo();
            sender = session.createSender(queue_responses);
            TextMessage txt = session.createTextMessage();

            if (operazione.equalsIgnoreCase("deposita")){
                int id_articolo = msg.getInt("valore");
                System.out.println(String.format("[WORKER] (%s) (servendo %s) Inserisco %d",Thread.currentThread().getName(), corrID, id_articolo));
                coda.inserisci(id_articolo);
                txt.setText("OK");
            } else if (operazione.equalsIgnoreCase("preleva")){
                int i = coda.preleva();
                System.out.println(String.format("[WORKER] (%s) (servendo %s) Prelevato %d",Thread.currentThread().getName(), corrID, i));
                txt.setText(String.valueOf(i));
            } else {
                System.out.println("[CLIENT ERROR] Operazione sconosciuta.");
                txt.setText("[CLIENT ERROR] Operazione sconosciuta.");
            }

            txt.setJMSCorrelationID(corrID);
            sender.send(txt);

        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
}
