import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import favicon16 from "../../../packages/brand-assets/icons/web/generated/16x16.png";
import favicon32 from "../../../packages/brand-assets/icons/web/generated/32x32.png";
import appleTouchIcon from "../../../packages/brand-assets/icons/web/generated/apple-touch-icon.png";

import "../../../packages/brand-assets/styles/fonts.css";
import App from "./app/App.jsx";
import "./styles/index.css";

const icons = [
  {
    rel: "icon",
    type: "image/png",
    sizes: "32x32",
    href: favicon32,
  },
  {
    rel: "icon",
    type: "image/png",
    sizes: "16x16",
    href: favicon16,
  },
  {
    rel: "apple-touch-icon",
    type: "image/png",
    sizes: "180x180",
    href: appleTouchIcon,
  },
];

icons.forEach(({ rel, type, sizes, href }) => {
  const link = document.createElement("link");

  link.rel = rel;
  if (type) link.type = type;
  if (sizes) link.sizes = sizes;
  link.href = href;

  document.head.appendChild(link);
});

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
