# Justificativa das métricas — Dashboard 2

Dataset: pedidos de um e-commerce de eletrônicos (`data/clean/dataset.csv`, 49.198 pedidos de jan/2024 a jun/2026).

**Público-alvo geral do painel:** gestão do e-commerce (área comercial e de operações), que acompanha o negócio mês a mês e não precisa conhecer as nuances estatísticas de cada variável.

**Como os KPIs são lidos:** cada cartão mostra o valor no período escolhido, a variação (delta) em relação ao período anterior de mesmo tamanho e um minigráfico com a mesma métrica mês a mês. No padrão (últimos 12 meses, jul/25–jun/26) a comparação é com jul/24–jun/25. Os números citados abaixo são desse recorte padrão.

## Métrica 1: Pedidos
- **Variável:** `OrderID` (contagem de pedidos)
- **O que mede:** a quantidade de pedidos feitos no período, nos segmentos e na categoria selecionados.
- **Por que foi escolhida:** é a métrica mais direta de demanda e serve de base para ler as outras: faturamento = pedidos × ticket médio. A EDA mostrou uma queda de volume a partir de fev/2026, e esse KPI deixa isso visível sem precisar abrir a série temporal.
- **Público-alvo:** gestão comercial e marketing.
- **Qual decisão pode ser apoiada por essa métrica?** Reforçar campanhas de aquisição ou de recompra quando o volume cai, e investigar a causa da queda (sazonalidade, problema no site, concorrência).
- **O que comunica ao público-alvo:** "vendemos mais ou menos pedidos do que antes?". Ex.: 18.075 pedidos nos últimos 12 meses, −13,4% em relação aos 12 meses anteriores.

## Métrica 2: Faturamento
- **Variável:** `Sales` (soma do valor dos pedidos)
- **O que mede:** o valor total vendido no período, contando também os pedidos que depois foram cancelados ou devolvidos (é o valor bruto de pedidos).
- **Por que foi escolhida:** é o resultado financeiro que a gestão acompanha. Junto do gráfico "Faturamento por categoria", mostra de onde vem o dinheiro (Electronics responde por cerca de metade).
- **Público-alvo:** diretoria e gestão comercial.
- **Qual decisão pode ser apoiada por essa métrica?** Definir metas e priorizar as categorias que mais faturam em estoque, mídia e promoções.
- **O que comunica ao público-alvo:** "quanto o e-commerce vendeu e se isso cresceu". Ex.: 1.266.501 em vendas nos últimos 12 meses, −13,1% em relação ao período anterior.

## Métrica 3: Ticket médio
- **Variável:** `Sales` (média por pedido)
- **O que mede:** o valor médio de cada pedido.
- **Por que foi escolhida:** separa as duas causas possíveis de uma variação no faturamento: menos pedidos ou pedidos mais baratos. Uso a média, e não a mediana, porque é ela que fecha a conta faturamento = pedidos × ticket médio. A EDA mostrou que a média (~70) fica acima da mediana (~38), puxada por poucos pedidos caros, e o gráfico "Pedidos por faixa de valor" mostra isso ao lado.
- **Público-alvo:** marketing e gestão comercial.
- **Qual decisão pode ser apoiada por essa métrica?** Criar ações para aumentar o valor do carrinho (kits, frete grátis acima de um valor, sugestões de acessórios) quando o ticket cai.
- **O que comunica ao público-alvo:** "cada cliente está gastando mais ou menos por compra?". Ex.: 70,1 por pedido, praticamente estável (+0,3%). Ou seja, a queda do faturamento veio do número de pedidos, não do valor de cada um.

## Métrica 4: Taxa de problema
- **Variável:** `desfecho` (derivada de `Status`: Cancelled ou Returned = "Problema")
- **O que mede:** a proporção de pedidos cancelados ou devolvidos.
- **Por que foi escolhida:** foi a classe de interesse da EDA. Cada problema é venda perdida e custo de operação (logística reversa, atendimento). A variação é mostrada em pontos percentuais (p.p.), que é mais fácil de entender do que "% de uma %", e o cartão usa cor invertida: subir aparece em vermelho.
- **Público-alvo:** operações, logística e atendimento.
- **Qual decisão pode ser apoiada por essa métrica?** Investigar processos (prazo de entrega, qualidade do produto, meio de pagamento) quando a taxa sobe. O gráfico "Taxa de problema por forma de pagamento" ajuda a ver se algum meio de pagamento está acima da média.
- **O que comunica ao público-alvo:** "de cada 100 pedidos, quantos deram problema?". Ex.: 8,4% nos últimos 12 meses, +0,7 p.p. em relação ao período anterior.

## Widgets e visuais de apoio

- **Período** (select_slider de meses, padrão últimos 12 meses) e **segmento de cliente** (pills New / Regular / VIP): recortam todos os KPIs e gráficos.
- **Faturamento por categoria** (barras, agrupa `Category`): clicar numa barra filtra os KPIs e os outros gráficos (seleção cruzada com `on_select` do Altair).
- **Pedidos por faixa de valor** (discretização de `Sales` em 5 faixas): versão simplificada da distribuição de `Sales`, sem exigir leitura de histograma.
- **Taxa de problema por forma de pagamento** (barras + linha da taxa geral): desdobra a métrica 4.
