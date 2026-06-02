# file di configurazione

QUEUE_SIZE = 5

METODI = ["deposita", "preleva", "svuota"]
PRODOTTI = ["smartphone", "laptop"]

# messaggi
QUEUE_REQUESTS = "/queue/richieste"
QUEUE_RESPONSES = "/queue/risposte"

# formato messaggi
'''
{
"metodo" : str
"id_articolo" : int
"prodotto" : str
}
'''