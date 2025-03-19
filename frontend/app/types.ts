type TimeRangeFetchDataParams = {
  data_inicial: Date;
  data_final: Date;
  limite: number;
  deslocamento: number;
};

type MarginalCostData = {
  total_registros: number;
  data_inicial: string;
  data_final: string;
  dados: {
    id_subsistema: string;
    subsistema_nome: string;
    data: string;
    custo_marginal_operacao_semanal: number;
    custo_marginal_operacao_semanal_carga_leve: number;
    custo_marginal_operacao_semanal_carga_media: number;
    custo_marginal_operacao_semanal_carga_pesada: number;
  }[];
}

type EnergyData = {
  total_registros: number;
  data_inicial: string;
  data_final: string;
  dados: {
    id_subsistema: string;
    subsistema_nome: string;
    data: string;
    hora: string;
    geracao_eolica: number;
    geracao_termica: number;
    geracao_solar: number;
    geracao_hidraulica: number;
    valor_carga: number;
    valor_intercambio: number;
  }[];
};
