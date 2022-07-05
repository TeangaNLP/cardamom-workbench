import { createRoot } from "react-dom/client";
import Router from './routes/Router';
const rootElement = document.getElementById("root");

const root = createRoot(rootElement);
root.render(<Router />,);
