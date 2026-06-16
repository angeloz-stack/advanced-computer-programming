package loggingServer;

import javax.jms.*;

public class LoggingThread extends Thread {
    private QueueConnection conn;
    private Queue queue;
    private String messaggioLog;
    private int tipo;

    public LoggingThread(QueueConnection c, Queue q, String messaggioLog, int tipo){
        conn = c;
        queue = q;
        this.messaggioLog = messaggioLog;
        this.tipo = tipo;
    }
    
    public void run(){
        /* NOTA SU SESSION
        Qui la sessione non è attributo della classe perché resta viva solo per il la durata
        dell'operazione, quindi nel metodo run(). Invece, si guardi come contro-esempio
        output/ErrorChecker.java, dove la sessione, visto che deve restare viva anche dopo
        la fine del costruttore, viene dichiarata come attributo.
        */
        QueueSession session = null;
        try {
            session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
            QueueSender sender = session.createSender(queue);

            MapMessage msg = session.createMapMessage();
            msg.setString("messaggioLog", messaggioLog);
            msg.setInt("tipo", tipo);

            sender.send(msg);
            
            session.close();
            sender.close();
            
        } catch (JMSException e) {
            e.printStackTrace();
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (JMSException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
