import { Link } from "react-router";
import { ArrowRight } from "lucide-react";
import { Button } from "~/components/ui/button";

export function HomePage() {
  return (
    <main className="flex flex-col items-center min-h-screen p-6 gap-6">
      <img src='icone-dashboard.png' width={240} alt="Ícone de dashboard" />
      <h1 className="scroll-m-20 text-2xl text-center font-bold tracking-tight lg:text-3xl">
        Dashboards Sistema Interligado Nacional (SIN)
      </h1>
      <p className="text-lg">
        Bem vindo aos dashboards do SIN, uma Prova de Conceito (POC) dos dados disponibilizados pelo Operador Nacional do Sistema Elétrico (ONS) sobre. Você pode encontrar detalhes do balanço de energia com diferentes matrizes para cada subsistema e também detalhes sobre o custo marginal de operação (CMO) nesses subsistemas ao longo do tempo.
      </p>
      <p className="text-lg">
        Os dados do balanço de energia estão divididos em medições realizadas a cada hora e outras medições realizadas a cada meia hora, segundo o Modelo de Despacho Hidrotérmico de Curtíssimo Prazo, novo de cálculo implementado em 2020 que realiza medições a cada meia hora. Os dados do CMO estão divididos em agregados calculados semanalmente e medidas calculadas a cada meia hora
      </p>
    </main>
  )
}


