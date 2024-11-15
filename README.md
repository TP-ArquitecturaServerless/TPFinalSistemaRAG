# Trabajo Práctico Final: Implementación de un Sistema RAG usando LangChain y Ollama.

## Tabla de Contenidos🌟
- [Instanciar Entorno virtual](#instanciar-✅)✅

- [Instalación](#instalación-🔧)🔧

- [Ejecucion](#Ejecutar-💻)💻

## Instanciar Entorno virtual: 🔧
1. Navega al directorio Backen: 👌
```bash      
    cd Back
```
2. Crear e iniciar un entorno virtual:💻
```bash      
    python -m venv env
    source env/Script/activate
```
## Instalación 🔧
1. Navega al directorio del proyecto Frond: 👌
```bash      
    cd SistemaRAG
```
2. Navega al directorio del proyecto Back:👌
```bash      
    cd Back
```
3. Instala las dependencias del Frond: 📚

```bash
   npm install
```
4.  Instala las dependencias del Back: 📚
```bash
   pip install langchain-community langchain-chroma langchain-ollama fastembed langchain PyMuPDF chromadb fastapi uvicorn fastapi[all]
```
## Ejecucion 💻
1. Para su ejecución en el frond:🔉
```bash
   npm run dev
```
2. Para su ejecución en el back:🔉
```bash
   uvicorn main:app --reload
```


