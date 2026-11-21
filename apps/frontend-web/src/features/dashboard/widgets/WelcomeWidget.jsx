import styles from "./WelcomeWidget.module.css";

function WelcomeWidget({ username }) {
  return (
    <section className={styles.welcome} aria-labelledby="welcome-title">
      <div className={styles.content}>
        <span className={styles.eyebrow}>YOUR WORKSPACE</span>

        <h1 className={styles.welcomeText} id="welcome-title">
          Welcome back, <span>{username}.</span>
        </h1>

        <p className={styles.description}>
          Your workspace is ready. What would you like to work on today?
        </p>
      </div>

      <div className={styles.accent} aria-hidden="true" />
    </section>
  );
}

export default WelcomeWidget;
