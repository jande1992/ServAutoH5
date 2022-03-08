# Biblioteker, der skal bruges til programmet.

import shutil
from datetime import datetime
from os import path
import errno
import csv
import zipfile
import os

# Opsætning af tids-variabler, der skal skrives til CSV
Backup_tidspunkt = datetime.now()
Fildato = "Backup - " + str(Backup_tidspunkt.strftime("%d%m%Y"))
Filnavn = 'Backup'
Klokkeslaet = Backup_tidspunkt.strftime("%H:%M:%S")
Dag = Backup_tidspunkt.day
Maaned = Backup_tidspunkt.month
Aar = Backup_tidspunkt.year

# Bruger-input, hvor brugeren skal bestemme, hvilken mappe, der skal kopieres, og hvor den skal kopieres hen.
Source_Sti = input("Skriv stien til mappen, du skal have en backup af: ")
if path.exists(Source_Sti) == True:
    print("Stien er korrekt.")
else:
    print("Stien findes ikke.")
    quit()
Backup_Sti = input("Skriv stien hvor mappen skal kopieres hen: ")
Backup_Sti2 = Backup_Sti + "\\"

# Kopiere Source-sti til Backup-sti.
try:
    shutil.copytree(Source_Sti, Backup_Sti2 + Fildato)
except OSError as err:
    if err.errno == errno.ENOTDIR:
        shutil.copy2(Source_Sti, Backup_Sti) # Hvis ingen fejl, kopieres source-sti til backup-sti.
    else:
        print("Error: % s" % err) # Skriver en fejlmeddelelse, hvis det ikke virker.

# Opret rækkerne og skriv dem ind i CSV-filen med mappenavn, tid og dato.
with open('Backuplog.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Mappenavn ", Filnavn])
    writer.writerow(["Klokkeslaet ", str(Klokkeslaet)])
    writer.writerow(["Aarstal ", str(Aar)])
    writer.writerow(["Maaned ", str(Maaned)])
    writer.writerow(["Dag ", str(Dag)])

# Parameter, der pejer på, hvor den nye backup ligger.
ZipLokation = str(Backup_Sti2 + Fildato)

# Funktion til at zippe filerne i det indtastede directory.
def zipdir(Source_Sti, ziph):

    for root, dirs, files in os.walk(Source_Sti):  # Looper for hver mappe-rod, directory og fil, som skal zippes.
        for fileN in files:
            ziph.write(os.path.join(root, fileN),  # For hver fil skrives der til stien root fileN.
                       os.path.relpath(os.path.join(root, fileN),
                                       os.path.join(Source_Sti, '..'))) # Source-stien sættes sammen med navnet på mappen.


zipf = zipfile.ZipFile('Backup.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir(ZipLokation, zipf)
zipf.close()
quit()

