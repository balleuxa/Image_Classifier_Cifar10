# Open the client interface
Start-Process "$PSScriptRoot\client\index.html"

# Start the FastAPI server using the venv inside /server/
Start-Process powershell -ArgumentList "cd $PSScriptRoot\server; uvicorn app:app --reload"


