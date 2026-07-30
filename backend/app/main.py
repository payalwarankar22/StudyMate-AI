from fastapi import FastAPI

# creates our FastAPI application.
app = FastAPI(
        title = "StudyMate AI API",
        description = "Backend API for StudyMate AI",
        version = "0.1.0"

)

# creates our first API endpoint.
@app.get("/")
def root():
    return {
       " message : StudyMet AI API is running"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    }