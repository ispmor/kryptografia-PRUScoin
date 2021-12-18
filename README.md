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
w porównaniu z pierwszym kamieniem milowym, pozbyliśmy się słownika).

```python main.py```