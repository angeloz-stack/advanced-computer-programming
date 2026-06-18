package sensor;

import java.io.*;
import coda.interfacce.Coda;

public class TExecutor extends Thread{
    private Coda coda;

    public TExecutor(Coda c){
        coda = c;
    }

    public void run(){
        String cmd;
        while (true){
            cmd = coda.preleva();
            System.out.println(String.format("[TExecutor] (%s) Prelevato %s dalla coda", Thread.currentThread().getName(), cmd));

            try(
                FileOutputStream file = new FileOutputStream("./CmdLog.txt", true);
                PrintStream out = new PrintStream(file);
            ){
                out.println(cmd);
            } catch (IOException e){
                e.printStackTrace();
            }
        }
    }
}
