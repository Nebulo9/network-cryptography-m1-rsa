# network-cryptography-m1-rsa
Projet du module **Introduction à la cryptographie des réseaux** en Master 1 RSA (Réseaux et Systèmes autonomes).

## Objectif du projet
Réaliser une simulation d'attaque *DDOS* entre des objets connectés à l'aide de scripts Python.

## Utilisation
### Exécution
#### `ddos_server.py`
```bash
python3 ddos_server.py SERVER_IP:LISTEN_PORT
```
#### `ddos_client.py`
Si le script est éxécuté sur une machine différente de celle utilisée pour le server:
```bash
python3 ddos_client.py SERVER_IP:LISTEN_PORT
```
sinon:
```bash
python3 ddos_client.py LOOPBACK:LISTEN_PORT
```

### Fonctionnement
`ddos_server.py` initialise un *socket* qui va écouter sur un port, donné en argument d'exécution, afin d'établir une connexion avec les machines clientes et leur envoyer des directives.
