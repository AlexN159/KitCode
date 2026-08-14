import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Home from "../app/page";
import { migrateLegacyBrowserStorage } from "../app/storage-migration.mjs";
import "../app/globals.css";

const root = document.getElementById("root");

if (!root) {
  throw new Error("KitCode could not find its application root.");
}

migrateLegacyBrowserStorage(window.localStorage);

createRoot(root).render(
  <StrictMode>
    <Home />
  </StrictMode>,
);
