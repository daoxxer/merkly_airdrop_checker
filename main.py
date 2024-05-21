import pandas as pd
from colorama import Fore, Style, init
from tabulate import tabulate

# Инициализация colorama
init(autoreset=True)

def load_wallets(file_path):
    """Загружаем адреса кошельков из текстового файла."""
    with open(file_path, 'r') as file:
        wallets = file.readlines()
    return [wallet.strip().lower() for wallet in wallets]

def load_eligible_wallets(file_paths):
    """Загружаем данные из списка CSV файлов и объединяем их."""
    all_data = []
    for file in file_paths:
        try:
            df = pd.read_csv(file, delimiter=';', on_bad_lines='skip')
            df['Address'] = df['Address'].str.strip().str.lower()
            all_data.append(df)
        except pd.errors.ParserError as e:
            print(f"Error reading {file}: {e}")
            continue
    if not all_data:
        return {}
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data.set_index('Address')['Merky RFP Points'].to_dict()

def main():
    # Список файлов с данными о кошельках
    eligible_files = [
        "Merkly RFP Points List.csv",
        "Merkly RFP Points List 1.csv"
    ]

    # Загрузка данных из файлов
    eligible_wallets = load_eligible_wallets(eligible_files)

    # Если нет данных, выходим
    if not eligible_wallets:
        print("No valid data found in the provided CSV files.")
        return

    # Загрузка адресов кошельков для проверки
    wallets_to_check = load_wallets('wallets.txt')
    
    results = []

    for index, wallet in enumerate(wallets_to_check, start=1):
        if wallet in eligible_wallets:
            status = f"{Fore.GREEN}eligible{Style.RESET_ALL}"
            points = f"{Fore.MAGENTA}{eligible_wallets[wallet]}{Style.RESET_ALL}"
        else:
            status = f"{Fore.RED}not eligible{Style.RESET_ALL}"
            points = "N/A"
        
        results.append([f"{Fore.YELLOW}{index}{Style.RESET_ALL}", wallet, points, status])
    
    # Форматирование таблицы
    headers = [f"{Fore.BLUE}№{Style.RESET_ALL}", f"{Fore.BLUE}Wallets{Style.RESET_ALL}", f"{Fore.BLUE}Merky RFP Points{Style.RESET_ALL}", f"{Fore.BLUE}Status{Style.RESET_ALL}"]
    table = tabulate(results, headers=headers, tablefmt="fancy_grid", stralign="left")
    print(table)

if __name__ == "__main__":
    main()
