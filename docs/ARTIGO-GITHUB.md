# Automação por componente no IngeTrazo

O plugin **Automação** adiciona uma prévia cinemática por componente ao IngeTrazo. Cada peça pode receber blocos independentes de rotação ou deslocamento linear, e todos podem ser reproduzidos juntos.

![Demonstração da Automação no IngeTrazo](media/automacao.gif)

## O que ele faz

- Rotação em X, Y, Z ou em um eixo definido por dois pontos.
- Deslocamento linear com direção, velocidade e repetição.
- Três modos lineares: Soma, Ida e Ida + volta.
- Vários blocos de movimento por peça.
- Controle de Play, reverso, Pause, Stop e avanço por passo.
- Relógio de tempo corrente durante a prévia.
- Configuração salva no arquivo `.igz`.

## Uso em poucos passos

1. Abra Automação e selecione uma peça.
2. Adicione um bloco de Rotação ou Deslocamento linear.
3. Defina X, Y, Z ou capture dois pontos no viewport para usar um eixo livre.
4. Ajuste os parâmetros e aperte Play.

O plugin é uma prévia cinemática de viewport: não tenta simular colisões, engrenamento ou física.

## Instalação

Baixe o pacote da release, copie a pasta `automacao` inteira para a pasta de plugins do IngeTrazo e reinicie o aplicativo. As instruções completas estão no [README](../README.md).

## Idiomas

A interface acompanha o idioma do IngeTrazo: português, inglês ou espanhol.
