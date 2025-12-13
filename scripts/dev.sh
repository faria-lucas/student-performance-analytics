#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📁 Project root: $PROJECT_ROOT"

# Ativar ambiente virtual
if [ ! -d ".venv" ]; then
  echo "❌ Virtual environment (.venv) not found."
  echo "👉 Create it first with: uv venv .venv"
  exit 1
fi

source .venv/bin/activate
echo "🐍 Virtual environment activated"

# Configurações
API_HOST="127.0.0.1"
API_PORT="8000"
DASHBOARD_PORT="8501"

echo "🚀 Starting FastAPI on http://${API_HOST}:${API_PORT} ..."
uvicorn src.api.main:app \
  --host "${API_HOST}" \
  --port "${API_PORT}" \
  --reload &

API_PID=$!

# Aguarda a API subir
sleep 2

echo "📊 Starting Streamlit dashboard on http://localhost:${DASHBOARD_PORT} ..."
export API_BASE_URL="http://${API_HOST}:${API_PORT}"
streamlit run src/dashboard/app.py --server.port "${DASHBOARD_PORT}"

# Quando o Streamlit parar, encerra a API também
echo "🛑 Shutting down FastAPI..."
kill $API_PID
