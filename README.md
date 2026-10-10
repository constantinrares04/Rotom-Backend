# Rotom Backend

## 1. Scop

Rotom Backend este un API REST care conecteaza aplicatia cu baza de date MongoDB. Permite consultarea ingredientelor si retetelor si actualizarea stocului ingredientelor.

API-ul este implementat in `main.py` cu FastAPI si foloseste baza de date `rotom_db`, colectiile `ingrediente` si `retete`.

## 2. Cerinte

- Python 3.9 sau mai nou
- MongoDB instalat si pornit local, la `mongodb://localhost:27017/`
- Pachetele Python din `requirements.txt`

Baza de date trebuie sa existe si sa contina colectiile asteptate de API. Importul datelor seed se face separat.

## 3. Instalare si pornire

Din directorul `rotom-backend`, creeaza si activeaza un mediu virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

In Windows PowerShell, activarea se face cu:

```powershell
.venv\Scripts\Activate.ps1
```

Instaleaza dependentele si porneste serverul:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API-ul este disponibil la `http://localhost:8000`. Documentatia interactiva FastAPI este disponibila la `http://localhost:8000/docs`.

Conexiunea MongoDB este definita direct in `main.py`. Pentru a folosi alta adresa, actualizeaza URI-ul `MongoClient`.

## 4. Rute API

Toate rutele sunt relative la `http://localhost:8000`. API-ul nu foloseste prefixul `/api`. Numele rutelor pentru retete pastreaza forma existenta `recipies`.

### Ingrediente

| Metoda si ruta | Descriere |
|---|---|
| `GET /ing/all` | Returneaza toate ingredientele, cu campurile disponibile. |
| `GET /ings/unavailable` | Returneaza ingredientele cu stocul egal cu zero. |
| `GET /ing/available` | Returneaza ingredientele cu stoc mai mare decat zero. |
| `GET /ing/{id}` | Returneaza ingredientul cu ID-ul indicat. |
| `PUT /modify/{id}?quantity=1` | Adauga valoarea `quantity` la stocul ingredientului. Valorile negative scad stocul; stocul nu poate deveni negativ. |

Exemplu de actualizare a stocului:

```text
PUT http://localhost:8000/modify/1?quantity=2
```

### Retete

| Metoda si ruta | Descriere |
|---|---|
| `GET /recipies/all` | Returneaza ID-ul si numele fiecarei retete, ordonate dupa ID. |
| `GET /recipies/{id}` | Returneaza reteta cu ID-ul indicat. |
| `GET /recipies/ing/{ing_id}` | Returneaza retetele care contin ingredientul cu ID-ul indicat. |
| `GET /recipies/ing_list?ids=1&ids=2` | Returneaza cel mult 10 retete aleatoare ale caror ingrediente sunt toate incluse in ID-urile trimise. |

Pentru `/recipies/ing_list`, trimite fiecare ID ca parametru `ids` repetat. De exemplu:

```text
GET http://localhost:8000/recipies/ing_list?ids=1&ids=2&ids=8
```

Filtrul nu cere ca reteta sa foloseasca toate ID-urile primite; cere ca reteta sa nu contina alte ingrediente in afara listei. Ingredientele retetelor sunt stocate ca ID-uri numerice in array-ul `ingredients`.

## 5. Formatul raspunsurilor

Raspunsurile pentru liste folosesc forma:

```json
{
  "data": [],
  "count": 0
}
```

Raspunsurile pentru o singura inregistrare folosesc un array `data` cu un element. Daca ingredientul sau reteta ceruta nu exista, API-ul intoarce un obiect cu un camp `error`.

## 6. Structura proiectului

```text
rotom-backend/
├── main.py
├── requirements.txt
└── README.md
```

Schemele si datele seed pentru baza de date sunt in proiectul `rotom-db`.
