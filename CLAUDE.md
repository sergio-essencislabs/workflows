# Piloto Workflows

Plugin independente para Claude Code. Entrada: `/workflows:workflows`, a forma com
prefixo do plugin para o `/workflows` descrito nos requisitos. Leia `skills/workflows/SKILL.md`.

Idioma: mantenha README, documentação, modelos, exemplos e textos apresentados ao
usuário em português. Somente as skills são redigidas em inglês; elas devem orientar
respostas e documentos em português. Preserve comandos e identificadores técnicos.

O GitHub é a fonte oficial de escopo, critérios de aceitação, dependências e situação
das issues. Registros locais são evidências e cópias de referência, nunca tickets
duplicados. Informe divergências. Faça todas as perguntas por `AskUserQuestion`;
não invente aprovação. Descoberta, PRD, publicação de issues e implementação
delimitada têm aprovações separadas.

Use worktrees isoladas. A autorização comum de implementação não permite escrever
em branches protegidas, fazer merge, implantar ou publicar versões. Preserve o
GuardianS e os dados do usuário. Leia `docs/protocol.md` para execução e retomada,
e `docs/security.md` para os limites de aplicação das permissões. Execute
`python -m unittest discover -s tests -v` e `python -m compileall -q scripts tests`.
Não apresente testes com dados simulados como homologação de integrações reais.
