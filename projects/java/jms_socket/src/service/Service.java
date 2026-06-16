package service;

import java.util.Random;

public class Service {
    private static final String[] messaggiLogInfo = {"success", "checking"};
    private static final String[] messaggiLogErr = {"fatal", "exception"};
    private static final int NUM_REQS = 10;

    public static void main(String[] args) {

        int port = Integer.valueOf(args[0]);

        Random random = new Random();
        Proxy proxy = new Proxy(port);

        for (int i = 0; i < NUM_REQS; i++) {
            int tipo = random.nextInt(0,3);
            String messaggioLog;
            
            if (tipo == 2) {
                messaggioLog = messaggiLogErr[random.nextInt(0,2)];
            } else {
                messaggioLog = messaggiLogInfo[random.nextInt(0,2)];
            }

            proxy.log(messaggioLog, tipo);
        }
    }




}
