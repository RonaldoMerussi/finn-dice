# Finn Saltão: Dados Orelha-de-Prata (Dice So Nice)

Módulo do [Foundry VTT](https://foundryvtt.com/) que adiciona um sistema de dados customizado para o
[Dice So Nice!](https://foundryvtt.com/packages/dice-so-nice): um d20 com faces de engrenagem e os
símbolos do Finn "Orelha-de-Prata" Saltão (corda partida no 1, alaúde no 20).

## Dependências

Este módulo **requer** que o módulo [Dice So Nice!](https://foundryvtt.com/packages/dice-so-nice)
esteja instalado e ativado no seu mundo do Foundry VTT.

## Instalação

1. No Foundry VTT, vá em **Setup > Add-on Modules > Install Module**.
2. Cole a seguinte Manifest URL no campo correspondente:

   ```
   https://github.com/RonaldoMerussi/finn-dice/releases/latest/download/module.json
   ```

3. Clique em **Install**.
4. Dentro do seu mundo, ative o módulo em **Game Settings > Manage Modules**, junto com o
   Dice So Nice!.

## Regenerando as faces do dado

As texturas das faces do d20 (`assets/faces/*.png`) são geradas por um script Python com Pillow,
disponível em [`tools/gen_faces.py`](tools/gen_faces.py).

Para gerar novamente as faces:

```bash
pip install pillow
python tools/gen_faces.py
```

O layout visual de cada face (posição e tamanho da engrenagem) é controlado por duas constantes no
topo do script:

- `RING`: raio externo da engrenagem, em fração do lado da textura.
- `CY`: centro vertical do conteúdo (0.0 = topo, 1.0 = base).

Ajuste esses valores e rode o script novamente para regenerar o conjunto completo de PNGs em
`assets/faces/`.

## Licença

Distribuído sob a licença MIT — veja [LICENSE](LICENSE).
