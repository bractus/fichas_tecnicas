# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[byterover-mcp]

# important 
always use byterover-retrieve-knowledge tool to get the related context before any tasks 
always use byterover-store-knowledge to store all the critical informations after sucessful tasks
# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

## Architecture Overview

This is a **CrewAI-based culinary recipe processing system** that extracts recipe data from multiple sources and generates Excel technical sheets with cost calculations. The system uses a multi-agent architecture with specialized agents for different tasks.

### Core Components

- **main.py**: Main orchestrator using CrewAI framework with 4 specialized agents
- **tools/**: Custom CrewAI tools for file reading, web scraping, Excel generation, and EXA search  
- **config/**: YAML-based configuration for agents, tasks, and data sources
- **files/fc/**: RAG knowledge base for ingredient correction factors
- **output/**: Generated Excel files destination

### Agent Architecture

The system uses 4 specialized CrewAI agents:
1. **file_reader_agent**: Extracts content from files and URLs
2. **ficha_tecnica_agent**: Extracts complete recipe technical sheets with correction factors
3. **base_insumos_agent**: Researches market prices and creates consolidated ingredient base
4. **excel_writer_agent**: Generates single Excel file with all sheets and ingredient database

### Data Flow

1. Sources (files/URLs) → Content extraction
2. Content → Recipe extraction with correction factors (uses RAG + web search)
3. Recipes → Market price research for consolidated ingredients
4. All data → Excel generation with cost calculations and CMV

## Common Development Commands

### Running the Application

```bash
# Standard execution
python main.py

# Docker execution (recommended)
docker-compose up --build

# Docker background execution
docker-compose up -d --build

# View Docker logs
docker-compose logs -f
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Install Python dependencies
pip install -r requirements.txt
```

### Docker Operations

```bash
# Build and run
docker-compose up --build

# Interactive debugging
docker-compose run --rm fichas-tecnicas bash

# Clean up
docker-compose down --rmi all --volumes --remove-orphans
```

## Configuration System

### Key Configuration Files

- **config/agents.yaml**: Agent definitions with roles, goals, and tools
- **config/tasks.yaml**: Task definitions with context dependencies and Pydantic output models
- **config/sources.yaml**: Input sources (files and URLs to process)

### Adding New Sources

Edit `config/sources.yaml` to add new recipe sources:
```yaml
sources:
  - './input_examples/new_recipe.txt'
  - 'https://example.com/recipe-url'
```

### LLM Configuration

The system uses two OpenAI models:
- **gpt-5-nano**: For file reading and Excel generation (temperature=0.0)
- **gpt-5-mini**: For recipe extraction (temperature=0.0)

## Data Models (Pydantic)

### Core Models
- **FichaTecnica**: Complete recipe with ingredients, portions, pricing
- **Ingrediente**: Individual ingredient with quantity, unit (kg/L), correction factor, cost
- **Insumo**: Market-priced ingredient with supplier and quote date
- **RecipeData**: Complete data structure combining recipes and ingredient database

### Key Constraints
- **Units**: Mandatory "kg" or "L" only (never grams/ml)
- **Correction factors**: Applied to all ingredients for waste/loss calculation
- **Pricing**: All in BRL with market research validation

## Tool System

### Custom Tools (tools/ directory)
- **MultiFormatFileReader**: Handles TXT, DOCX, PDF, XLSX files
- **WebScrapingTool**: Web content extraction for URLs
- **ExcelGeneratorTool**: Creates structured Excel output with multiple sheets
- **EXASearchTool**: Enhanced web search for market pricing

### RAG Integration
- Correction factors database stored in `files/fc/fatores1.md` and `fatores2.md`
- Used by ficha_tecnica_agent before web search for ingredient correction factors

## Output Structure

Generated Excel files are saved to `/output/` with structure:
- One sheet per recipe with detailed cost calculations
- "Base de Insumos" sheet with consolidated ingredient pricing
- CMV (Cost of Goods Sold) calculations
- Filename format: `FICHA_TECNICA_COMPLETA_YYYYMMDD_HHMMSS.xlsx`

## Development Guidelines

### Working with Agents
- Each agent has specific tools and responsibilities
- Tasks have context dependencies (sequential processing)
- All outputs use Pydantic models for validation

### Adding New Ingredients/Recipes
1. Update source files in `input_examples/` or URLs in `config/sources.yaml`
2. Add correction factors to `files/fc/` markdown files if needed
3. Run the system - agents will automatically extract and process new content

### Monitoring and Logging
- Comprehensive logging to `fichas_tecnicas.log`
- Langfuse integration for agent execution tracking
- File validation with automatic cleanup of corrupted Excel files

## Docker Environment

The system runs in Python 3.11-slim containers with:
- Volume mounts for input, output, and configuration directories
- Environment variable injection for API keys
- Non-root user execution for security
- Automatic output directory creation

### Required Environment Variables
- `OPENAI_API_KEY`: OpenAI API access
- `SERPER_API_KEY`: Search API access  
- `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`: Monitoring
- `EXA_API_KEY`: Enhanced search capabilities