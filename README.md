# network-cryptography-m1-rsa
Projet du module **Introduction à la cryptographie et la sécurité des réseaux** en Master 1 RSA (Réseaux et Systèmes autonomes).

## Objectif du projet
Réaliser une simulation d'attaque *DDOS* entre des objets connectés à l'aide de scripts Python.
## Exécution
### `ddos_server.py`
```bash
python3 ddos_server.py SERVER_IP:PORT
```
### `ddos_client.py`
Si le script est éxécuté sur une machine différente de celle utilisée pour éxécuter `ddos_server.py`:
```bash
python3 ddos_client.py SERVER_IP:PORT
```
sinon:
```bash
python3 ddos_client.py LOOPBACK:PORT
```

## Fonctionnement
`ddos_server.py` initialise un *socket* qui va écouter sur un port, donné en argument d'exécution, afin d'établir une connexion avec les machines clientes et leur envoyer des directives.
