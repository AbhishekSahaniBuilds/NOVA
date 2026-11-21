import { createBrowserRouter } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

import Chat from "../features/chat/Chat";
import Dashboard from "../features/dashboard/Dashboard";

const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      {
        path: "/dashboard",
        element: <Dashboard />,
      },
      {
        path: "/chat",
        element: <Chat />,
      },
    ],
  },
]);

export default router;
