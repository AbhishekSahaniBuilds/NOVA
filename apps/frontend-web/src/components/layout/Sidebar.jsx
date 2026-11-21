import {
  LayoutDashboard,
  MessageSquare,
  Settings,
  SlidersHorizontal,
  UserRound,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import novaIcon from "../../../../../packages/brand-assets/icons/web/generated/32x32.png";
import styles from "./Sidebar.module.css";

const navigation = [
  { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { label: "Chat", path: "/chat", icon: MessageSquare },
  { label: "Control", path: "/control", icon: SlidersHorizontal },
];

function Sidebar({ collapsed }) {
  const getLinkClass = (isActive, extraClass = "") =>
    [styles.navLink, extraClass, isActive ? styles.active : ""]
      .filter(Boolean)
      .join(" ");

  return (
    <aside
      className={[styles.sidebar, collapsed ? styles.collapsed : ""]
        .filter(Boolean)
        .join(" ")}
      aria-label="Main sidebar"
    >
      <div className={styles.brandHeader}>
        <div className={styles.brand}>
          <img className={styles.logo} src={novaIcon} alt="NOVA" />
          <span className={styles.brandName}>NOVA</span>
        </div>
      </div>

      <div className={styles.content}>
        <section className={styles.section}>
          <span className={styles.sectionLabel}>WORKSPACE</span>

          <nav className={styles.navigation} aria-label="Workspace navigation">
            {navigation.map(({ label, path, icon: Icon }) => (
              <NavLink
                key={path}
                to={path}
                end={path === "/dashboard"}
                title={collapsed ? label : undefined}
                className={({ isActive }) => getLinkClass(isActive)}
              >
                <Icon size={19} strokeWidth={1.8} />
                <span className={styles.navLabel}>{label}</span>
              </NavLink>
            ))}
          </nav>
        </section>
      </div>

      <footer className={styles.footer}>
        <NavLink
          to="/settings"
          title={collapsed ? "Settings" : undefined}
          className={({ isActive }) =>
            getLinkClass(isActive, styles.settingsLink)
          }
        >
          <Settings size={19} strokeWidth={1.8} />
          <span className={styles.navLabel}>Settings</span>
        </NavLink>

        <div className={styles.divider} />

        <div className={styles.profile}>
          <div className={styles.avatar}>
            <UserRound size={19} strokeWidth={1.8} />
          </div>

          <div className={styles.profileInfo}>
            <span className={styles.profileName}>Abhishek</span>
            <span className={styles.profileDescription}>
              Personal workspace
            </span>
          </div>
        </div>
      </footer>
    </aside>
  );
}

export default Sidebar;
