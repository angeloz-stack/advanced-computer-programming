package coda.impl;

import coda.interfacce.Coda;

public class CodaCircolare implements Coda{
    private int size;
    private int head;
    private int tail;
    private int elem;
    private String data[];

    public CodaCircolare(int queue_size){
        size = queue_size;
        head=tail=elem=0;
        data = new String[size];
    }

    public int getSize(){
        return size;
    }

    public boolean empty(){
        return (elem == 0);
    }

    public boolean full(){
        return (elem == size);
    }

    public void inserisci(String i){
        data[head] = i;

        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        elem++;
        head = (head + 1) % size;
    }

    public String preleva(){
        String i = data[tail];

        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        elem--;
        tail = (tail + 1) % size;

        return i;
    }
}
