import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

public class LLMClient {
    private static Map<String, JButton> colorButtons = new HashMap<>();

    public static void main(String[] args) {
        try {
            startServers();  // Startet Ollama + MCP beim Starten der GUI
        } catch (IOException e) {
            e.printStackTrace();
        }

        // GUI-Aufbau
        JFrame frame = new JFrame("Interaktive Anwendung mit LLM");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 500);
        frame.setLocationRelativeTo(null);
        frame.setLayout(new BorderLayout());

        // Header
        JPanel header = new JPanel();
        header.setBackground(new Color(76, 175, 80));
        JLabel headerLabel = new JLabel("Interagiere mit dem LLM", JLabel.CENTER);
        headerLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerLabel.setForeground(Color.WHITE);
        header.add(headerLabel);
        frame.add(header, BorderLayout.NORTH);

        // Container für Inhalt
        JPanel container = new JPanel();
        container.setLayout(new BoxLayout(container, BoxLayout.Y_AXIS));
        container.setBackground(Color.WHITE);

        // Farbbuttons
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 20, 20));
        JButton redButton = createColorButton("Roter Button", Color.RED);
        JButton blueButton = createColorButton("Blauer Button", Color.BLUE);
        JButton yellowButton = createColorButton("Gelber Button", Color.YELLOW);

        colorButtons.put("rot", redButton);
        colorButtons.put("blau", blueButton);
        colorButtons.put("gelb", yellowButton);

        buttonPanel.add(redButton);
        buttonPanel.add(blueButton);
        buttonPanel.add(yellowButton);

        // Eingabefeld + Button
        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        JTextField userPromptField = new JTextField(20);
        userPromptField.setFont(new Font("Arial", Font.PLAIN, 16));
        userPromptField.setBorder(BorderFactory.createLineBorder(new Color(200, 200, 200)));

        JButton submitButton = new JButton("Absenden");
        submitButton.setFont(new Font("Arial", Font.BOLD, 16));
        submitButton.setBackground(new Color(100, 100, 100));
        submitButton.setForeground(Color.WHITE);
        submitButton.setFocusPainted(false);

        inputPanel.add(userPromptField);
        inputPanel.add(submitButton);

        // Antwortmeldung
        JPanel confirmationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        JLabel confirmationLabel = new JLabel("Wähle eine Farbe aus!");
        confirmationLabel.setFont(new Font("Arial", Font.ITALIC, 14));
        confirmationLabel.setForeground(new Color(100, 100, 100));
        confirmationPanel.add(confirmationLabel);

        submitButton.addActionListener(e -> {
            String prompt = userPromptField.getText().trim();
            if (prompt.isEmpty()) {
                JOptionPane.showMessageDialog(frame, "Bitte gib einen Prompt ein.", "Fehler", JOptionPane.ERROR_MESSAGE);
                return;
            }
            sendRequestToServer(prompt, confirmationLabel);
        });

        container.add(buttonPanel);
        container.add(inputPanel);
        container.add(confirmationPanel);
        frame.add(container, BorderLayout.CENTER);

        frame.setVisible(true);
    }

    // Startet Ollama-LLM-Server und MCP
    private static void startServers() throws IOException {
        // Ollama/Qwen-Server starten
        ProcessBuilder ollamaServer = new ProcessBuilder("python3", "ollama_qwen3_server.py");
        ollamaServer.redirectErrorStream(true);
        Process ollamaProcess = ollamaServer.start();
        System.out.println("🧠 Ollama Qwen Server gestartet...");

        // MCP-Server starten
        ProcessBuilder mcp = new ProcessBuilder("python3", "mcp_server.py");
        mcp.redirectErrorStream(true);
        Process mcpProcess = mcp.start();
        System.out.println("🧩 MCP-Server gestartet...");

        // Kurzes Delay, damit die Server hochfahren
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static JButton createColorButton(String text, Color color) {
        JButton button = new JButton(text);
        button.setBackground(color);
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Arial", Font.BOLD, 14));
        button.setFocusPainted(false);
        button.setPreferredSize(new Dimension(150, 50));
        button.setOpaque(true);
        button.setBorderPainted(false);
        return button;
    }

    private static void sendRequestToServer(String prompt, JLabel label) {
        try {
            URL url = new URL("http://127.0.0.1:5006/mcp_request");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

            String data = "user_prompt=" + URLEncoder.encode(prompt, "UTF-8") + "&context=" + URLEncoder.encode("", "UTF-8");
            con.getOutputStream().write(data.getBytes());

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            StringBuilder responseBuilder = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) {
                responseBuilder.append(line);
            }
            in.close();

            String responseStr = responseBuilder.toString();
            System.out.println("Antwort vom Server: " + responseStr);

            if (responseStr.contains("rot")) {
                JButton btn = colorButtons.get("rot");
                btn.setBackground(Color.GRAY);
                label.setText("LLM hat den roten Button gedrückt.");
                label.setForeground(new Color(76, 175, 80));
            } else if (responseStr.contains("blau")) {
                JButton btn = colorButtons.get("blau");
                btn.setBackground(Color.GRAY);
                label.setText("LLM hat den blauen Button gedrückt.");
                label.setForeground(new Color(76, 175, 80));
            } else if (responseStr.contains("gelb")) {
                JButton btn = colorButtons.get("gelb");
                btn.setBackground(Color.GRAY);
                label.setText("LLM hat den gelben Button gedrückt.");
                label.setForeground(new Color(76, 175, 80));
            } else {
                label.setText("Keine erkannte Farbe.");
                label.setForeground(Color.RED);
            }

        } catch (Exception e) {
            label.setText("Fehler bei der Anfrage.");
            label.setForeground(Color.RED);
            e.printStackTrace();
        }
    }
}
