import styles from "./Dashboard.module.css";

import WelcomeWidget from "./widgets/WelcomeWidget";

function Dashboard() {
  return (
    <section className={styles.dashboard}>
      <WelcomeWidget username={"Abhishek"} />
    </section>
  );
}

export default Dashboard;
