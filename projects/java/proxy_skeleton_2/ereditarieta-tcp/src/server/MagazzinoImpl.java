package server;

import coda.*;
import codaimpl.CodaCircolare;
import codaimpl.CodaWrapperLock;

public class MagazzinoImpl extends Skeleton{
    private final CodaWrapper coda_smartphone;
    private final CodaWrapper coda_laptop;
    private final int QUEUE_SIZE = 5;

    public MagazzinoImpl(){
        coda_smartphone = new CodaWrapperLock(new CodaCircolare(QUEUE_SIZE));
        coda_laptop = new CodaWrapperLock(new CodaCircolare(QUEUE_SIZE));
    }

    public void deposita(String articolo, int id){
        System.out.println(String.format("[MAGAZZINO] - Deposito %s id: %d", articolo, id));

        if (articolo.compareTo("laptop") == 0){
            coda_laptop.inserisci(id);
        } else if (articolo.compareTo("smartphone") == 0) {
            coda_smartphone.inserisci(id);
        } else {
            System.out.println(String.format("[MAGAZZINO] - Article %s not recognized", articolo));
        }
    }

    public int preleva(String articolo){
        System.out.println(String.format("[MAGAZZINO] - Prelevo %s", articolo));
        int id = -1;
        if (articolo.compareTo("laptop") == 0){
            id = coda_laptop.preleva();
        } else if (articolo.compareTo("smartphone") == 0) {
            id = coda_smartphone.preleva();
        } else {
            System.out.println(String.format("[MAGAZZINO] - Article %s not recognized", articolo));
        }
        return id;
    }
}
