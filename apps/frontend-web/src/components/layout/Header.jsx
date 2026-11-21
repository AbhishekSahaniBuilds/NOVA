import { PanelLeftClose, PanelLeftOpen } from "lucide-react";
import { useLocation } from "react-router-dom";

import styles from "./Header.module.css";

const pageTitles = {
  "/": "Dashboard",
  "/dashboard": "Dashboard",
  "/chat": "Chat",
  "/control": "Control",
  "/settings": "Settings",
};

function Header({ collapsed, onToggleSidebar }) {
  const { pathname } = useLocation();

  const normalizedPath =
    pathname.length > 1 ? pathname.replace(/\/+$/, "") : pathname;

  const title =
    pageTitles[normalizedPath] ||
    normalizedPath
      .split("/")
      .filter(Boolean)
      .at(-1)
      ?.replace(/-/g, " ")
      .replace(/\b\w/g, (character) => character.toUpperCase()) ||
    "Dashboard";

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <button
          type="button"
          className={styles.sidebarToggle}
          onClick={onToggleSidebar}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          aria-expanded={!collapsed}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? (
            <PanelLeftOpen size={19} strokeWidth={1.8} />
          ) : (
            <PanelLeftClose size={19} strokeWidth={1.8} />
          )}
        </button>

        <div className={styles.heading}>
          <span className={styles.eyebrow}>NOVA</span>
          <h1 className={styles.title}>{title}</h1>
        </div>
      </div>
    </header>
  );
}

export default Header;
