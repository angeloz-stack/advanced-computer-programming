package codaimpl;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import coda.CodaWrapper;
import coda.Coda;

public class CodaWrapperLock extends CodaWrapper{
    
    // visto che in CodaWrapper non c'è un no-arg
    // constrctor, qui dobbiamo esplicitamente chiamare
    // super(...)

    private Lock lock;
    private Condition prod;
    private Condition cons;

    public CodaWrapperLock(Coda c){
        super(c);

        lock = new ReentrantLock();
        prod =  lock.newCondition();
        cons = lock.newCondition();
    }

    public void inserisci(int i){
        
        lock.lock();
        try {
            while(coda.full()){
                try {
                    prod.await();
                } catch (InterruptedException e){
                    e.printStackTrace();
                }
            }
            coda.inserisci(i);
            cons.signal();

        }
        finally {
            lock.unlock();
        }

        return;
    }

    public int preleva(){
        int x = 0;
        lock.lock();
        try{
            while(coda.empty()){
                try {
                    cons.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            x = coda.preleva();
            prod.signal();
        } finally {
            lock.unlock();
        }

        return x;
    }

}
