package codaimpl;

import coda.*;

public class CodaWrapperSynchr extends CodaWrapper{
    public CodaWrapperSynchr(Coda c){
        super(c);
    }

    public void inserisci(int i){

        synchronized (coda){
            // monitor ""built-in"

            while(coda.full()){
                try {
                    coda.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            coda.inserisci(i);
            coda.notifyAll();
        }
        return;
    }

    public int preleva(){
        int x = 0;

        synchronized(coda){
            while(coda.empty()){
                try {
                    coda.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            x = coda.preleva();
            coda.notifyAll();
        }
        return x;
    }
}
