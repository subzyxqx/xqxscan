import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import tkinter as tk
from tkinter import scrolledtext
import threading

def extract_links_with_pattern():
    base_url = url_entry.get().strip()
    pattern = pattern_entry.get().strip()
    result_text.delete(1.0, tk.END)

    if not base_url or not pattern:
        result_text.insert(tk.END, "Por favor, insira uma URL e um padrão de busca.\n")
        return
    
    visited_urls = set()
    matching_urls = set()
    to_visit = [base_url]
    regex_pattern = re.compile(re.escape(pattern), re.IGNORECASE)

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited_urls:
            continue

        root.after(0, result_text.insert, tk.END, f"Visitando: {current_url}\n")
        root.after(0, result_text.update_idletasks)
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                root.after(0, result_text.insert, tk.END, f"Erro ao acessar {current_url}: {response.status_code}\n")
                continue

            if regex_pattern.search(current_url):
                matching_urls.add(current_url)

            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                if urlparse(full_url).netloc == urlparse(base_url).netloc and full_url not in visited_urls:
                    to_visit.append(full_url)

        except Exception as e:
            root.after(0, result_text.insert, tk.END, f"Erro ao processar {current_url}: {e}\n")

    root.after(0, result_text.insert, tk.END, "\nResultados encontrados:\n")
    if matching_urls:
        for url in matching_urls:
            root.after(0, result_text.insert, tk.END, url + "\n")
    else:
        root.after(0, result_text.insert, tk.END, "Nenhum resultado encontrado.\n")
    root.after(0, result_text.update_idletasks)

def start_search():
    search_thread = threading.Thread(target=extract_links_with_pattern, daemon=True)
    search_thread.start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("SAN_LINK")
root.configure(bg="black")

# Título ASCII
title_ascii = """
░██████╗░█████╗░░█████╗░███╗░░██╗  ██╗░░░░░██╗███╗░░██╗██╗░░██╗
██╔════╝██╔══██╗██╔══██╗████╗░██║  ██║░░░░░██║████╗░██║██║░██╔╝
╚█████╗░██║░░╚═╝███████║██╔██╗██║  ██║░░░░░██║██╔██╗██║█████═╝░
░╚═══██╗██║░░██╗██╔══██║██║╚████║  ██║░░░░░██║██║╚████║██╔═██╗░
██████╔╝╚█████╔╝██║░░██║██║░╚███║  ███████╗██║██║░╚███║██║░╚██╗
╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝  ╚══════╝╚═╝╚═╝░░╚══╝╚═╝░░╚═╝
 """
title_label = tk.Label(root, text=title_ascii, font=("Courier", 10, "bold"), fg="#ADD8E6", bg="black", justify="left")
title_label.pack(pady=10)

# Entrada de URL
url_label = tk.Label(root, text="Host:", fg="#ADD8E6", bg="black")
url_label.pack()
url_entry = tk.Entry(root, width=50, bg="black", fg="#ADD8E6")
url_entry.pack(pady=5)

# Entrada de padrão
pattern_label = tk.Label(root, text="Padrão de busca:", fg="#ADD8E6", bg="black")
pattern_label.pack()
pattern_entry = tk.Entry(root, width=50, bg="black", fg="#ADD8E6")
pattern_entry.pack(pady=5)

# Botão de busca
search_button = tk.Button(root, text="Buscar", command=start_search, bg="#001f3f", fg="#ADD8E6")
search_button.pack(pady=10)

# Área de resultado
result_text = scrolledtext.ScrolledText(root, width=70, height=20, bg="black", fg="#ADD8E6")
result_text.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
