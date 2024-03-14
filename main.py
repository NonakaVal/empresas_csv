import pandas as pd
import requests
import csv
import tkinter as tk
from tkinter import filedialog


def load_place_ids(csv_file):
    """Carrega os place IDs do arquivo CSV e retorna como uma lista."""
    df = pd.read_csv(csv_file)
    place_ids = df['place_id'].tolist()
    return place_ids


def get_local_info(place_ids, api_key):
    """Obtém as informações locais para cada place ID."""
    local_infos = []
    for place_id in place_ids:
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            local_infos.append(response.json())
        else:
            print(f"Falha ao obter informações para o place ID {place_id}.")
    return local_infos


def write_csv(local_infos, file_name):
    """Escreve as informações locais em um arquivo CSV."""
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Telefone', 'Website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for local in local_infos:
            if 'result' in local:
                writer.writerow({
                    'Telefone': local['result'].get('formatted_phone_number', ''),
                    'Website': local['result'].get('website', '')
                })


def concatenate_dataframes(file1, file2):
    """Concatena dois dataframes."""
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    result = pd.concat([df1, df2], axis=1)
    return result


def select_file_dialog(mode='open', default_extension=".csv"):
    """Exibe o diálogo de seleção de arquivo."""
    root = tk.Tk()
    root.withdraw()
    if mode == 'open':
        file = filedialog.askopenfilename()
    elif mode == 'save':
        file = filedialog.asksaveasfilename(defaultextension=default_extension)
    return file


def main():
    initial_file = select_file_dialog('open')
    place_ids = load_place_ids(initial_file)
    api_key = 'AIzaSyAomt6rv2nL7Et8uc61OF8nBp91MLilVJ0'
    local_infos = get_local_info(place_ids, api_key)

    temp_csv_file = 'temp_info.csv'
    write_csv(local_infos, temp_csv_file)

    result_df = concatenate_dataframes(initial_file, temp_csv_file)

    save_file_path = select_file_dialog('save')
    if save_file_path:
        # Salvando o resultado em um arquivo CSV
        result_df.to_csv(save_file_path, index=False)
        print("Arquivo resultante salvo com sucesso.")
    else:
        print("Operação cancelada.")

if __name__ == "__main__":
    main()
