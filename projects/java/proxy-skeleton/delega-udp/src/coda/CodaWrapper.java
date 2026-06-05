package coda;

public abstract class CodaWrapper implements Coda{

    protected Coda coda;

    public CodaWrapper(Coda c){
        coda = c;
    }

    // per questi metodi rimando alla Coda "wrappata"

    public boolean empty(){
        return coda.empty();
    }

    public boolean full(){
        return coda.full();
    }

    public int getSize(){
        return coda.getSize();
    }
}
