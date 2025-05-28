import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

public class LLMClient {
    private static Map<String, JButton> colorButtons = new HashMap<>();

    public static void main(String[] args) {
        try {
            startServers();  // Launch Ollama + MCP when the GUI starts
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Build the GUI
        JFrame frame = new JFrame("Interactive LLM Application");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 500);
        frame.setLocationRelativeTo(null);
        frame.setLayout(new BorderLayout());

        // Header section
        JPanel header = new JPanel();
        header.setBackground(new Color(76, 175, 80));
        JLabel headerLabel = new JLabel("Interact with the LLM", JLabel.CENTER);
        headerLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerLabel.setForeground(Color.WHITE);
        header.add(headerLabel);
        frame.add(header, BorderLayout.NORTH);

        // Main content container
        JPanel container = new JPanel();
        container.setLayout(new BoxLayout(container, BoxLayout.Y_AXIS));
        container.setBackground(Color.WHITE);

        // Color buttons
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 20, 20));
        JButton redButton = createColorButton("Red Button", Color.RED, Color.WHITE);
        JButton blueButton = createColorButton("Blue Button", Color.BLUE, Color.WHITE);
        JButton yellowButton = createColorButton("Yellow Button", Color.YELLOW, Color.BLACK);

        colorButtons.put("red_button", redButton);
        colorButtons.put("blue_button", blueButton);
        colorButtons.put("yellow_button", yellowButton);

        buttonPanel.add(redButton);
        buttonPanel.add(blueButton);
        buttonPanel.add(yellowButton);

        // Input field and submit button
        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        JTextField userPromptField = new JTextField(20);
        userPromptField.setFont(new Font("Arial", Font.PLAIN, 16));
        userPromptField.setBorder(BorderFactory.createLineBorder(new Color(200, 200, 200)));

        JButton submitButton = new JButton("Submit");
        submitButton.setFont(new Font("Arial", Font.BOLD, 16));
        submitButton.setBackground(new Color(100, 100, 100));
        submitButton.setForeground(Color.BLACK); // Nur dieser schwarz
        submitButton.setFocusPainted(false);

        inputPanel.add(userPromptField);
        inputPanel.add(submitButton);

        // Response message display
        JPanel confirmationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        JLabel confirmationLabel = new JLabel("Pick a color!");
        confirmationLabel.setFont(new Font("Arial", Font.ITALIC, 14));
        confirmationLabel.setForeground(new Color(100, 100, 100));
        confirmationPanel.add(confirmationLabel);

        submitButton.addActionListener(e -> {
            String prompt = userPromptField.getText().trim();
            if (prompt.isEmpty()) {
                JOptionPane.showMessageDialog(frame, "Please enter a prompt.", "Error", JOptionPane.ERROR_MESSAGE);
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

    // Launches Ollama backend, Flask LLM server, and MCP server
    private static void startServers() throws IOException {
        ProcessBuilder ollamaBackend = new ProcessBuilder("ollama", "serve");
        ollamaBackend.redirectErrorStream(true);
        ollamaBackend.start();
        System.out.println("🦙 Ollama backend started...");

        ProcessBuilder ollamaServer = new ProcessBuilder("python3", "ollama_qwen3_server.py");
        ollamaServer.redirectErrorStream(true);
        ollamaServer.start();
        System.out.println("🧠 Ollama Qwen server started...");

        ProcessBuilder mcp = new ProcessBuilder("python3", "mcp_server.py");
        mcp.redirectErrorStream(true);
        mcp.start();
        System.out.println("🧩 MCP server started...");

        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static JButton createColorButton(String text, Color bg, Color fg) {
        JButton button = new JButton(text);
        button.setBackground(bg);
        button.setForeground(fg);
        button.setFont(new Font("Arial", Font.BOLD, 14));
        button.setFocusPainted(false);
        button.setPreferredSize(new Dimension(150, 50));
        button.setOpaque(true);
        button.setBorderPainted(false);
        return button;
    }

    private static void sendRequestToServer(String prompt, JLabel label) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            String form = "user_prompt=" + URLEncoder.encode(prompt, "UTF-8") + "&context=" + URLEncoder.encode("", "UTF-8");

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("http://127.0.0.1:5006/mcp_request"))
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .POST(HttpRequest.BodyPublishers.ofString(form))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            String responseStr = response.body();

            // Reset all button colors and text colors
            colorButtons.get("red_button").setBackground(Color.RED);
            colorButtons.get("red_button").setForeground(Color.WHITE);

            colorButtons.get("blue_button").setBackground(Color.BLUE);
            colorButtons.get("blue_button").setForeground(Color.WHITE);

            colorButtons.get("yellow_button").setBackground(Color.YELLOW);
            colorButtons.get("yellow_button").setForeground(Color.BLACK);

            if (response.statusCode() != 200) {
                label.setText("Server error: " + response.statusCode() + " - " + responseStr);
                label.setForeground(Color.RED);
                return;
            }

            if (responseStr.contains("red_button")) {
                JButton btn = colorButtons.get("red_button");
                btn.setBackground(Color.GRAY);
                label.setText("LLM pressed the red button.");
                label.setForeground(new Color(76, 175, 80));
            } else if (responseStr.contains("blue_button")) {
                JButton btn = colorButtons.get("blue_button");
                btn.setBackground(Color.GRAY);
                label.setText("LLM pressed the blue button.");
                label.setForeground(new Color(76, 175, 80));
            } else if (responseStr.contains("yellow_button")) {
                JButton btn = colorButtons.get("yellow_button");
                btn.setBackground(Color.GRAY);
                label.setText("LLM pressed the yellow button.");
                label.setForeground(new Color(76, 175, 80));
            } else {
                label.setText("No recognized color in the response.");
                label.setForeground(Color.RED);
            }

        } catch (Exception e) {
            label.setText("Request error: " + e.getMessage());
            label.setForeground(Color.RED);
            e.printStackTrace();
        }
    }
}
