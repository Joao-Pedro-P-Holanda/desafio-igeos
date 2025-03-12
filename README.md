# Desafio Igeos 

Projeto para o desafio da Igeos, com backend feito em FastAPI e integrado ao Google BigQuery, e frontend com React e Material UI.

## Objetivo

Fornecer uma forma simplificada de acessar dados das Estimativas de custos da operação do Sistema Interligado Nacional (SIN), com diferentes opções de agrupamento pelos usuários da API

## Decisões

- **Endpoints em português:** pelo fato da API conter dados referentes a um contexto específico de uma empresa nacional, optei por descrever os endpoints da aplicação em português, para seguir o padrão de outras APIs constantemente utilizadas para a ciência de dados, como a do IBGE e também facilitar a consulta e reduzir a necessidade de memorização por engenheiros de dados interessados.
- **Material UI em vez de Tailwind CSS:** o Material UI é uma biblioteca mais robusta, com componentes seguindo padrões de acessibilidade e pré-estilizados. Considerei mais fácil de aplicar para essa aplicação do que utilizar o Tailwind, principalmente pela existência de uma extensão da biblioteca para gerar gráficos.


