import type { Route } from "./+types/home";
import { withAuthenticationRequired } from "@auth0/auth0-react";
import { EnergyProductionPage } from "~/pages/energy-production";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Balanço de Energia" },
    { name: "description", content: "Informações sobre o balanço de energia nos subsistemas nos diferentes modais energéticos" },
  ];
}


function EnergyProduction() {
  return <EnergyProductionPage />;
}

export default withAuthenticationRequired(EnergyProduction)
