# Evidências de aceitação — candidata à 1.0 (0.23.0, 07/10/2026)

Este registro diz o que está **provado**, o que **falta** e quais são os **limites declarados**. Ele não traz
saída de sessão real, endereços, nomes de produto, de cliente ou de pessoa: resume o que foi observado.
O roteiro que o orienta é o [`evals/runbook.md`](../evals/runbook.md). O plugin se chamava Workflows até a
versão 0.6.1; os registros antigos desta página, que citavam os nomes da época, foram substituídos por este.

## Escopo da homologação

Homologação para **uso supervisionado no Windows**: uma pessoa acompanha a sessão e responde às perguntas.
Não é homologada, e não se promete: a execução sem supervisão com teto de contexto garantido e escopo exato
das permissões (o plugin não instala hooks e não isola ferramentas; veja `docs/security.md`), qualquer
sistema fora do Windows e o uso do `authorize` como barreira (ele é consultivo).

## Verificação automatizada

- `python -m unittest discover -s tests -v`: **1401 testes em 27 módulos, nenhum falhando** (5 pulados por dependências ausentes no ambiente, como o Playwright; contagem da 0.23.0).
  Alguns módulos (`test_serve_ports`, `test_checks_integration`) levam vários minutos; rode por módulo.
- `python -m compileall -q scripts tests`: passou (não há verificador de tipos externo).
- `claude plugin validate .`: passou; `claude --plugin-dir . plugin details frontlights` carrega uma skill,
  sem agentes, hooks nem servidores MCP.
- Integração contínua no GitHub Actions: configurada para Windows, Python 3.11 e 3.14; localmente só o 3.14 foi rodado,
  então o resultado da integração contínua desta versão só existe depois da publicação.
- Os testes usam transporte e datas simulados e **não** homologam o RoadS real; os dados dele estão na seção própria.

## Matriz do roteiro (sessões reais de 25/09 a 05/10/2026, num projeto de produto real)

| Item | Situação | O que está provado | O que falta |
| --- | --- | --- | --- |
| 1. Carregamento, etapa 0, perguntas com opções, português | Parcial | `/frontlights` rodou em várias sessões, a primeira pergunta é a do roadmap, todas as perguntas tinham opções e o texto ao usuário saiu em português | `/help` nunca foi inspecionado; a skill única e oculta só foi vista pelo inventário nativo |
| 2. Leitura real, fonte indisponível, duplicada | Parcial | issues e roadmap lidos de verdade; fonte indisponível tratada sem bloquear; duplicadas fechadas com aprovação | a fonte de observações do RoadS ficou sem configurar nos projetos reais |
| 3. Entrevista, PRD, plano, publicação | Parcial | PRD aprovado numa revisão exata, planos com 4 e 7 issues publicados e relidos no GitHub | a recusa de uma publicação só foi vista em ensaio local, sem GitHub |
| 4. Tickets horizontais corrigidos | Parcial | ensaio local de 25/09: a proposta horizontal virou fatias verticais sem pergunta extra | não repetido numa sessão com GitHub |
| 5. Concorrência com worktrees | Comprovado, com ressalva | `schedule` devolveu a onda, duas issues rodaram em paralelo em worktrees distintas e a dependente esperou | a concorrência foi de subagentes da mesma sessão; sobreposição de arquivos não apareceu |
| 6. Red/green, revisão independente | Parcial | red real antes do green, suíte ampla, revisão do diff exato | a re-revisão depois de uma mudança falhou em duas sessões reais; o `review-gate` desta versão só foi exercitado em teste automatizado, não numa sessão real |
| 7. Renovação de contexto | Parcial | retomada por handoff com `resume` em sessão nova, mudança de escopo tratada | o teto de contexto **não** é imposto nem medido de forma confiável (veja os limites) |
| 8. Celular (Remote Control) | Parcial | respostas do usuário confirmando que o celular recebeu e respondeu, em testes de setembro | sem confirmação vigente nem prompt nativo de permissão respondido pelo celular |
| 9. Escritas não autorizadas | Parcial | o classificador do modo automático e as regras do GitHub barraram merge, push e fechamento de issues | sem simulação planejada; o `authorize` nunca foi chamado numa sessão real; o escopo exato não é imposto |
| 10. Reiniciar sem o plugin | Pendente | o plugin não depende do GuardianS nem o altera | conferir dados e histórico do projeto depois de reiniciar sem o plugin |
| 11. Modo aprendizado | Parcial | ligado e desligado, explicação antes de decidir, "Ficou claro?" com até 3 decisões, 3 abordagens mais "Explicar antes de decidir" | duas reexplicações em sequência e "Seguir a recomendação" nunca apareceram |
| 12. Família de issues e branches empilhadas | Parcial | aplicado à mão na 0.16.0: sub-issues lidas, `needs-decision` no grilling, worktrees das filhas saindo da branch do pai | PR de filha com a base do pai e o retarget depois do merge nunca foram exercitados; falta uma sessão real com esta versão |
| 13. Teste de navegador assistido | Parcial | aplicado à mão na 0.16.0: pergunta antes da janela, Chrome visível, ANTES e DEPOIS, cada caso 2 vezes, janela aberta 45 s, perfil restrito real movido e devolvido; o resultado real passou | os auxiliares `serve` e `checks` não foram usados; a pergunta de fechamento da 0.19.0 ("Assistir de novo", "Aprovado", "Precisa de alteração", "Pode prosseguir") só tem prova textual e falta uma sessão real com esta versão |
| 14. Fechamento de issues e cartões em Done | Pendente | implementado e testado com `gh` simulado: só propõe issue aberta com todos os critérios marcados, filhas antes dos pais, aprovação própria da lista e releitura do GitHub | falta uma sessão real em que uma pessoa mescle uma família e responda à pergunta |
| 15. Conclusões registradas nos `.md` | Pendente | implementado e testado com transporte simulado: só o `done` do estado conta, mesma aprovação, marca e verificação, sem `ack` para o que não está na fila do RoadS | falta uma sessão real: Done no quadro, Sincronizar no RoadS e a sincronização aprovada no Frontlights |
| 16. Pendências como critério de aceitação | Pendente | regra escrita na skill, nos modelos e nos docs, e testada: o `closeout.py` conta a pendência como critério (a issue com ela aberta sai da lista) e avisa sobre a seção legada "Pendências conhecidas" fora dos critérios, com `gh` simulado | falta uma sessão real em que o portão liste os achados, o texto exato do critério seja aprovado antes da escrita e o corpo no GitHub mude só pelas linhas acrescentadas; o portão é regra da skill, não barreira |
| 17. Espera do merge, marcação no pai e limpeza | Pendente | implementado e testado com `gh` simulado e repositórios Git reais em pasta temporária: `merge-status` só aceita merge na base aprovada, `parentTicks` e `tick-check` conferem que só `[ ]` virou `[x]`, e `cleanup.py` só propõe o que tem o tip igual à cabeça de uma PR mesclada que chegou à base, sem alteração pendente, sem PR aberta e fora da pasta da sessão, nomeia os arquivos ignorados e só oferece a worktree de integração sem commit próprio | falta uma sessão real em que uma pessoa faça o merge de uma família empilhada; o gatilho (inscrição na PR ou monitor) depende do ambiente e a espera é regra da skill, não barreira |
| 18. Pergunta do resumo em qualquer projeto e início por linguagem natural | Pendente | implementado e testado com projetos temporários e um RoadS simulado: o bloco do próprio projeto vale primeiro, o registro assinado do usuário vale sem bloco, um registro copiado, editado ou sem assinatura vira `invalid`, as operações seguintes rodam na raiz do registro; o modelo de comando lista os gatilhos em português e o hook opcional foi testado como script | falta uma sessão real: a pergunta em dois projetos sem o bloco, o hook sendo executado pelo Claude Code a cada prompt e a frase comum abrindo o estágio 1 |
| 19. Teste assistido por lote, antes da revisão | Pendente | implementado e testado com repositórios Git reais em pasta temporária: `browser-gate` acha a mudança visível no diff, uma decisão cobre o lote inteiro, teste, documento e fatia sem mudança visível não reabrem a pergunta, código que muda a tela a torna `stale`, e a pendência `teste_assistido` atravessa `checkpoint`, `resume` e `context` | falta uma sessão real com uma família de duas fatias de tela e uma só de API; o `browser-gate` é regra da skill conferida por script, não barreira |

## RoadS em produção

- A fila de mudanças foi confirmada (`ack`) em produção em cinco dias distintos entre 28/09 e 05/10, sem
  pendências restantes; o `gaps` completou issues reais; e um rascunho do resumo com prints chegou ao RoadS
  em 05/10 já no contrato novo. O RoadS não registra quem chamou cada rota, então que foi o plugin é provável,
  não provado: por isso o plugin manda um User-Agent com a versão e o RoadS passa a registrá-lo.
- Os caminhos de erro (tempo esgotado do `sync-board`, credencial trocada, `schemaVersion` desconhecido,
  marcas recusadas) só têm cobertura simulada.
- O contrato agora está escrito em [`docs/roads-contract.md`](roads-contract.md), com versão, regra de
  mudança aditiva e regra de quebra.

## Defeitos achados no uso real e corrigidos nesta versão

- O `inspect` falhava num projeto cujo `browserTest` só declara as contas: agora avisa e segue.
- O `validate-plan` não explicava o status inválido nem o padrão de caminho em `ownership`, e não modelava
  uma sub-issue de uma issue publicada fora do plano: ganhou mensagens claras e `parent_external`.
- Nada obrigava a re-revisão depois de uma correção: o `review-gate` compara a evidência da revisão com a
  atual e sai com código 2 quando ela envelheceu.
- Faltava uma etapa de integração local de uma família antes dos PRs, e a regra para um desfazer que o
  endpoint do produto não devolve idêntico.
- Segredos de teste impressos no chat e números publicados sem o predicado que os gerou: viraram regra.
- A pasta dos prints do resumo caía na semana errada para uma janela que começa no fim de semana, e dois
  resumos da mesma semana dividiam o `captions.json`: a pasta segue o último dia do período, com uma subpasta
  por resumo.
- O plugin só conferia `schemaVersion` em uma rota do RoadS.
- Um item concluído que fica na sprint não aparecia como concluído nos `.md` até a rotação semanal: agora o plugin
  o registra, com a data da sincronização, na mesma aprovação do diff.
- Depois de uma atuação completa, o plugin não perguntava se podia fechar as issues e sub-issues com todos
  os critérios marcados e mover os cartões para Done: nova etapa 7, com aprovação própria da lista.

## Limites declarados (não são pendências desta versão)

- **Execução sem supervisão:** sem hook, o teto de contexto de 150 mil tokens não é imposto nem medido de
  forma confiável, e a maior parte das sessões reais passou dele. A renovação por handoff existe, mas é
  pedida pela pessoa ou pelo uso, não por uma medição.
- **Permissões:** o plugin orienta e confere predicados; quem barra é o Claude Code. Em modo `bypassPermissions`
  não há parada nativa; o `authorize` nunca devolve `permission_granted: true`.
- **Plataforma:** só o Windows é suportado e testado.
- **Celular:** o plugin não detecta o celular nem o host do Remote Control; `phone_connected: true` vale só pela afirmação do usuário na sessão.

## Para a 1.0

A 1.0 sai depois de **uma sessão real com a 0.19.0** que cumpra os itens 12 e 13 do roteiro (família empilhada
com os PRs das filhas na base do pai e o retarget depois do merge; teste assistido com `serve` e `checks`) e
exercite o fechamento de issues (item 14) e o registro de conclusões nos `.md` (item 15), que só foram testados com
GitHub e RoadS simulados, e de a pessoa responsável aceitar este registro. Os itens parciais acima ficam como limites ou como issues de
acompanhamento, nunca como "passou".
