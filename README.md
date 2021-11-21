# PRUScoin
## Prywatna Rozrywkowa Umowa Szyfrowana
### Kryptografia stosowana, 2021Z, PW EE

Monika Osiak, 291094
Bartosz Puszkarski, 291104

## Jak to w ogóle działa?
Program odczytuje konfigurację początkową z pliku ```input.json```.
Załączony przykład to modelowy przykład takiego pliku. Poprawność pliku
wejściowego nie jest sprawdzana, jako że nie było to jedno z wymagań – chcieliśmy
się skupić na meritum.

Program nie przyjmuje argumentów od użytkownika.
Program nie zapisuje blockchainu do pliku. (Wynika to ze zmiany koncepcji
w porównaniu z poprzednim kamieniem milowym, pozbyliśmy się słownika).

```python main.py```

W pliku ```main.py``` przygotowaliśmy prezentację 4 przykładów, pokazujących
kluczowe funkcjonalności:
* **przykład 1:** ```chain_manager``` prawidłowo weryfikuje poprawność blockchainu, użytkownicy 
są w stanie sprawdzić stan swoich portfeli
* **przykład 2:** ```chain_manager``` po zmianie jednego z bloków wykrywa błąd
* **przykład 3:** po zmianie ostatniego bloku i header hash ```chain_manager``` nie 
wykrywa błędu, ale robi to jeden z użytkowników
* **przykład 4:** uniemożliwiony double spending