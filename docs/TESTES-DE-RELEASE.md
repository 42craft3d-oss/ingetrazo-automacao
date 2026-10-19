# Checklist de release

Execute em uma cópia de teste de um modelo e reinicie o IngeTrazo antes da validação.

## Interface e idiomas

- [ ] Abrir a janela Automação em português, inglês e espanhol.
- [ ] Conferir título, botões, campos, tooltips, avisos de captura e mensagens de erro.
- [ ] Confirmar que a instrução fica abaixo de `+ Adicionar bloco`.
- [ ] Confirmar que o relógio fica abaixo dos botões de transporte e o passo ao lado.

## Eixo e persistência

- [ ] Em rotação, capturar A e B em uma peça.
- [ ] Após o segundo ponto, confirmar que `2 pontos` aparece habilitado e marcado automaticamente.
- [ ] Alternar entre `2 pontos`, X, Y e Z; confirmar que o eixo salvo muda corretamente.
- [ ] Salvar, fechar e reabrir o `.igz`; confirmar que blocos, locks, modo e eixo são preservados.

## Movimento

- [ ] Testar rotação nos sentidos horário e anti-horário.
- [ ] Testar deslocamento A → B e B → A.
- [ ] Testar os modos lineares Soma, Ida e Ida + volta com pelo menos duas repetições.
- [ ] Testar delay, velocidade, repetição infinita e múltiplos blocos.

## Transporte

- [ ] Play atualiza o relógio continuamente.
- [ ] Play reverso reduz o relógio e para no início.
- [ ] Pause congela a posição e retoma sem salto.
- [ ] Passo atrás/frente atualiza posição e relógio.
- [ ] Stop restaura todas as peças e `00:00,00`.

## Higiene de release

- [ ] Não incluir log, cache, backups ou ícones não referenciados.
- [ ] Conferir que o release contém exatamente os arquivos da seção Estrutura do pacote no README.
- [ ] Verificar que um novo `automacao-debug.log` não registra erro durante este checklist.
