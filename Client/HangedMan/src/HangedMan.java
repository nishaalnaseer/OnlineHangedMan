import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.io.*;

public class HangedMan extends WindowAdapter implements ActionListener {
    // sections
        // GUI
        // connect() that connects to server
        // processing functions

    // GUI attributes
    private JFrame frame = new JFrame("Hanged Man");
    private JTextField input;
    private JLabel pic, score_label, level_label, tracker_label;
    private String tracker = "Letters entered = ";
    private String progress, last_word;
    private int count, level, score;
    private boolean signedin = false;
    private JButton connect;
    private JButton signin;
    private JButton signup;
    private JButton hi_sco;

    // network attributes
    private String host_ip;
    private int port;

    public HangedMan() throws Exception {
        pic = new JLabel();
        score_label = new JLabel();
        level_label = new JLabel();
        tracker_label = new JLabel();
        frame.setSize(500, 400);
        score_label.setBounds(230,0,150,20);
        level_label.setBounds(432,0,150,20);
        tracker_label.setBounds(80,340,200,20);
        pic.setBounds(10, 10, 500, 218);
        frame.add(level_label);
        frame.add(pic);
        frame.add(score_label);
        frame.add(tracker_label);

        signin =new JButton("Signin");
        signin.setBounds(130,200,95,30);
        frame.add(signin);
        signup = new JButton("Signin");
        signup.setBounds(275,200,95,30);
        frame.add(signup);
        hi_sco = new JButton("High Scores");
        hi_sco.setBounds(185,150,130,30);
        frame.add(hi_sco);
        connect = new JButton("Connect");
        connect.setBounds(202,50,95,30);
        frame.add(connect);

        frame.setLayout(null);
        frame.setResizable(false);
        frame.setVisible(true);

        connect.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                hide_all();
                try {
                    load_config();
                } catch (IOException ex) {
                    // TODO handle exception through pop window;
                }
                JButton connect_to_server = new JButton("Connect to " + host_ip + ":" + port);
                connect_to_server.setBounds(150,150,200,30);
                frame.add(connect_to_server);

                JTextField new_ip = new JTextField("New IP");
                JTextField new_port = new JTextField("New Port");
                JButton new_addr = new JButton("Connect to new Address");
                new_ip.setBounds(57, 250, 100, 30);
                new_port.setBounds(163, 250, 80, 30);
                new_addr.setBounds(253, 250, 190, 30);

                frame.add(new_ip);
                frame.add(new_port);
                frame.add(new_addr);

            }
        });
    }

    public void hide_all() {
        connect.setVisible(false);
        pic.setVisible(false);
        level_label.setVisible(false);
        score_label.setVisible(false);
        tracker_label.setVisible(false);
        signin.setVisible(false);
        signup.setVisible(false);
        hi_sco.setVisible(false);
    }

    public void load_config() throws IOException {
        File file = new File("src\\config");
        BufferedReader br = new BufferedReader(new FileReader(file));

        String word = "";
        String line = br.readLine();
        int line_len = line.length();
        char ch;
        int i = 0;
        String[] content = new String[2];
        for (int x = 0; x < line_len; x++) {
            ch = line.charAt(x);

            if ((ch == ',') || (ch == '\n')) {
                content[i] = word;
                i++;
                word = "";
            } else {
                word = word + line.charAt(x);
            }
        }
        br.close();
        host_ip = content[0];
        try {
            port = Integer.parseInt(content[1]);
        } catch (NumberFormatException e) {
            // TODO show error to GUI
        }

    }

    public void save_config() throws IOException {
        File file = new File("src\\config");

        FileWriter wr = new FileWriter(file);
        wr.write(host_ip + "," + port + ",");
        wr.close();
    }

    @Override
    public void actionPerformed(ActionEvent e) {

    }

    public static void main(String[] args) throws Exception{
        HangedMan game = new HangedMan();
    }

}
