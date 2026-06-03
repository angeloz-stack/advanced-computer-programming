package server;

import coda.*;
import codaimpl.*;

public class DispatcherImpl extends DispatcherSkeleton{
    private final CodaWrapper codaWrapper;

    public DispatcherImpl(int backlog, int size){
        super(backlog);
        Coda coda = new CodaCircolare(size);
        codaWrapper = new CodaWrapperLock(coda);
    }

    public void sendCmd(int i){
        System.out.println(String.format("[SERVER] [%s] eseguo sendCmd: %d", Thread.currentThread().getName(), i));
        codaWrapper.inserisci(i);
        return;
    }
    
    public int getCmd(){
        System.out.println(String.format("[SERVER] [%s] eseguo getCmd...", Thread.currentThread().getName()));
        int cmd = codaWrapper.preleva();
        System.out.println(String.format("[SERVER] [%s] cmd prelevato: %d", Thread.currentThread().getName(), cmd));
        return cmd;
    }
}
