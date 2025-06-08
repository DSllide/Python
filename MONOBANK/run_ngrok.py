from pyngrok import ngrok
import uvicorn

public_url = ngrok.connect(8000)
print(f"Ngrok public URL: {public_url}")
uvicorn.run("main:app", port=8000, reload=True)
