package codaimpl;

import java.util.Random;

import coda.Coda;

public class CodaCircolare implements Coda{

    private int data[];
    private int size; // lunghezza della coda
    private int tail; 
    private int head;
    private int elem; // n. elementi in coda

    public CodaCircolare(int size){
        this.size = size;
        data = new int[size];
        tail=elem=head=0;
    }

    public boolean empty(){
        return (elem == 0);
    }

    public boolean full(){
        return (size == elem);
    }

    public int getSize(){
        return size;
    }

    // prelevo in coda (tail)
    public int preleva(){

        int i = data[tail];

        try {
            Thread.sleep(new Random().nextInt(100, 201));
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        tail  = (tail + 1) % size;
        elem--;

        return i;
    }

    public void inserisci(int i){

        // inserisco in testa (head)
        data[head] = i;
        
        try {
            Thread.sleep(new Random().nextInt(100, 201));
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        head = (head + 1) % size;
        elem++;

        return;
    }

}
