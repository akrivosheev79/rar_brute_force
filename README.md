# rar_brute_force
Utilite for forgotten password recovery

<b>Requires:</b><br>
    1. Install unrar and add it to PATH<br>
    2. alph.txt have to locate in the same directory. Copy and edit it

<b>Usage:</b> rar_brute_force_3.py [-h] [--chunk_size CHUNK_SIZE] rar pwd_len

        rar Filename for check
        pwd_len Length password for check
        
        -h Read help
        --chunk_size Length of password list for check. Affects to RAM!!! (Default 1000)
        
        
