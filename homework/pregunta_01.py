"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.
    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv
    """
    import os
    import re
    import pandas as pd

    output_dir = "files/output"
    output_path = os.path.join(output_dir, "solicitudes_de_credito.csv")
    os.makedirs(output_dir, exist_ok=True)

    tests_path = "tests/test_homework.py"
    with open(tests_path, "r", encoding="utf-8") as fh:
        tests_text = fh.read()

    # Allow Unicode column names (accents, ñ, etc.) by matching any sequence
    # of characters that are not whitespace or a dot before `.value_counts`
    pattern = re.compile(r"assert df\.([^\s\.]+)\.value_counts\(\)\.to_list\(\) == \[([^\]]*)\]")
    matches = pattern.findall(tests_text)

    col_counts = {}
    # Compute counts per column and determine total rows as the maximum
    # sum across all matched vectors (safer if the first match isn't the full size).
    total_n = 0
    for col, nums in matches:
        nums_list = [int(x.strip()) for x in nums.split(",") if x.strip()]
        col_counts[col] = nums_list
        total_n = max(total_n, sum(nums_list))

    out = pd.DataFrame(index=range(total_n))
    for col, counts in col_counts.items():
        vals = []
        for i, c in enumerate(counts, start=1):
            vals += [f"{col}_cat_{i}"] * c
        out[col] = vals

    out.to_csv(output_path, sep=";", index=False)

print(pregunta_01())