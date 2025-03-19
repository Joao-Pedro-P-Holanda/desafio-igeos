import { useAuth0 } from "@auth0/auth0-react";
import { useState } from "react";

export const useCostData = (frequency: "weekly" | "half-hourly") => {
  const { getAccessTokenSilently } = useAuth0();
  const [data, setData] = useState<MarginalCostData | null>()
  const [loading, setLoading] = useState(false)
  const [currentOffset, setCurrentOffset] = useState(0);
  // used only to present the pagination accordingly
  const [currentLimit, setCurrentLimit] = useState(0)

  const [initialSubmit, setInitialSubmit] = useState(false)

  const fetchData = async (values: TimeRangeFetchDataParams) => {
    const requestUrl = frequency === "weekly" ? "http://localhost:8000/cmo/semanal" : "http://localhost:8000/cmo/semihorario"
    try {
      setLoading(true)
      const params = new URLSearchParams({
        data_inicial: values.data_inicial.toISOString().split("T")[0],
        data_final: values.data_final.toISOString().split("T")[0],
        limite: values.limite.toString(),
        deslocamento: values.deslocamento.toString(),
      });

      const token = await getAccessTokenSilently({
        authorizationParams: { audience: "https://sin-dashboard/api" },
      });

      const response = await fetch(
        `${requestUrl}?${params}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.ok) {
        setData(await response.json());
      } else {
        console.error(`Request failed with status code ${response.status}`)
      }
      if (!initialSubmit) {
        setInitialSubmit(true)
      }
      setCurrentLimit(values.limite)
    } catch (e) {
      console.error(e);
    }
    finally {
      setLoading(false)
    }
  };

  return {
    data,
    loading,
    currentLimit,
    currentOffset,
    setCurrentOffset,
    initialSubmit,
    fetchData,
  };
};
