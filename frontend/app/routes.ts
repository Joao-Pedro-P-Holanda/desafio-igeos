import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("geracao-energia", "./routes/energy-production.tsx"),
  route("custos-energia", "./routes/marginal-costs.tsx")
] satisfies RouteConfig;
