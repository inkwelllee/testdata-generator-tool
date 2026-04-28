# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Run the application
python main.py

# Install Python dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
pytest tests/test_generators.py -v  # single file with verbose

# Frontend (gui/)
cd gui && npm install       # install dependencies
npm run dev                 # dev server with hot reload
npm run build:copy          # build and copy to assets/ui/
```

## Architecture

**Python Backend (pywebview) + Vue 3 Frontend**

### Backend (src/)
- `generators/`: Data generators inheriting from `DataGenerator` base class. Each generator receives configuration via dependency injection in `__init__`.
- `services/`: `ImageService` (ID card/business license image generation with PIL), `PathService` (path utilities)
- `configs/`: `ConfigManager` singleton with lazy-loaded area codes; `constants.py` has static data (bank prefixes, name data)
- `utils/api.py`: `Api` class exposes all public methods to frontend via pywebview's JS bridge (`pywebview.api.methodName()`)

### Frontend (gui/)
Vue 3 + Vite + Element Plus. Components in `components/`, pages in `views/`.

### Key Integration
- `main.py` creates a pywebview window pointing to Vite dev server (`localhost:8098`) in dev or built files in production
- Frontend calls backend through pywebview's JS bridge, not HTTP
- `Api` class is the bridge - all public methods are callable from frontend

## Configuration

Application behavior controlled by `CONFIG` dict in `main.py`:
- `enable_file_logging_in_production`: Log to file when packaged
- `use_pywebview_directory`: Use `%APPDATA%/pywebview/` for logs
- `clear_cache_on_startup`: Clear WebView cache on start

Window settings (always-on-top) persisted in `%APPDATA%/pywebview/window_config.json`.

## Packaging

Build frontend first, then PyInstaller:
```bash
cd gui && npm run build:copy && cd ..
pyinstaller -i assets/ico.ico --name 测试数据生成器 --windowed --clean --noconfirm --onefile --add-data "assets;assets" main.py
```
