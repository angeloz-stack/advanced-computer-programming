package codaimpl;

import coda.Coda;
import coda.CodaWrapper;

import java.util.concurrent.Semaphore;

public class CodaWrapperSemaphore extends CodaWrapper{
    private Semaphore elemDisp;
    private Semaphore spazioDisp;

    public CodaWrapperSemaphore(Coda c){
        super(c);
        spazioDisp = new Semaphore(coda.getSize());
        elemDisp = new Semaphore(0);
    }

    public void inserisci(int i){
        try {
            spazioDisp.acquire();
            try{
                synchronized (coda) {
                    coda.inserisci(i);
            }
            } finally {elemDisp.release();}
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return;
    }

    public int preleva(){
        int x = 0;
        try {
            elemDisp.acquire();
            try {
                synchronized (coda){
                    x = coda.preleva();
                }
            } finally {spazioDisp.release();}
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return x;
    }
}
