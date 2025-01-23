from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import pandas as pd
from openpyxl import load_workbook
import io
import os

app = FastAPI()

# Diretório para armazenar arquivos localmente (simula um serviço de armazenamento)
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/")
async def create_upload_file(
    file: UploadFile = File(...),  # Arquivo Excel enviado
    name: str = Form(...),        # Parâmetro obrigatório vindo do formulário (Bubble Dropdown)
    return_url: bool = Form(False)  # Parâmetro opcional para retornar URL ou arquivo diretamente
):
    # Verifica se o nome foi fornecido
    if not name:
        raise HTTPException(status_code=400, detail="O parâmetro 'name' é obrigatório.")

    # Ler e modificar o arquivo Excel
    try:
        file.file.seek(0)  # Voltar ao início do arquivo
        wb = load_workbook(file.file)
        sheet = wb.active

        # Usar o parâmetro 'name' para modificar o Excel dinamicamente
        sheet["A1"] = name  # A célula A1 recebe o valor do parâmetro 'name'

        if return_url:
            # Salvar o arquivo no servidor local
            file_path = os.path.join(UPLOAD_DIR, f"modified_{file.filename}")
            wb.save(file_path)

            # Construir a URL pública do arquivo
            file_url = f"https://api-edd.onrender.com/{file_path}"
            return JSONResponse({"file_url": file_url})

        # Caso contrário, retornar o arquivo diretamente
        excel_io = io.BytesIO()
        wb.save(excel_io)
        excel_io.seek(0)  # Voltar ao início do buffer

        return StreamingResponse(
            excel_io,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=modified_file.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
