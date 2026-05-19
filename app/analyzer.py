import re
from app.models import AnalysisResult

# Reglas de detección con su peso
RULES = [
    (r"ignora?\s+(tus\s+)?(instrucciones|reglas|restricciones)", "ignorar_instrucciones", 3),
    (r"olvida?\s+(tus\s+)?(instrucciones|reglas|restricciones)", "olvidar_instrucciones", 3),
    (r"(actúa|actua|comporta)\s+(como|siendo)\s+una?\s+ia\s+sin", "ia_sin_restricciones", 4),
    (r"(eres|ahora\s+eres|imagina\s+que\s+eres)\s+una?\s+ia\s+sin", "rol_ia_sin_limites", 4),
    (r"(pretende|simula|imagina)\s+que\s+no\s+tienes\s+(reglas|restricciones|limites|límites)", "simular_sin_reglas", 4),
    (r"(do\s+anything\s+now|dan\s+mode|developer\s+mode|jailbreak)", "modo_sin_filtros", 5),
    (r"(ignora|bypass|salta|evita)\s+(el\s+)?(filtro|sistema|seguridad)", "bypass_seguridad", 4),
    (r"(muéstrame|dime|revela|explica)\s+(tu\s+)?(prompt\s+de\s+sistema|instrucciones\s+internas|configuracion)", "extraer_sistema", 3),
    (r"(roleplay|rol|personaje)\s+.{0,30}\s+(sin\s+límites|sin\s+restricciones|prohibido|ilegal)", "roleplay_evasion", 3),
    (r"(para\s+una\s+novela|para\s+una\s+historia|ficcion|ficticio).{0,50}(instrucciones|como\s+hacer|pasos)", "ficcion_evasion", 2),
    (r"[A-Za-z0-9+/]{20,}={0,2}", "posible_base64", 2),
    (r"(nuevo\s+rol|nueva\s+identidad|nuevo\s+personaje).{0,30}(sin\s+límites|sin\s+filtros)", "cambio_rol", 3),
    (r"(sistema|system)\s*:\s*(ignora|olvida|ahora\s+eres)", "inyeccion_sistema", 5),
    (r"(admin|administrator|root|superuser)\s*(mode|modo|access|acceso)", "acceso_admin", 4),
]

def analyze_prompt(prompt: str) -> AnalysisResult:
    text = prompt.lower().strip()
    score = 0
    triggered = []

    for pattern, name, weight in RULES:
        if re.search(pattern, text, re.IGNORECASE):
            score += weight
            triggered.append(name)

    # Calcular nivel de riesgo
    if score == 0:
        risk_level = "bajo"
        decision = "permitir"
        message = "La entrada no presenta señales de riesgo."
    elif score <= 2:
        risk_level = "bajo"
        decision = "permitir"
        message = "La entrada presenta señales leves. Se permite con registro."
    elif score <= 5:
        risk_level = "medio"
        decision = "advertir"
        message = "La entrada presenta señales moderadas de manipulación."
    else:
        risk_level = "alto"
        decision = "bloquear"
        message = "La entrada presenta señales claras de intento de manipulación."

    return AnalysisResult(
        prompt=prompt,
        score=score,
        risk_level=risk_level,
        triggered_rules=triggered,
        decision=decision,
        message=message
    )
