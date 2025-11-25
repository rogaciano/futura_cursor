from openpyxl import load_workbook

wb = load_workbook('futuraDesprotegidaModelo1.xlsx')
ws = wb['CÁLCULO']

print("Data Validations in CÁLCULO:")
for dv in ws.data_validations.dataValidation:
    print(f"Range: {dv.sqref}, Formula: {dv.formula1}")

