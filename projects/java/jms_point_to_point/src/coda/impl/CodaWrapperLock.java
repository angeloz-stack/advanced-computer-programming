package coda.impl;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import coda.interfacce.*;

public class CodaWrapperLock extends CodaWrapper{
    private Lock lock;
    private Condition prod;
    private Condition cons;

    public CodaWrapperLock(Coda c){
        super(c);
        lock = new ReentrantLock();
        prod = lock.newCondition();
        cons = lock.newCondition();
    }

    public void inserisci(int i){
        lock.lock();
        try {
            while(coda.full()){
                prod.await();
            }
            coda.inserisci(i);
            cons.signal();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public int preleva(){
        lock.lock();
        int i = Integer.MIN_VALUE;
        try {
            while(coda.empty()){
                cons.await();
            }
            i = coda.preleva();
            prod.signal();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
        return i;
    }
}
