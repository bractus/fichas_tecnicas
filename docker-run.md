# Docker Setup para Fichas Técnicas

## Pré-requisitos
- Docker
- Docker Compose
- Arquivo `.env` com as variáveis necessárias

## Configuração

1. **Copie o arquivo de exemplo de variáveis:**
```bash
cp .env.example .env
```

2. **Edite o arquivo `.env` com suas chaves de API:**
```bash
nano .env
```

## Execução

### Opção 1: Docker Compose (Recomendado)
```bash
# Build e execução
docker-compose up --build

# Executar em background
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Opção 2: Docker puro
```bash
# Build da imagem
docker build -t fichas-tecnicas .

# Execução
docker run -it --rm \
  --env-file .env \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/input_examples:/app/input_examples \
  -v $(pwd)/files:/app/files \
  fichas-tecnicas
```

## Volumes

- `./output:/app/output` - Arquivos Excel gerados
- `./input_examples:/app/input_examples` - Arquivos de entrada
- `./files:/app/files` - Arquivos de fatores de correção

## Troubleshooting

### Problemas de permissão
```bash
# Ajustar permissões do diretório output
sudo chown -R $USER:$USER output/
```

### Limpar containers e imagens
```bash
docker-compose down --rmi all --volumes --remove-orphans
docker system prune -a
```

### Executar interativamente para debug
```bash
docker-compose run --rm fichas-tecnicas bash
```