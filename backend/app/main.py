"""Safe, small API for the MATLAB Scientific Computing Academy.

This API provides named, bounded simulations. It intentionally does not run
arbitrary user-submitted Python, MATLAB, shell commands, or uploaded files.
"""
from __future__ import annotations
import math
import os
from typing import Literal
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

app = FastAPI(title="MATLAB Scientific Computing Academy API", version="1.0.0", description="Named scientific demonstrations and lesson metadata; no arbitrary code execution.")
allowed_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

class DiffractionRequest(BaseModel):
    wavelength_nm: float = Field(default=550, ge=380, le=780)
    slit_width_um: float = Field(default=50, ge=5, le=500)
    screen_distance_m: float = Field(default=1, ge=0.1, le=5)
    points: int = Field(default=401, ge=51, le=2001)

class IntegrationRequest(BaseModel):
    points: int = Field(default=101, ge=3, le=10001)

@app.get("/health")
def health():
    return {"status": "ok", "service": "matlab-scientific-academy-api", "version": "1.0.0"}

@app.get("/api/lessons")
def lessons():
    return {"lessons": [
        {"slug":"fundamentals","title":"MATLAB fundamentals","level":"Beginner"},
        {"slug":"programming","title":"Scripts & algorithms","level":"Beginner"},
        {"slug":"numerical-methods","title":"Numerical methods","level":"Intermediate"},
        {"slug":"visualization","title":"Plotting & data analysis","level":"Intermediate"},
        {"slug":"physics","title":"Computational physics","level":"Intermediate"},
        {"slug":"optics","title":"Light & optical systems","level":"Advanced"},
        {"slug":"instrumentation","title":"Optical & biomedical sensors","level":"Advanced"},
        {"slug":"projects","title":"Scientific projects","level":"Research-oriented"}
    ]}

@app.post("/api/simulate/diffraction")
def simulate_diffraction(req: DiffractionRequest):
    wavelength = req.wavelength_nm * 1e-9
    slit = req.slit_width_um * 1e-6
    x = np.linspace(-0.015, 0.015, req.points)
    theta = np.arctan(x / req.screen_distance_m)
    beta = np.pi * slit * np.sin(theta) / wavelength
    intensity = np.ones_like(beta)
    mask = np.abs(beta) > 1e-12
    intensity[mask] = (np.sin(beta[mask]) / beta[mask]) ** 2
    return {"model":"ideal single-slit Fraunhofer diffraction", "x_mm":(x*1000).round(7).tolist(), "intensity":intensity.round(9).tolist(), "first_minimum_mm":wavelength*req.screen_distance_m/slit*1000, "central_width_mm":2*wavelength*req.screen_distance_m/slit*1000, "assumptions":["ideal single slit", "far-field Fraunhofer intensity model", "small-angle estimate for reported width"]}

@app.post("/api/simulate/integration")
def simulate_integration(req: IntegrationRequest):
    x = np.linspace(0, math.pi, req.points)
    y = np.sin(x)
    estimate = float(np.trapezoid(y, x))
    return {"function":"sin(x)", "interval":[0, math.pi], "points":req.points, "estimate":estimate, "exact_value":2.0, "absolute_error":abs(estimate-2.0), "x":x.tolist(), "y":y.tolist()}

@app.get("/api/examples/{topic}")
def example(topic: Literal["sine", "diffraction", "integration"]):
    examples = {
        "sine": {"filename":"first_plot.m", "code":"x = linspace(0, 2*pi, 200);\ny = sin(x);\nplot(x, y, 'LineWidth', 2);\nxlabel('x (radians)'); ylabel('sin(x)'); grid on;"},
        "diffraction": {"filename":"single_slit.m", "code":"lambda = 550e-9; a = 50e-6; L = 1;\nx = linspace(-0.015, 0.015, 1000);\ntheta = atan(x/L); beta = pi*a*sin(theta)/lambda;\nI = ones(size(beta)); idx = abs(beta) > 1e-12;\nI(idx) = (sin(beta(idx))./beta(idx)).^2;\nplot(x*1e3, I); xlabel('Position (mm)'); ylabel('I/I_0'); grid on;"},
        "integration": {"filename":"trapezoid.m", "code":"x = linspace(0, pi, 101);\ny = sin(x);\nestimate = trapz(x, y);\nabsolute_error = abs(estimate - 2);"}
    }
    return examples[topic]

@app.exception_handler(Exception)
async def safe_error_handler(request, exc):
    # Avoid leaking internal details to callers; server logs retain diagnostics.
    return JSONResponse(status_code=500, content={"detail":"An internal server error occurred."})
