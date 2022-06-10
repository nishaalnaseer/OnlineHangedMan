import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    private Socket client;
    private BufferedReader in;
    private PrintWriter out;
    private boolean done;

    public Client() {
        try {
            client = new Socket("127.0.0.1", 65000);
            out = new PrintWriter(client.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }
        Scanner scan = new Scanner(System.in);
        String message, inMessage;

        while (true) {
            System.out.print("Send to Server: ");
            message = scan.nextLine();
            out.println(message);
            try {
                inMessage = in.readLine();
                System.out.print("Server: " + inMessage + "\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws IOException {
        Client client = new Client();
    }
}
