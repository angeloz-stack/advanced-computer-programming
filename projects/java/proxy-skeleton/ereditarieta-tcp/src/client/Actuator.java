package client;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import dispatcher.IDispatcher;

public class Actuator {


    public static void main(String[] args) {
        // args[0] è address
        // agrs[1] è port

        String address = args[0];
        int port = Integer.valueOf(args[1]);

        IDispatcher proxy = new Proxy(address, port);
        int cmd = -1;

        try {
            FileOutputStream fileOut = new FileOutputStream("./cmdlog.txt");
            PrintStream out = new PrintStream(fileOut);

            while (true){
                cmd = proxy.getCmd();
                System.out.println(String.format("[ACTUATOR] - getCmd result: %d", cmd));
                out.println(String.format("cmd: %d", cmd));
                Thread.sleep(1000);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        
    }
}
