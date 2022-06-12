//import org.jetbrains.annotations.NotNull;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.Socket;
import java.net.SocketException;

public class HangedMan extends WindowAdapter implements ActionListener {
    // sections
    // GUI
    // connect() that connects to server
    // processing functions

    // some game attributes
    String saved_username;
    String saved_password;
    String[] game_args;

    // GUI attributes
    private final JFrame frame = new JFrame("Hanged Man");
    private JTextField input;
    private final JLabel pic, score_label, level_label, tracker_label, hi_sco_label;
    private String tracker = "Letters entered = ";
    private String progress, last_word, hi_sco;
    private String level, score;
    private int count;
    private boolean signedin = false;
    private final JButton connect;
    private final JButton signin;
    private final JButton signup;
    private final JLabel info;
    private final JButton hi_sco_button;
    private final String img_path = "src\\img\\img";
    private final JButton change_level;
    private final JButton submit;
    private final JTextField letters;
    private final JButton new_game;

    // network attributes
    private String host_ip;
    private int port;
    private Socket client;
    private PrintWriter out;
    private BufferedReader in;
//    frame.setSize(500, 400);

    public HangedMan() {
        pic = new JLabel();
        score_label = new JLabel("Your score: " + score);
        level_label = new JLabel("Next level: " + level);
        tracker_label = new JLabel("Letters you have entered: ");
        hi_sco_label = new JLabel("High score: " + hi_sco);
        frame.setSize(500, 400);
        hi_sco_label.setBounds(200, 0, 150,20);
        score_label.setBounds(410,25,150,20);
        level_label.setBounds(420,0,150,20);
        tracker_label.setBounds(10,340,200,20);
        pic.setBounds(10, 10, 500, 218);
        frame.add(level_label);
        frame.add(hi_sco_label);
        hi_sco_label.setVisible(false);
        frame.add(pic);
        frame.add(score_label);
        frame.add(tracker_label);
        info = new JLabel("Signing or signup and signin");
        info.setBounds(170,100,190,50);
        frame.add(info);
        info.setVisible(false);
        Font f = new Font("comic-sans", Font.BOLD, 30);
        pic.setFont(f);
        change_level = new JButton("Change Level");
        frame.add(change_level);
        change_level.setVisible(false);
        change_level.setBounds(330, 330, 150, 30);

        signin = new JButton("Signin");
        signin.setBounds(130,200,95,30);
        signup = new JButton("Signin");
        signup.setBounds(275,200,95,30);
        hi_sco_button = new JButton("High Scores");
        hi_sco_button.setBounds(185,150,130,30);
        connect = new JButton("Connect");
        connect.setBounds(202,185,95,30);
        frame.add(connect);
        submit = new JButton("Submit");
        letters = new JTextField("Letters");
        submit.setBounds(290,290,75,20);
        letters.setBounds(135,290,150,20);
        new_game = new JButton("New Game");
        new_game.setBounds(202,185,95,30);
        frame.add(new_game);
        new_game.setVisible(false);
        new_game.setBounds(0, 240, 105, 30);
        frame.add(submit);
        frame.add(letters);
        submit.setVisible(false);
        letters.setVisible(false);
        letters.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (letters.getText().equals("Letters")) {
                    letters.setText("");
                }
            }
        });
        hide_all();

        frame.setLayout(null);
        frame.setResizable(false);
        frame.setVisible(true);

        connect.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                hide_all();
                connect.setVisible(false);
                frame.remove(connect);
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
                new_addr.setVisible(true);
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
                                boolean state = server_connect_func();

                                if (state) {
                                    new_addr.setVisible(false);
                                    new_ip.setVisible(false);
                                    new_port.setVisible(false);
                                    connect_to_server.setVisible(false);

                                    signin_screen();
                                }
                            }
                        }
                    }
                });
                connect_to_server.addActionListener(new ActionListener() {
                    @Override
                    public void actionPerformed(ActionEvent e) {
                        boolean state = server_connect_func();

                        if (state) {
                            new_addr.setVisible(false);
                            new_ip.setVisible(false);
                            new_port.setVisible(false);
                            connect_to_server.setVisible(false);

                            signin_screen();
                        }
                    }
                });
            }
        });
    }

    private void update_display() {
        level_label.setText("Level: " + level);
        score_label.setText("Score: " + score);
        hi_sco_label.setText("High Score: " + hi_sco);
        ImageIcon icon = new ImageIcon(img_path + count + ".png");
        pic.setText(progress);
        pic.setIcon(icon);
    }

    private void after_submitting() {
        String function = game_args[0];

        switch (function) {
            case "update":
                progress = game_args[1];
                count = Integer.parseInt(game_args[2]);
                score = game_args[3];

            case "nextword":
                progress  = game_args[1];
                last_word = game_args[2];
                score = game_args[3];
                tracker = "Letters entered = ";
                if (Integer.parseInt(score) > Integer.parseInt(hi_sco)) {
                    hi_sco = score;
                }
                hi_sco_label.setText("High score: " + hi_sco);
                tracker_label.setText(tracker);

            case "code0010:a":
                count = 7;
                submit.setVisible(false);
                letters.setVisible(false);
                change_level.setVisible(false);

            case "new_game":
                count = 0;
                change_level.setVisible(true);
                submit.setVisible(true);
                letters.setVisible(true);
                tracker = "Letters entered = ";
        }
        update_display();
    }

    private boolean decorder(String from_server) {

        String[] args = from_server.split(" ");
        String code = args[0];
        int code_len = code.length();
        char endswith = code.charAt(code_len-1);

        if (code.startsWith("code")) {
            if (endswith == 's' || endswith == 'g'); {
                switch (code) {
                    case "code0001:s":
                        JOptionPane.showMessageDialog(frame, "Successfully signed up");
                        return false;
                    case "code0004:s":
                        game_args = args;
                        return true;
                }
            }
        } else {
            String decoded = return_server_messages(code);
            JOptionPane.showMessageDialog(frame, decoded);
        }
        return  false;
    }

    private String return_server_messages(String code) {
        switch(code) {
            case "code0000:f":
                return "No spaces in username or password allowed";
            case "code0001:f" :
                return "Incorrect number of args";
            case "code0001:i" :
                return "Username already taken";
            case "code0001:s" :
                return "Successfully signed up";
            case "code0001:a" :
                return "You have created too many users for now";
            case "code0002:f":
                return "Username not on server";
            case "code0003:f":
                return "Username or password missing on input";
            case "code0004:c":
                return "Your password is wrong";
            case "code0004:i":
                return "Username or password missing on input";
            case "code0004:j":
                return "Too many arguments";
            case "code0004:u":
                return "Username not on Server";
            case "code0005:f":
                return "Incorrect input";
            case "code0006:f":
                return "no input";
            case "code0007:f":
                return "Incorrect number of arguments";
            case "code0007:a":
                return "Zerodivison error";
            case "code0008:f":
                return "Incorrect number of arguments. hax?";
            case "code0009:f":
                return "Invalid input";
            case "code0010:a":
                return "You are dead";
            default :
                return "Unknown error contact server admin: " + code;
        }
    }

    private void signin_screen() {
        info.setVisible(true);
        JButton signin_to_server = new JButton("Signin");
        signin_to_server.setBounds(300, 185, 80, 30);
        JButton signup_to_server = new JButton("Signup");
        signup_to_server.setBounds(300, 225, 80, 30);

        JTextField signin_user_name_label = new JTextField(saved_username);
        signin_user_name_label.setBounds(125, 185, 80, 30);
        JPasswordField signin_password = new JPasswordField(saved_password);
        signin_password.setBounds(210, 185, 80, 30);
        JTextField signup_user_name_label = new JTextField("Username");
        signup_user_name_label.setBounds(125, 225, 80, 30);
        JPasswordField signup_password = new JPasswordField("password");
        signup_password.setBounds(210, 225, 80, 30);
        signin_user_name_label.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                signin_user_name_label.setText("");
            }
        });
        signin_password.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                signin_password.setText("");
            }
        });
        signup_user_name_label.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                signup_user_name_label.setText("");
            }
        });
        signup_password.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                signup_password.setText("");
            }
        });

        signin_to_server.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String username = signin_user_name_label.getText();
                char[] ch_password = signin_password.getPassword();
                boolean ok = check_username_password(username, ch_password);

                if (ok) {
                    String message = "signin " + saved_username + " " + saved_password;
                    out.println(message);
                    try {
                        String from_server = in.readLine();
                        signedin = decorder(from_server);
                        System.out.println(from_server);
                    } catch (IOException ex) {
                        throw new RuntimeException(ex);
                    }

                    if (signedin) {
                        try {
                            save_config();
                        } catch (IOException ex) {
                            throw new RuntimeException(ex);
                        }

                        signin_to_server.setVisible(false);
                        signup_to_server.setVisible(false);
                        signin_user_name_label.setVisible(false);
                        signin_password.setVisible(false);
                        signup_user_name_label.setVisible(false);
                        signup_password.setVisible(false);
                        info.setVisible(false);

                        frame.remove(signin_to_server);
                        frame.remove(signup_to_server);
                        frame.remove(signin_user_name_label);
                        frame.remove(signin_password);
                        frame.remove(signup_user_name_label);
                        frame.remove(signup_password);
                        frame.remove(info);
                        game_screen();
                    }
                }
            }
        });

        signup_to_server.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String username = signup_user_name_label.getText();
                char[] ch_password = signup_password.getPassword();
                boolean ok = check_username_password(username, ch_password);

                if (ok) {
                    String message = "signup " + saved_username + " " + saved_password;

                    out.println(message);
                    try {
                        String from_server = in.readLine();
                        decorder(from_server);
                        System.out.println(from_server);
                    } catch (IOException ex) {
                        throw new RuntimeException(ex);
                    }
                }
            }
        });
        frame.add(signin_to_server);
        frame.add(signup_to_server);
        frame.add(signin_user_name_label);
        frame.add(signin_password);
        frame.add(signup_user_name_label);
        frame.add(signup_password);
    }

    private void key_pressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ENTER) {
            submit.doClick();
        }
    }

    private void game_screen() {
        level = game_args[5];
        score = game_args[2];
        hi_sco = game_args[3];
        count = Integer.parseInt(game_args[4]);
        progress = game_args[1];

        submit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (!(letters.getText().equals("Letters"))) {
                    String letters_formatted = (letters.getText()).replace(" ", "");

                    for (int x = 0; x < letters_formatted.length(); x++) {
                        char ch = letters_formatted.charAt(x);
                        tracker += " '" + ch + "'";
                    }

                    out.println("submit " + letters_formatted);
                    try {
                        String from_server = in.readLine();
                        System.out.println(from_server);
                        game_args = from_server.split(" ");
                        after_submitting();
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            }
        });

        level_label.setVisible(true);
        score_label.setVisible(true);
        tracker_label.setVisible(true);
        hi_sco_button.setVisible(true);
        pic.setVisible(true);
        hi_sco_label.setVisible(true);
        change_level.setVisible(true);
        submit.setVisible(true);
        letters.setVisible(true);
        new_game.setVisible(true);
        
        new_game.add

        change_level.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String desired_level = JOptionPane.showInputDialog(frame,"Enter your desired level. Max level is 11 and minimum is 1");
                out.println("level " + desired_level);
                try {
                    String from_server = in.readLine();
                    String[] args = from_server.split(" ");
                    JOptionPane.showMessageDialog(frame, "Level will be changed to " + args[1] + " after this word.");
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });
        update_display();
    }
    private void hide_all() {
        pic.setVisible(false);
        level_label.setVisible(false);
        score_label.setVisible(false);
        tracker_label.setVisible(false);
        hi_sco_button.setVisible(false);
    }

    private boolean checker(String str) {
        int len = str.length();
        for (int x = 0; x < len; x++) {
            char ch = str.charAt(x);

            if (ch == ':') {
                JOptionPane.showMessageDialog(frame, "':' is an invalid character in password and username");
                return false;
            }
        }
        return true;
    }

    private boolean check_username_password(String username, char[] password){
        String pass = new String(password);

        if ((username.equals("Username") || pass.equals("Password"))) {
            JOptionPane.showMessageDialog(frame, "Invalid username and/or password");
            return false;
        }

        if (!checker(pass)) {
            return false;
        }
        if (!checker(username)) {
            return false;
        }

        try {
            save_config();
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
        saved_username = username;
        saved_password = pass;
        return true;
    }

    private boolean load_config() throws IOException {
        File file = new File("src\\config");
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line = br.readLine();
        if ((line == null) || (check_ip_port(line) == false)) {
            JOptionPane.showMessageDialog(frame, "Corrupt save file");
            return false;
        }

        File us_file = new File("src\\user");
        BufferedReader us = new BufferedReader(new FileReader(us_file));
        String password_and_username = us.readLine();
        String[] user_info = password_and_username.split(":");
        
        if (user_info.length != 2) {
            JOptionPane.showMessageDialog(frame, "Corrupt save file");
            saved_username = "username";
            saved_password = "";
            return false;
        }

        saved_username = user_info[0];
        saved_password = user_info[1];

        return true;
    }

    private void save_config() throws IOException {
        File file = new File("src\\config");

        FileWriter wr = new FileWriter(file);
        wr.write(host_ip + ":" + port);
        wr.close();

        File userinfo = new File("src\\user");
        FileWriter us = new FileWriter(userinfo);
        us.write(saved_username + ":" + saved_password+":");
        us.close();
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
        // TODO main loop
    }

    private boolean server_connect_func() {
        boolean ok = true;

        try {
            client = new Socket(host_ip, port);
            out = new PrintWriter(client.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        } catch (SocketException e) {
            ok = false;
            JOptionPane.showMessageDialog(frame, "Connection Error. Check ip:port or if host is up.");
            return false;
        } catch (IOException e) {
            ok = false;
            JOptionPane.showMessageDialog(frame, "IOException");
            return false;
        }
        if (ok) {
            connect.setBounds(395,40,95,30);
        }
        return true;

//        String fromServer;
//        try {
//            fromServer = in.readLine();
//            if (fromServer.equals("ok")) {
//
//            } else {
//                JOptionPane.showMessageDialog(frame, "Server return not OK!");
//            }
//        }
//        catch (IOException error) {
//            JOptionPane.showMessageDialog(frame, error);
//        }
    }

    public static void main(String[] args) throws Exception {
        HangedMan Game = new HangedMan();
    }
}
