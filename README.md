# Workflows — piloto para Claude Code

Um plugin independente que transforma observações do RoadS em descoberta do
problema, documentos de requisitos (PRDs) aprovados, issues verticais no GitHub e
implementação com testes e autorização delimitada. Uma única sessão pública e
quatro skills internas de apoio. Não depende do GuardianS nem altera sua instalação.

**Situação do piloto:** implementado localmente, com testes automatizados dos
utilitários e validação nativa do pacote. A integração real com RoadS, o
monitoramento pelo celular, a revisão independente e a execução completa sem
supervisão **ainda não foram homologados**. Consulte as
[evidências de aceitação](docs/acceptance.md) antes de depender de execução sem supervisão.

## Idioma

A documentação, os modelos, os exemplos e os conteúdos apresentados ao usuário
são em português. As skills, destinadas ao modelo, são escritas em inglês, mas
orientam a produção de respostas e documentos em português. Comandos, caminhos,
chaves de configuração e identificadores técnicos mantêm sua grafia original.

## Carregar localmente

Requer Claude Code com suporte a plugins, skills e `AskUserQuestion`, Python 3.11+,
Git e, para consultar o GitHub, GitHub CLI autenticado. Não exige pacotes Python adicionais.

No diretório do projeto em que você pretende trabalhar, execute:

```powershell
claude --plugin-dir C:/Software/WorkflowS
```

Na mesma sessão do Claude, use:

```text
/workflows:workflows
```

O Claude Code acrescenta o nome do plugin aos comandos. `/workflows`, mencionado
no documento de requisitos do piloto, representa a entrada conceitual; este pacote
não instala um atalho no projeto. As quatro skills de apoio ficam ocultas no menu
de comandos por meio de `user-invocable: false`. O comando `/help` deve mostrar
apenas a entrada pública do plugin. O `CLAUDE.md` da raiz orienta quem trabalha neste
repositório; o Claude não o carrega nos projetos que usam o plugin. A skill principal
contém todas as regras essenciais de operação.

Esse carregamento de desenvolvimento não instala o plugin permanentemente. Para
parar de usá-lo, encerre a sessão e inicie outra sem `--plugin-dir`. Preserve os
pontos de retomada e as cópias de trabalho isoladas do Git (worktrees). Nenhuma
configuração ou rotina automática de interceptação (hook) é instalada.

## Configurar um projeto

Copie `examples/config.json` para `.workflows/config.json` no projeto de destino,
defina o repositório exato no formato `proprietario/repositorio` e mantenha
`.workflows/` ignorado pelo Git desse projeto. Configure o RoadS somente quando o
endereço real de consulta autenticada e o formato da resposta forem conhecidos:

```json
{
  "repository": "PROPRIETARIO/REPOSITORIO",
  "roads": {
    "observations_url": "https://SEU-APLICATIVO.example/api/SUA-ROTA-DE-CONSULTA",
    "token_env": "WORKFLOWS_ROADS_TOKEN"
  }
}
```

O endereço acima é ilustrativo; não representa uma API garantida do RoadS.
O utilitário envia somente GET, obtém o token da variável de ambiente indicada,
recusa redirecionamentos e não confirma nem consome filas. Verifique se o endereço
real permite apenas leitura. Nenhum endereço ou credencial do RoadS foi presumido
a partir de outro plugin. A consulta ao quadro e ao planejamento de entregas exige
ferramentas configuradas separadamente; o utilitário consulta issues do GitHub e
uma rota JSON de observações. Integrações ausentes são informadas explicitamente.

## Fluxo de trabalho e utilitários

Inspeção → acordo de monitoramento → entrevista de decisões → PRD aprovado →
plano de issues verticais aprovado e publicado → autorização delimitada de
implementação → desenvolvimento orientado a testes (TDD), revisão e evidências.
Uma issue vertical entrega um resultado observável de ponta a ponta, incluindo as
camadas necessárias, em vez de separar tickets apenas por banco de dados, API ou tela.
As perguntas ao usuário usam `AskUserQuestion`. O GitHub é a fonte oficial;
os arquivos Markdown e JSON locais são registros e pontos de retomada, não um
segundo sistema de tickets.

Execute estes comandos no diretório do plugin:

```powershell
python scripts/workflow.py validate-plan --plan examples/plan.json
python scripts/workflow.py schedule --plan examples/plan.json --limit 2
python scripts/workflow.py context --used 85000 --reserve 15000
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
claude plugin validate . --json
claude --plugin-dir . plugin details workflows
```

O exemplo seleciona `[1, 2]`; a issue 3 depende da issue 1. O planejador escolhe o
maior conjunto seguro de issues prontas, respeita o trabalho em andamento e verifica
sobreposição de caminhos sem distinguir maiúsculas de minúsculas, para compatibilidade
com Windows. Ele recomenda um lote; a skill distribui o trabalho entre os agentes
ou sessões disponíveis do Claude, respeitando a autorização e a capacidade reais.
A validação estrutural não determina se o texto descreve uma entrega realmente
vertical. Isso exige a revisão de conteúdo da skill e a avaliação fornecida.

Leia o [protocolo](docs/protocol.md), os [limites de segurança](docs/security.md),
as [verificações manuais do piloto](evals/pilot.md) e a [recuperação](docs/recovery.md).

## Fontes da documentação

O formato e os comandos seguem as referências oficiais de
[plugins do Claude Code](https://code.claude.com/docs/en/plugins) e
[skills](https://code.claude.com/docs/en/skills). O monitoramento segue a documentação
de [Remote Control](https://code.claude.com/docs/en/remote-control). O desenho de
permissões foi conferido na [referência de hooks](https://code.claude.com/docs/en/hooks).
Essas fontes externas estão em inglês. Consulta realizada em 24/09/2026; versão da
CLI testada localmente: 2.1.278. A validação nativa avisa que o CLAUDE.md da raiz não
é carregado nos projetos consumidores; isso é tratado pela skill principal.
