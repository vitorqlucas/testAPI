from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import pandas as pd
from openpyxl import load_workbook
import io

app = FastAPI()

@app.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    # Forçar o pandas a usar o engine openpyxl para ler o arquivo Excel
    df = pd.read_excel(file.file, engine="openpyxl")
    
    # Modificar a célula A1 usando openpyxl
    file.file.seek(0)  # Voltar para o início do arquivo
    wb = load_workbook(file.file)
    sheet = wb.active
    sheet["A1"] = "Vitor"  # A célula A1 recebe o valor "Vitor"
    
    # Salvar a planilha em um buffer de memória
    excel_io = io.BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)  # Voltar para o início do arquivo no buffer
    
    # Retornar o arquivo Excel modificado para download
    return StreamingResponse(excel_io, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=modified_file.xlsx"})
