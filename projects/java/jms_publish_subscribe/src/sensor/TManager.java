package sensor;
import coda.interfacce.Coda;

public class TManager extends Thread{
    private Coda coda;
    private String cmd;

    public TManager(Coda c, String cmd){
        coda = c;
        this.cmd = cmd;
    }

    public void run(){
        System.out.println(String.format("[TExecutor] (%s) Inserisco %s in coda", Thread.currentThread().getName(), cmd));
        coda.inserisci(cmd);
    }

}
