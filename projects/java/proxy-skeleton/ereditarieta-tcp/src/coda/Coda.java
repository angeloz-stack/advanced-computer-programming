package coda;

public interface Coda {
    public boolean empty();
    public boolean full();
    public int getSize();
    public int preleva();
    public void inserisci(int i);
}
