package output;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Hashtable;
import javax.jms.*;
import javax.naming.*;

public class ErrorChecker implements MessageListener{
    private static final String[] messaggiLogErr = {"fatal", "exception"};
    private String msg_to_write;
    private Hashtable<String, String> prop = new Hashtable<String, String> ();
    private QueueConnection conn;
    private Queue queue;
    private QueueSession session; // la sessione qui viene dichiarata come attributo perché deve continuare ad esistere dopo il costruttore
    private QueueReceiver receiver;


    public ErrorChecker(String msg_to_write){
        this.msg_to_write = msg_to_write;

        // setup jms
        // ------------------------------------------------------------------------------------------------------------------
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put( "java.naming.provider.url", "tcp://127.0.0.1:61616" );
        prop.put("queue.error", "errorqueue");
        
        try {
            Context jndiContext = new InitialContext(prop);
            QueueConnectionFactory connFactory = (QueueConnectionFactory) jndiContext.lookup("QueueConnectionFactory");
            queue = (Queue) jndiContext.lookup("error");
            
            conn = connFactory.createQueueConnection();
            session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
            receiver = session.createReceiver(queue);
            receiver.setMessageListener(this); // gli passo `this` perché ErrorChecker implementa MessageListener
            
            conn.start();
        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
        // ------------------------------------------------------------------------------------------------------------------
    }

    public void onMessage(Message message){
        MapMessage msg = (MapMessage) message;
        String messaggioLog = null;
        try{
            messaggioLog = msg.getString("messaggioLog");
        } catch (JMSException e){
            e.printStackTrace();
        }

        /* NOTA SUL FILTRO DEI MESS IN INGRESSO
        Nella traccia c'è esplicitamente scritto: "il listener JMS di Error Checker estrae il
        contenuto del messaggio, verifica se esso contiene la stringa ricevuta in input". Se
        non fosse stato scritto esplicitamente, si sarebbe potuto pensare di applicare un filtro
        a livello broker, quindi direttamente nel receiver, e.g.:
                                                                    // sintassi tipo SQL
        QueueReceiver receiver = session.createReceiver(queue, "messaggioLog LIKE '%fatal%'")

        Questo comportamento, spesso usato per il JMSCorrelationID, in realtà così non è
        applicabile, perchè messaggioLog È UN CAMPO DI UN MAPMESSAGE E NON è UNA PROPRIETA',
        QUINDI IL BROKER NON PUOI AVERVI HA ACCESSO!
        */

        if (messaggioLog != null && messaggioLog.contains(msg_to_write)){
            System.out.println(String.format("[ERROR CHECKER] - Scrivo messaggioLog: %s", messaggioLog));
            
            /* NOTA SU FILEOUTPUTSTREAM
            Qui ci va append=True, e viene spontaneo pensare, perché? In molti esercizi simili, non l'avevo mai messo.
            La ragione giace nel fatto che negli altri esercizi aprivo il file 1 SOLA VOLTA e in un while (...)
            facevo println. Qui invece il file viene aperto (e chiuso) a ogni messaggio ricevuto (siamo nella funzione
            onMessage!!), quindi senza append si andrebbe a sovrascrivere ogni volta il contenuto del file.
            */

            try (
                FileOutputStream file = new FileOutputStream("./error.txt", true);
                PrintStream out = new PrintStream(file)
            ) {
                out.println(messaggioLog);
            } catch (IOException e){
                e.printStackTrace();
            }
            
        } else {
            System.out.println(String.format("[ERROR CHECKER] - Non scrivo messaggioLog: %s (not allowed)", messaggioLog));
        }
    }

    public static void main(String args[]){
        String allowed_message = args[0].toLowerCase().strip();
        boolean valido = false;
        int i = 0;

        while (i < messaggiLogErr.length && !valido){
            if (allowed_message.compareTo(messaggiLogErr[i]) == 0) valido = true;
            i++;
        }

        if (!valido) throw new IllegalArgumentException(String.format("%s non valido", allowed_message));

        ErrorChecker checker = new ErrorChecker(allowed_message);


        // runna così (se hai compilato tutto in out/) da jms_socket/
        // $ java -cp "lib/activemq-all-5.16.6.jar:out" output.ErrorChecker fatal (o exception)

    }
}
