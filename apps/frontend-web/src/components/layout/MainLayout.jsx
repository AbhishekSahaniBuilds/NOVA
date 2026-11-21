import { useState } from "react";
import { Outlet } from "react-router-dom";

import Header from "./Header";
import styles from "./MainLayout.module.css";
import Sidebar from "./Sidebar";

function MainLayout() {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => {
    setCollapsed((previous) => !previous);
  };

  return (
    <div className={styles.appLayout}>
      <Sidebar collapsed={collapsed} />

      <div className={styles.mainArea}>
        <Header collapsed={collapsed} onToggleSidebar={toggleSidebar} />

        <main className={styles.mainContent}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default MainLayout;
