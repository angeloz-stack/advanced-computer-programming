package server;

import coda.CodaWrapper;
import codaimpl.CodaCircolare;

public class MainServer {

    private static final int size = 5;
    public static void main(String[] args) {
        
        MagazzinoImpl m = new MagazzinoImpl();
        m.runSkeleton();
    }
}
