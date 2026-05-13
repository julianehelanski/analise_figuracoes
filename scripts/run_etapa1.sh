#!/usr/bin/env bash
# Pipeline da Etapa 1 em sequência, sobre as obras com escopo_etapa1 == 'sim'.
# Requer .env configurado e Google Drive sincronizado localmente.
#
# Uso:
#     bash scripts/run_etapa1.sh
#     bash scripts/run_etapa1.sh --force            # reextrai texto

set -euo pipefail
cd "$(dirname "$0")/.."

EXTRA_EXTRACAO="${1:-}"

echo "==> 01_extract_text"
python scripts/01_extract_text.py $EXTRA_EXTRACAO

echo "==> 02_kwic"
python scripts/02_kwic.py --autor latour --janela 10

echo "==> 03_frequencies"
python scripts/03_frequencies.py

echo "==> 04_visualizations"
python scripts/04_visualizations.py

echo "==> 05_cooccurrence"
python scripts/05_cooccurrence.py --janela 200

echo "==> 06_sampling (amostra estratificada de 45 páginas)"
python scripts/06_sampling.py

echo "==> 07_trajectory"
python scripts/07_trajectory.py

echo
echo "Etapa 1 concluída. Entregáveis principais:"
echo "  - corpus/qualidade_extracao.csv             (taxa de qualidade por obra)"
echo "  - outputs/amostra_validacao_etapa1.csv      (45 páginas para validação)"
echo "  - outputs/<obra_id>/csv/frequencias.csv     (tabelas de frequência)"
echo "  - outputs/trajetoria_latour_1986_1999.md    (relatório de trajetória)"
