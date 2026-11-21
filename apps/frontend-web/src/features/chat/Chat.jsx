import { useState } from "react";
import styles from "./Chat.module.css";

const possibleWelcomeTexts = [
  "Ready when you are.",
  "The possibilities are yours.",
  "Let's make things happen.",
  "Hey, good to have you back.",
  "Your world. Your direction.",
  "Everything connected. One step ahead.",
  "Your next idea starts here.",
  "A smarter way to move forward.",
  "What's on your mind today?",
  "Your digital world, within reach.",
  "Big ideas. Seamless execution.",
  "Let's turn plans into progress.",
  "One intelligence. Infinite possibilities.",
  "Your workspace is ready for what's next.",
];

function Chat() {
  const [welcomeText] = useState(
    () =>
      possibleWelcomeTexts[
        Math.floor(Math.random() * possibleWelcomeTexts.length)
      ],
  );

  const [message, setMessage] = useState("");

  return (
    <section className={styles.chatSection}>
      <div className={styles.welcome}>
        <span className={styles.eyebrow}>NOVA · CHAT</span>
        <h1 className={styles.title}>{welcomeText}</h1>
        <p className={styles.description}>Your digital workspace.</p>
      </div>

      <div className={styles.composer}>
        <input
          type="text"
          className={styles.messageInput}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Message NOVA..."
          aria-label="Message NOVA"
        />
      </div>
    </section>
  );
}

export default Chat;
