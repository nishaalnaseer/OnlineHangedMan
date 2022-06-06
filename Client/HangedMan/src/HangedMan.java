import javax.swing.*;
import java.awt.event.*;
import java.io.*;
import java.net.Socket;
import java.net.SocketException;

public class HangedMan extends WindowAdapter implements ActionListener {
    // sections
    // GUI
    // connect() that connects to server
    // processing functions

    // GUI attributes
    private JFrame frame = new JFrame("Hanged Man");
    private JTextField input;
    private final JLabel pic, score_label, level_label, tracker_label;
    private String tracker = "Letters entered = ";
    private String progress, last_word;
    private int count, level, score;
    private boolean signedin = false;
    private final JButton connect;
    private final JButton signin;
    private final JButton signup;
    private final JButton hi_sco;

    // network attributes
    private String host_ip;
    private int port;
    private Socket client;
    private PrintWriter out;
    private BufferedReader in;

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
        signup = new JButton("Signin");
        signup.setBounds(275,200,95,30);
        hi_sco = new JButton("High Scores");
        hi_sco.setBounds(185,150,130,30);
        connect = new JButton("Connect");
        connect.setBounds(202,185,95,30);
        frame.add(connect);

        frame.setLayout(null);
        frame.setResizable(false);
        frame.setVisible(true);

        connect.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                hide_all();
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

                try {
                    if (load_config() == false) {
                        connect_to_server.setVisible(false);
                    }
                    else {
                        connect_to_server.setText("Connect to " + host_ip + ":" + port);
                    }
                } catch (IOException ex) {
                    // TODO handle exception through pop window;
                }

                new_ip.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mouseClicked(MouseEvent e) {
                        new_ip.setText("");
                    }
                });

                new_port.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mouseClicked(MouseEvent e) {
                        new_port.setText("");
                    }
                });

                new_addr.addActionListener(new ActionListener() {
                    @Override
                    public void actionPerformed(ActionEvent e) {
                        String ip_text = new_ip.getText();
                        String port_text = new_port.getText();

                        if ((ip_text.equals("")) || (port_text.equals("")) || (ip_text.equals(null))
                                || (port_text.equals(null)) || (ip_text.equals("New IP")) || (port_text.equals("New Port")))
                        {

                        } else {
                            final boolean addr_ok = check_ip_port(ip_text + ":" + port_text);

                            if (addr_ok) {
                                try {
                                    save_config();
                                } catch (IOException ex) {
                                    throw new RuntimeException(ex);
                                }
                                connect_to_server.setText("Connect to " + host_ip + ":" + port);
                                server_connect_func();
                            }
                        }
                    }
                });
                connect_to_server.addActionListener(new ActionListener() {
                    @Override
                    public void actionPerformed(ActionEvent e) {
                        server_connect_func();
                    }
                });
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

    public boolean load_config() throws IOException {
        File file = new File("src\\config");
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line = br.readLine();
        if ((line == null) || (check_ip_port(line) == false)) {
            JOptionPane.showMessageDialog(frame, "Corrupt save file");
            return false;
        }
        return true;
    }

    public void save_config() throws IOException {
        File file = new File("src\\config");

        FileWriter wr = new FileWriter(file);
        wr.write(host_ip + ":" + port);
        wr.close();
    }

    public boolean check_ip_port(String ip_port) {
        char ch;
        int i;
        int section_num = 0;
        int str_len = ip_port.length();
        String section = "";
        int[] addr = new int[5];

        for (i = 0; i < str_len; i++) {
            ch = ip_port.charAt(i);
            int section_val;

            if ((ch == '.') || (ch == ':')) {

                try {
                    section_val = Integer.parseInt(section);
                }
                catch (NumberFormatException int_e) {
                    JOptionPane.showMessageDialog(frame, "Invalid chars in IP");
                    return false;
                }

                if ((section_val > 254) || (section_val < 0)) {
                    JOptionPane.showMessageDialog(frame, "Invalid IP address!");
                    return false;
                }

                addr[section_num] = section_val;
                section_num++;
                if (section_num > 4) {
                    JOptionPane.showMessageDialog(frame, "Incorrect Format!");
                    return false;
                }
                section = "";

            } else {
//                if (ch == ';') {
//                    section = "";
//                }
                section += ch;

                if (i == str_len-1) {
                    try {
                        section_val = Integer.parseInt(section);
                    }
                    catch (NumberFormatException int_e) {
                        JOptionPane.showMessageDialog(frame, "Invalid chars in Port");
                        return false;
                    }

                    if ((section_val < 0) || (section_val > 65535)) {
                        JOptionPane.showMessageDialog(frame, "Invalid Port! Port must be between 0 and 65535");
                        return false;
                    }
                    addr[section_num] = section_val;
                }
            }
        }
        if (section_num != 4) {
            JOptionPane.showMessageDialog(frame, "Incorrect Format");
            return false;
        }

        if ((addr[0] == 0) || (addr[3] == 0)) {
            JOptionPane.showMessageDialog(frame, "Invalid IP address!");
            return false;
        }
        host_ip = addr[0] + "." + addr[1] + "." + addr[2] + "." + addr[3];
        port = addr[4];
        return true;
    }

    @Override
    public void actionPerformed(ActionEvent e) {

    }

    public void server_connect_func() {
        boolean ok = true;

        try {
            client = new Socket(host_ip, port);
            out = new PrintWriter(client.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        } catch (SocketException e) {
            ok = false;
            JOptionPane.showMessageDialog(frame, "Connection Error. Check ip:port or if host is up.");
        } catch (IOException e) {
            ok = false;
            JOptionPane.showMessageDialog(frame, "IOException");
        }
        if (ok == true) {
            connect.setBounds(395,40,95,30);
        }
    }

    public static void main(String[] args) throws Exception {
        HangedMan Game = new HangedMan();
    }
}
