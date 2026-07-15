"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import os
    import zipfile
    from pathlib import Path
    import pandas as pd

    # Mapear meses a números
    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    # Raíz del repositorio: un nivel arriba de homework/
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Leer todos los archivos ZIP
    input_dir = os.path.join(root, "files", "input")
    all_dfs = []

    for i in range(10):
        zip_path = os.path.join(input_dir, f"bank-marketing-campaing-{i}.csv.zip")
        with zipfile.ZipFile(zip_path, "r") as z:
            csv_file = z.namelist()[0]
            with z.open(csv_file) as f:
                df = pd.read_csv(f)
                all_dfs.append(df)

    # Combinar todos los datos
    df = pd.concat(all_dfs, ignore_index=True)

    # Crear directorio de salida
    output_dir = os.path.join(root, "files", "output")
    os.makedirs(output_dir, exist_ok=True)

    # ========== CLIENT.CSV ==========
    client = df[
        ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]
    ].copy()

    # Transformar job: reemplazar "." por "" y "-" por "_"
    client["job"] = client["job"].str.replace(".", "").str.replace("-", "_")

    # Transformar education: reemplazar "." por "_" y "unknown" por pd.NA
    client["education"] = client["education"].str.replace(".", "_")
    client.loc[client["education"] == "unknown", "education"] = pd.NA

    # Transformar credit_default: "yes" → 1, resto → 0
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)

    # Transformar mortgage: "yes" → 1, resto → 0
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # Guardar
    client.to_csv(os.path.join(output_dir, "client.csv"), index=False)

    # ========== CAMPAIGN.CSV ==========
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "month",
            "day",
        ]
    ].copy()

    # Transformar previous_outcome: "success" → 1, resto → 0
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)

    # Transformar campaign_outcome: "yes" → 1, resto → 0
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    # Crear last_contact_date
    campaign["last_contact_date"] = campaign.apply(
        lambda row: f"2022-{month_map[row['month']]}-{str(int(row['day'])).zfill(2)}",
        axis=1,
    )

    # Seleccionar columnas finales
    campaign = campaign[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "last_contact_date",
        ]
    ]

    # Guardar
    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)

    # ========== ECONOMICS.CSV ==========
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    # Guardar
    economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)


if __name__ == "__main__":
    clean_campaign_data()