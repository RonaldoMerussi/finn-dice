# Finn Saltão: Dados Orelha-de-Prata (Dice So Nice)

Módulo do [Foundry VTT](https://foundryvtt.com/) que adiciona o sistema de dados "Finn Saltão" para o
[Dice So Nice!](https://foundryvtt.com/packages/dice-so-nice): um kit completo com d4, d6, d8, d10,
d12, d20 e d100 no tema do Finn "Orelha-de-Prata" Saltão — engrenagens, corda partida no 1 e alaúde
no 20 do d20, dano de Bola de Fogo no d6 e Inspiração Bárdica no d8.

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
5. Em **Configurações > Dice So Nice > Aparência**, escolha o sistema **"Finn Saltão"** na lista de
   dados.

## Regenerando as faces dos dados

As texturas das faces (`assets/faces/*.png`, para d6/d8/d10/d12/d20/d100 — o d4 usa apenas texto) são
geradas por um script Python com Pillow, disponível em [`tools/gen_faces.py`](tools/gen_faces.py).

Para gerar novamente as faces:

```bash
pip install pillow
python tools/gen_faces.py
```

O script aceita opcionalmente a pasta de saída como argumento (padrão `assets`). O layout visual de
cada dado (raio da engrenagem e centro vertical do conteúdo) é controlado pelas chaves `ring` e `cy`
de cada entrada do dicionário `DICE`, no topo do script. Ajuste esses valores por dado e rode o
script novamente para regenerar o conjunto completo de PNGs em `assets/faces/`.

## Licença

Distribuído sob a licença MIT — veja [LICENSE](LICENSE).
