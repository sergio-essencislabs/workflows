# <One observable outcome>

PRD: <approved revision/link>

## Outcome

## Boundaries and non-goals

## Acceptance criteria

- [ ] <observable result>

Achado de revisão, de teste ao vivo ou de conferência que não for corrigido no PR entra
aqui como mais um critério (`- [ ] Pendência (achado da revisão): <resultado observável>.
Evidência que fecha: <teste, medição ou diff revisado>`), nunca numa seção à parte: só
esta seção conta para fechar a issue, e a issue só fecha com a pendência tratada,
concluída e marcada com evidência.

## Approach and conventions

Chosen approach (rejected alternatives in the PRD or discovery log) and the
project conventions to follow, with example paths. Any approved break of the
pattern is named here with its reason.

## Seams under test

- <public interface> — <acceptance behavior observed there>

Only these seams receive tests. A missing or wrong seam goes back to the user.

## Test expectations

Focused regression, broader integration and actual type-check commands.

## Camadas da fatia

A fatia é esta issue mais as sub-issues dela, e juntas cobrem todas as camadas que
o requisito pede. Liste as camadas lidas do código (no mínimo as seis abaixo, mais as
do projeto, como permissões, configuração, tradução, observabilidade, tarefas em
segundo plano). Uma camada que ninguém analisou é lacuna do plano, não "não tocada".
Uma sub-issue copia só as linhas que ela cobre.

A fatia só é definida depois da leitura de todas as camadas (front: componentes, serviços,
modelos, rotas e specs; back: controllers, services, contratos e DTOs, repositories,
mapeamentos e validadores; migrations e schema; testes; documentação), com certeza de que
não sobra ponta solta. "Não tocada" só vale com a evidência do rastreio abaixo; motivo sem
evidência não é aceito, e linha sem evidência impede aprovar o plano.

| Camada | Situação | Onde ou motivo | Evidência |
| --- | --- | --- | --- |
| Tela | tratada / não tocada | esta issue, #<filha>, ou o motivo | arquivo:linha, coluna, consumidor ou teste |
| API | | | |
| Banco e migração | | | |
| Testes | | | |
| Integração | | | |
| Documentação | | | |

Rastreio dos campos, botões e ações que a fatia toca na tela, feito por busca no código:

| Campo ou ação | Consumidor no back (arquivo:linha) | Coluna no banco | Teste |
| --- | --- | --- | --- |
| <campo> | | | |

Campo sem consumidor no back, ou capacidade do back sem ação na tela, é achado: vira
critério de aceitação desta issue ou sub-issue, nunca "não tocada". Rastreio inconclusivo
(consumo dinâmico, reflexão, nome de coluna montado em texto) vira a tarefa "provar o
consumo por teste ou por leitura da execução" e bloqueia a aprovação do plano até ser
resolvida com evidência; nunca fica só como nota.

## Navegador e testes ligados

- Toca o frontend: <sim | não>
- Conta: <conta 1 | contas 1 e 2>
- Fluxo: <telas e ações a exercitar, com o resultado esperado e o efeito no back e no banco depois de salvar; se mover um usuário de teste de perfil pelo endpoint do produto, diga qual e que será desfeito>
- Testes ligados: <navegador, integração, regressão, permissões entre contas, smoke>; casos extras: <nenhum>

Contas e processos vêm de `browserTest` no `.frontlights/config.json` do projeto,
nunca deste texto: aqui não entram login, senha nem URL.

`Toca o frontend:` é uma declaração, e o `browser-gate` a confere com o diff: uma mudança visível
com `não` vira pergunta. O teste assistido é um por lote de trabalho, antes da revisão, não um por
issue nem por branch.

## Dependencies

Depends on: none
Parent: none

Replace `none` with canonical #issue links after approved publication.

`Parent` é a issue de origem de uma sub-issue (parte da mesma fatia, achado de revisão
ou de conferência); `none` numa issue de topo. Toda issue de topo entra no quadro;
sub-issue entra só pelo pai, que mostra o progresso das filhas. `Parent` é
pertencimento, não dependência: uma filha que precisa do código do pai também o lista
em `Depends on`, e na etapa 6 ela pode ser empilhada na branch dele, sem esperar o merge.

## Ownership and contention

Files/components, generated files, migrations, ports, shared test services.

## Vertical slice check

What works end to end, and how a reviewer can observe it. A prerequisite must
name its working seam, test and dependent consumer.

## Risks and session size

## Evidence checkpoints

Timestamp, branch/PR, exact HEAD/diff hashes, commands/results, independent review,
remaining blockers and next action. GitHub remains canonical; local evidence links
are not separate tickets. Do not close automatically.
