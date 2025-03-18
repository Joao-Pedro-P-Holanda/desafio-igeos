import type { Route } from "./+types/home";
import { HomePage } from "~/pages/home";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Dashboards Sin" },
    { name: "description", content: "Página inicial dos dashboard SIN" },
  ];
}

export default function Home() {
  return <HomePage />;
}
