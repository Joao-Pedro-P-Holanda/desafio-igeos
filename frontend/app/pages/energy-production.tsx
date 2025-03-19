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
  type ChartConfig,
} from "~/components/ui/chart"
import { Input } from "~/components/ui/input";
import { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "~/components/ui/pagination";
import { useEnergyData } from "~/hooks/use-energy-data";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "~/components/ui/form";
import { useForm } from "react-hook-form";
import { Button } from "~/components/ui/button";
import { CircularProgress } from "~/components/circular-progress";
import groupBy from "lodash/groupBy";
import meanBy from "lodash/meanBy";

const schema = z.object({
  data_inicial: z.date(),
  data_final: z.date(),
  limite: z.coerce.number().min(100)
});

const processChartData = (data: EnergyData | null) => {
  if (!data) return [];

  const groupedData = groupBy(data.dados, (item: { data: Date; }) => format(item.data, "yyyy-MM"));

  return Object.entries(groupedData).map(([month, records]) => ({
    month,
    geracao_eolica: meanBy(records, "geracao_eolica"),
    geracao_termica: meanBy(records, "geracao_termica"),
    geracao_solar: meanBy(records, "geracao_solar"),
    geracao_hidraulica: meanBy(records, "geracao_hidraulica"),
  }));
};



const barConfig = {
  geracao_eolica: { label: "Geração Eólica", color: "#8884d8" },
  geracao_termica: { label: "Geração Térmica", color: "#82ca9d" },
  geracao_solar: { label: "Geração Solar", color: "#ffc658" },
  geracao_hidraulica: { label: "Geração Hidráulica", color: "#a4de6c" },
} satisfies ChartConfig;

export function EnergyProductionPage() {
  const { data, loading, currentOffset, currentLimit, setCurrentOffset, initialSubmit, fetchData } = useEnergyData();

  const form = useForm({
    resolver: zodResolver(schema), defaultValues: {
      data_inicial: new Date(new Date().getFullYear(), 0, 1),
      data_final: new Date(),
      limite: 1000,
    }
  })

  const handleSubmit = async (values: z.infer<typeof schema>) => {
    const params = { "deslocamento": currentOffset, ...values }
    await fetchData(params);
  };

  useEffect(() => {
    (async () => {
      await handleSubmit(form.getValues()); // Realizando o submit inicial
    })();
  }, [initialSubmit, currentOffset, form.getValues]);

  return (
    <main className="flex flex-col items-center min-h-screen p-4 gap-6">
      <h1 className="scroll-m-20 text-2xl text-center font-bold tracking-tight lg:text-3xl">
        Dashboards do Balanço geral de energia
      </h1>
      <div className="flex flex-col items-start gap-3">
        <p>
          Nesta página você pode filtrar por uma data específica para visualizar os gráficos do balanço de energia medido de hora em hora agrupados por cada matriz energética
        </p>
        <p>
          Os dados medidos de hora em hora estão presentes desde 01/01/2000 até 13/03/2025.
        </p>
        <p>
          Os dados medidas de meia em meia hora, por sua vez estão presentes de  15/08/2023 até 03/03/2024.
        </p>
      </div>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="flex flex-col md:flex-row gap-4 items-center mb-4">
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


      {loading ? <CircularProgress /> :
        data ?
          <div>
            <ChartContainer config={barConfig} className="w-full h-[400px]">
              <BarChart width={800} height={400} data={processChartData(data)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" label={{ value: "Mês", position: "insideBottom", dy: 10 }} />
                <YAxis label={{
                  value: "Produção média (MegaWatt Médio)", angle: -90, position: "insideCenter", dx: -30,
                }} />
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent indicator="dashed" />}
                />
                <Legend />
                <Bar dataKey="geracao_eolica" name="Geração Eólica" fill="#8884d8" />
                <Bar dataKey="geracao_termica" name="Geração Térmica" fill="#82ca9d" />
                <Bar dataKey="geracao_solar" name="Geração Solar" fill="#ffc658" />
                <Bar dataKey="geracao_hidraulica" name="Geração Hidráulica" fill="#a4de6c" />              </BarChart>
            </ChartContainer>

            <Pagination className="mt-4">
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious href="#" onClick={() => setCurrentOffset((prev) => Math.max(0, prev - currentLimit))} />
                </PaginationItem>
                <PaginationItem>
                  <PaginationLink href="#">{(currentOffset / currentLimit) + 1}</PaginationLink>
                </PaginationItem>
                <PaginationItem>
                  <PaginationNext href="#" onClick={() => { if (currentOffset + currentLimit < data["total_registros"]) { setCurrentOffset((prev) => prev + currentLimit) } }} />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </div>
          : <p>
            Nenhum registro encontrado
          </p>
      }
    </main>
  )
}
