#!/usr/bin/env python3
"""Hook opcional `UserPromptSubmit` do Frontlights: lembra o modelo de abrir o /frontlights quando a
pessoa cita o plugin em linguagem comum ("frontlights, ataque a issue <n>", "ativar frontlights").

Por que existe: sem a barra, abrir o estágio 1 (as perguntas do roadmap, do resumo e do fechamento)
depende de o modelo decidir invocar o comando, e já houve a frase lida como pedido à sessão vizinha do próprio plugin. Este hook não decide nada pelo modelo: só injeta um lembrete no turno.

O plugin não instala hooks. Para ligar este, copie o arquivo para `~/.claude/hooks/` e registre-o no
`~/.claude/settings.json` do usuário (passo a passo no README, seção "Início por linguagem natural").
Ele lê o JSON do hook na entrada padrão (`prompt`, `transcript_path`) e, quando há o que lembrar,
imprime na saída padrão um JSON com `hookSpecificOutput.additionalContext`; em qualquer outro caso
não imprime nada e sai com 0, então nunca bloqueia nem atrasa um prompt.

Não lembra quando:
- o prompt já começa com `/frontlights`;
- a palavra aparece só dentro de um caminho, nome de arquivo ou identificador (`.frontlights/`,
  `frontlights.py`, `<pasta>/frontlights`);
- a sessão está aberta na pasta do próprio plugin (quem o desenvolve cita o nome o tempo todo);
- o transcrito da sessão já mostra o Frontlights aberto (o comando ou o `SKILL.md` aparecem nele).
"""

import json
import os
import re
import sys

MENTION = re.compile(r'(?<![\w/\\.-])frontlights(?![\w/\\-]|\.\w)', re.IGNORECASE)
OPENED = ('command-name>/frontlights', 'skills/frontlights/SKILL.md', 'skills\\\\frontlights\\\\SKILL.md')
CHUNK = 1024 * 1024

REMINDER = (
    'A pessoa citou o Frontlights. Se ela quer usar o plugin (iniciar, ativar, atuar, atacar ou retomar uma '
    'issue), execute o comando /frontlights com o pedido dela ANTES de qualquer outro trabalho, para que a '
    'etapa 1 faça as perguntas do roadmap, do resumo para a diretoria e do fechamento. Aqui "frontlights" é o '
    'plugin, não uma sessão ou um projeto de mesmo nome (o repositório do próprio plugin), a não ser que a '
    'pessoa peça claramente para falar com essa sessão. Se o Frontlights já foi aberto nesta sessão, ignore '
    'este lembrete.'
)


def already_opened(transcript_path):
    """Whether the session transcript shows Frontlights already open. Unreadable means no."""
    if not isinstance(transcript_path, str) or not transcript_path:
        return False
    try:
        tail = ''
        with open(transcript_path, encoding='utf-8', errors='replace') as handle:
            while True:
                block = handle.read(CHUNK)
                if not block:
                    return False
                text = tail + block
                if any(marker in text for marker in OPENED):
                    return True
                tail = text[-max(len(marker) for marker in OPENED):]
    except OSError:
        return False


def is_the_plugin_itself(cwd):
    if not isinstance(cwd, str) or not cwd:
        return False
    try:
        with open(os.path.join(cwd, '.claude-plugin', 'plugin.json'), encoding='utf-8-sig') as handle:
            return json.load(handle).get('name') == 'frontlights'
    except (OSError, ValueError, AttributeError):
        return False


def reminder(data):
    prompt = data.get('prompt') if isinstance(data, dict) else None
    if not isinstance(prompt, str) or is_the_plugin_itself(data.get('cwd')):
        return None
    if prompt.lstrip().lower().startswith('/frontlights') or not MENTION.search(prompt):
        return None
    if already_opened(data.get('transcript_path')):
        return None
    return REMINDER


def main():
    try:
        data = json.loads(sys.stdin.buffer.read())
        message = reminder(data)
    except (ValueError, OSError, RecursionError):
        return 0
    if message:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit', 'additionalContext': message}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
