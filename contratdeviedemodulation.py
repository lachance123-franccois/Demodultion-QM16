# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:24:27 2026

@author: AWOUNANG
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.signal import sosfiltfilt, butter
from scipy.special import erfc
 
from declarationconstellationMAQ16Optim import M, Vx, Vy, constellation, symboles, nom

def charger_signal(chemin: str, fe: float = 100e6):

    signal = np.fromfile(chemin, dtype=np.float32)
    n = len(signal)
    t = np.arange(n) / fe
    print(f"Signal charge {n} echantillons Fe = {fe/1e6:.2f} MHz")
    return signal, t, n

def afficher_signal(t, signal, n_points=1000, fe=100e6, titre="Signal module"):
    
    plt.figure()
    plt.plot(t[:n_points], signal[:n_points], "b")
    plt.title(f"{titre}—{n_points} pts Fe={fe/1e6} MHz", fontsize=12)
    plt.xlabel("Temps (s)")
    plt.grid(True)
    plt.show()
    
    
def afficher_spectre(signal, fe=100e6):
    
    fft   = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1 / fe)
    plt.figure()
    plt.plot(freqs / 1e6, np.abs(fft), "b")
    plt.title("Spectre du signal module")
    plt.xlabel("Frequence (MHz)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def estimer_frequence_porteuse(signal, fe=100e6, f0_defaut=10e6):
    fft= np.fft.rfft(signal)
    freqs= np.fft.rfftfreq(len(signal), 1 / fe)
    indice = np.argmax(np.abs(fft))
    f0= freqs[indice] if freqs[indice] > 0 else f0_defaut
    print(f"Frequence porteuse estimee : {f0/1e6:.3f} MHz")
    return f0
    

def distance_minimale(constellation):
    dmin = np.inf
    for i, j in combinations(range(len(constellation)), 2):
        d = np.linalg.norm(constellation[i] - constellation[j])
        if d < dmin:
            dmin = d
    print(f"Distance minimale theorique : {dmin:.4f}")
    return dmin

def demoduler_iq(signal, t, f0, th, fe=100e6):
   
    vi= 2 * signal * np.cos(2 * np.pi * f0 * t)
    vq= -2 * signal * np.sin(2 * np.pi * f0 * t)

    fc=6/ th # la frequence de coupure du du filtre. Nous aaurions pu utilser a la ....
                    # place du filtre passe bas un moyennage .
    sos=butter(N=5, Wn=fc, btype="low", fs=fe, output="sos") # 
    i= sosfiltfilt(sos, vi) # ce filtre a ete utilseer en lieu et place du filtre filtfilt car celui si est plus stable et  nous permet d'eviter des explosion des exposant a la demonulation.
    q   = sosfiltfilt(sos, vq)
    return i, q
def afficher_iq(t, i, q, n_points=1000, fe=100e6, titre="Composantes I/Q"):
    plt.figure()
    plt.plot(t[:n_points], i[:n_points], "b", label="Voie I")
    plt.plot(t[:n_points], q[:n_points], "r", label="Voie Q")
    plt.title(f"{titre}  |  Fe={fe/1e6} MHz", fontsize=12)
    plt.xlabel("Temp (s)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def extraire_coefficients(i, q, th, fe=100e6):
  
    ns= int(th * fe)
    s= len(i) // ns
    ak= i[:s * ns].reshape(s, ns).mean(axis=1)
    bk= q[:s * ns].reshape(s, ns).mean(axis=1)
    return ak, bk

def afficher_constellation(ak, bk, constellation,titre="Constellation QM16 reçue"):
   
    plt.figure()
    plt.scatter(ak, bk, s=5, alpha=0.5, color="blue", marker="*", label="Recu")
    plt.scatter(constellation[:, 0], constellation[:, 1],
                color="red", s=100, marker="+", label="Theorique")
    plt.title(titre)
    plt.xlabel("ak (voie I)")
    plt.ylabel("bk (voie Q)")
    plt.grid(True)
    plt.axhline(0, color="k", linewidth=0.5)
    plt.axvline(0, color="k", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    
def decoder_symboles(ak, bk, constellation, symboles):
    indices = []
    for k in range(len(ak)):
        point=np.array([ak[k], bk[k]])
        distances=np.linalg.norm(constellation - point, axis=1)
        indices.append(symboles[np.argmin(distances)])
    return indices


def indices_vers_texte(indices):
    #Convertit les indices QAM-16  en texte ASCII
    message = ""
    for i in range(0, len(indices) - 1, 2):
        valeur   = (indices[i] << 4) + indices[i + 1]
        message += chr(valeur)
    return message


def calculer_ber(indices_ref, indices_b):
    
    #Calcule le taux d'erreur binaire entre deux séquences d'indices.

    n=min(len(indices_ref), len(indices_b))
    bits_ref= np.unpackbits(np.array(indices_ref[:n], dtype=np.uint8))
    bits_b= np.unpackbits(np.array(indices_b[:n],   dtype=np.uint8))
    return np.sum(bits_ref != bits_b) / len(bits_ref)
    


 
def ber_multi_niveaux(niveaux, dossier, indices_ref,constellation, symboles, f0, th, fe=100e6):
    
    #Démodule et calcule le BER pour chaque valeur Eb/N0.

    ns        = int(th * fe)
    liste_ber = []
 
    for db in niveaux:
        fichier  = os.path.join(dossier, f"signalModule{float(db)}db_optim.bin")
        signal_b = np.fromfile(fichier, dtype=np.float32)
        t_b      = np.arange(len(signal_b)) / fe
 
        i, q = demoduler_iq(signal_b, t_b, f0, th, fe)
 
        s    = len(signal_b) // ns
        ak_b = i[:s * ns].reshape(s, ns).mean(axis=1)
        bk_b = q[:s * ns].reshape(s, ns).mean(axis=1)
 
        afficher_constellation(ak_b, bk_b, constellation,
                                titre=f"Constellation  Eb/N0 = {db} dB")
 
        indices_b = decoder_symboles(ak_b, bk_b, constellation, symboles)
        print(f"[{db} dB]  {indices_vers_texte(indices_b)}")
 
        ber = calculer_ber(indices_ref, indices_b)
        liste_ber.append(ber)
        print(f"[{db} dB]  BER = {ber:.4e}")
 
    return liste_ber



def tracer_ber(niveaux, liste_ber):
    #Trace la courbe BER simulation + courbe théorique  QM16
    ebn0_db  = np.linspace(0, 15, 200)
    ebn0_lin = 10 ** (ebn0_db / 10)
    pe_th    = (3/2) * erfc(np.sqrt(ebn0_lin / 5))
    plt.figure(figsize=(8, 5))
    plt.semilogy(ebn0_db, pe_th,"b-", label="Theorique QM16 optim")
    plt.semilogy(niveaux, liste_ber, "ro", markersize=8, label="Simulation")
    plt.title("BER en fonction de Eb/N0")
    plt.xlabel("Eb/N0 (dB)")
    plt.ylabel("BER")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    
def contratdeviedemo():
    
    FE= 100e6
    F0= 10e6
    TH= 1e-6
    DOSSIER ="C:/Users/AWOUNANG/Desktop/Demodulation QM16"
    
    NIVEAUX = [1, 3, 5, 7, 9, 11, 13]
 
    print(f"Démodulation QM16{nom}")
 
    #Signal de reference
    signal, t, _ = charger_signal("signalModule100.0db_optim.bin", fe=FE)
    afficher_signal(t, signal, fe=FE)
    afficher_spectre(signal, fe=FE)
 
    #Distance minimale
    distance_minimale(constellation)
 
    #Demodulation de reference
    i, q = demoduler_iq(signal, t, F0, TH, FE)
    afficher_iq(t, i, q, fe=FE)
 
    #Coefficients symboles
    ak, bk = extraire_coefficients(i, q, TH, FE)
    afficher_constellation(ak, bk, constellation)
 
    #Decodage du message de reference
    indices_ref = decoder_symboles(ak, bk, constellation, symboles)
    print("Message de reference:", indices_vers_texte(indices_ref))
 
    #BER multi-niveaux
    liste_ber = ber_multi_niveaux(NIVEAUX, DOSSIER, indices_ref, constellation, symboles, F0, TH, FE )
 
    # Courbe BER
    tracer_ber(NIVEAUX, liste_ber)
    
if __name__ == "__main__":
    contratdeviedemo()