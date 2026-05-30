package buffer;

public class Buffer {

    private long content;
    private boolean full;

    public Buffer() {
        content = 0;
        full = false; // false = buffer vuoto, true = buffer pieno
    }

    public synchronized void produci() {
        System.out.println(Thread.currentThread().getName() + ": invocazione produci");

        while (full) {
            System.out.println(Thread.currentThread().getName() + ": in attesa (buffer pieno)");
            try {
                wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        content = System.currentTimeMillis();
        System.out.println(Thread.currentThread().getName() + ": prodotto = " + content);

        full = true;
        notifyAll();
    }

    public synchronized void consuma() {
        System.out.println(Thread.currentThread().getName() + ": invocazione consuma");

        while (!full) {
            System.out.println(Thread.currentThread().getName() + ": in attesa (buffer vuoto)");
            try {
                wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println(Thread.currentThread().getName() + ": consumato = " + content);

        full = false;
        notifyAll();
    }
}
