"use client";

import { z } from "zod";
import { zodResolver } from '@hookform/resolvers/zod';
import { Bar, BarChart, CartesianGrid, Legend, XAxis, YAxis } from "recharts"
import { useEffect } from "react";
import { format } from "date-fns";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "~/components/ui/chart"
import type { ChartConfig } from "~/components/ui/chart";
import { Input } from "~/components/ui/input";
import { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "~/components/ui/pagination";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "~/components/ui/form";
import { useForm } from "react-hook-form";
import { Button } from "~/components/ui/button";
import { useCostData } from "~/hooks/use-cost-data";
import { CircularProgress } from "~/components/circular-progress";
import groupBy from "lodash/groupBy";
import meanBy from "lodash/meanBy";


const schema = z.object({
  data_inicial: z.date(),
  data_final: z.date(),
  limite: z.coerce.number().min(100)
});

const chartConfig = {
  custo_marginal_operacao_semanal: {
    label: "Custo Total",
    color: "#8884d8",
  },
  custo_marginal_operacao_semanal_carga_leve: {
    label: "Carga Leve",
    color: "#82ca9d",
  },
  custo_marginal_operacao_semanal_carga_media: {
    label: "Carga Média",
    color: "#ffc658",
  },
  custo_marginal_operacao_semanal_carga_pesada: {
    label: "Carga Pesada",
    color: "#a4de6c",
  },
} satisfies ChartConfig;

const processChartData = (data: MarginalCostData | null) => {
  if (!data) return [];

  const groupedData = groupBy(data.dados, (item: { data: Date; }) => format(item.data, "yyyy-MM"));

  return Object.entries(groupedData).map(([month, records]) => ({
    month,
    custo_marginal_operacao_semanal: meanBy(records, "custo_marginal_operacao_semanal"),
    custo_marginal_operacao_semanal_carga_leve: meanBy(records, "custo_marginal_operacao_semanal_carga_leve"),
    custo_marginal_operacao_semanal_carga_media: meanBy(records, "custo_marginal_operacao_semanal_carga_media"),
    custo_marginal_operacao_semanal_carga_pesada: meanBy(records, "custo_marginal_operacao_semanal_carga_pesada"),
  }));
};

export function MarginalCostPage() {
  const weeklyCosts = useCostData("weekly");

  const halfHourlyCosts = useCostData("half-hourly");


  const form = useForm({
    resolver: zodResolver(schema), defaultValues: {
      data_inicial: new Date(2024, 0, 1),
      data_final: new Date(2024, 2, 8),
      limite: 1000,
    }
  })

  const handleSubmitWeekly = async (values: z.infer<typeof schema>) => {
    const params = { "deslocamento": weeklyCosts.currentOffset, ...values }
    await weeklyCosts.fetchData(params);
  };

  const handleSubmitHalfHourly = async (values: z.infer<typeof schema>) => {
    const params = { "deslocamento": halfHourlyCosts.currentOffset, ...values }
    await halfHourlyCosts.fetchData(params);
  };

  useEffect(() => {
    (async () => {
      await handleSubmitWeekly(form.getValues()); // Realizando o submit inicial
      await handleSubmitHalfHourly(form.getValues());
    })();
  }, [weeklyCosts.initialSubmit, halfHourlyCosts.initialSubmit, form.getValues]);

  return (
    <main className="flex flex-col items-center min-h-screen p-4 gap-4">
      <h1 className="scroll-m-20 text-2xl text-center font-bold tracking-tight lg:text-3xl">
        Dashboards do Custo Marginal de Operação (CMO)
      </h1>
      <div className="flex flex-col items-start gap-3">
        <p>
          Nesta página você pode filtrar por uma data específica para visualizar os gráficos do CMO medido de hora em hora e também no formato de meia em meia hora.
        </p>
        <p>
          Os dados medidos semanalmente estão presentes de 07/01/2005 até 08/03/2024.
        </p>
        <p>
          Os dados medidas de meia em meia hora, por sua vez estão presentes de 01/01/2020 até 03/03/2024.
        </p>
      </div>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(handleSubmitWeekly)} className="flex flex-col md:flex-row gap-4 items-center mb-4">
          <FormField
            control={form.control}
            name="data_inicial"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Data Inicial</FormLabel>
                <FormControl>
                  <Input
                    type="date"
                    value={field.value ? format(field.value, "yyyy-MM-dd") : ""}
                    onChange={(e) => field.onChange(new Date(e.target.value))}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="data_final"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Data Inicial</FormLabel>
                <FormControl>
                  <Input
                    type="date"
                    value={field.value ? format(field.value, "yyyy-MM-dd") : ""}
                    onChange={(e) => field.onChange(new Date(e.target.value))}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="limite"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Máximo de resultados</FormLabel>
                <FormControl>
                  <Input type="number" {...field} className="w-24" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" variant='outline' className="mt-4">Buscar</Button>
        </form>
      </Form>
      {weeklyCosts.loading ? <CircularProgress /> :
        weeklyCosts.data ?
          <div>
            <ChartContainer config={chartConfig} className="w-full h-[400px]">
              <BarChart width={900} height={400} data={processChartData(weeklyCosts.data)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" label={{ value: "Mês", position: "insideBottom", dy: 10 }} />
                <YAxis
                  label={{
                    value: "Valor médio do CMO", angle: -90, position: "insideCenter", dx: -30,
                  }}
                  tickFormatter={(value, _) => value.toExponential(2)}
                />
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent indicator="dashed" />}
                />
                <Legend />
                <Bar dataKey="custo_marginal_operacao_semanal" name="Custo Total" fill="#8884d8" />
                <Bar dataKey="custo_marginal_operacao_semanal_carga_leve" name="Carga Leve" fill="#82ca9d" />
                <Bar dataKey="custo_marginal_operacao_semanal_carga_media" name="Carga Média" fill="#ffc658" />
                <Bar dataKey="custo_marginal_operacao_semanal_carga_pesada" name="Carga Pesada" fill="#a4de6c" />
              </BarChart>
            </ChartContainer>

            <Pagination className="mt-4">
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious href="#" onClick={() => weeklyCosts.setCurrentOffset((prev) => Math.max(0, prev - weeklyCosts.currentLimit))} />
                </PaginationItem>
                <PaginationItem>
                  <PaginationLink href="#">{Math.ceil(weeklyCosts.currentOffset / weeklyCosts.currentLimit) + 1}</PaginationLink>
                </PaginationItem>
                <PaginationItem>
                  <PaginationNext
                    isActive={(weeklyCosts.currentOffset + weeklyCosts.currentLimit) >= weeklyCosts.data["total_registros"]}
                    href="#"
                    onClick={() => { if (weeklyCosts.currentOffset + weeklyCosts.currentLimit < weeklyCosts.data["total_registros"]) weeklyCosts.setCurrentOffset((prev) => prev + weeklyCosts.currentLimit) }} />

                </PaginationItem>
              </PaginationContent>
            </Pagination>
            <br />
            {weeklyCosts.currentOffset}
            <br />
            {weeklyCosts.currentLimit}
          </div>
          : <p>
            Nenhum registro encontrado
          </p>

      }
    </main>
  )
}
