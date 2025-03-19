import type { Route } from "./+types/home";
import { withAuthenticationRequired } from "@auth0/auth0-react";
import { MarginalCostPage } from "~/pages/marginal-costs";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Custos de Energia" },
    { name: "description", content: "Página inicial dos dashboard SIN" },
  ];
}

function EnergyCosts() {
  return <MarginalCostPage />;
}

export default withAuthenticationRequired(EnergyCosts)
