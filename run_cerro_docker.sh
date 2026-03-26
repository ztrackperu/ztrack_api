#!/usr/bin/env bash
# Usa tu test_cerro.json del directorio actual y deja datos_cerro_prieto_antiguo.json aquí.
# Uso: ./run_cerro_docker.sh   (o bash run_cerro_docker.sh)

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
docker run --rm \
  -v "${DIR}":/data \
  -e INPUT_FILE=/data/santa_anita.json \
  -e OUTPUT_FILE=/data/santa_anita_ok.json \
  cerro-prieto
echo "Archivo generado: ${DIR}/datos_cerro_prieto_antiguo.json"
