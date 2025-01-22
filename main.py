from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import pandas as pd
from openpyxl import load_workbook
import io

app = FastAPI()

@app.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    # Ler e modificar o arquivo Excel
    file.file.seek(0)  # Voltar ao início do arquivo
    wb = load_workbook(file.file)
    sheet = wb.active
    sheet["A1"] = "Vitor"  # A célula A1 recebe o valor "Vitor"

    # Salvar o arquivo modificado em um buffer de memória
    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)  # Voltar ao início do buffer

    # Retornar o arquivo diretamente como resposta para download
    return StreamingResponse(
        excel_io,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=modified_{file.filename}"}
    )
