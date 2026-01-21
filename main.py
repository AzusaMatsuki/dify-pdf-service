import os
from fastapi import FastAPI, Body
from fastapi.responses import Response
import markdown
from xhtml2pdf import pisa
from io import BytesIO

app = FastAPI()

@app.post("/generate-pdf")
async def generate_pdf(content: str = Body(embed=True), company_name: str = Body(embed=True)):
    # 1. MarkdownをHTMLに変換
    html_content = f"""
    <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family: Arial, sans-serif;">
            <h1>{company_name} 様 採用戦略レポート</h1>
            {markdown.markdown(content)}
        </body>
    </html>
    """
    
    # 2. HTMLをPDFに変換
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_buffer)
    
    # 3. PDFファイルをレスポンスとして返す
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
